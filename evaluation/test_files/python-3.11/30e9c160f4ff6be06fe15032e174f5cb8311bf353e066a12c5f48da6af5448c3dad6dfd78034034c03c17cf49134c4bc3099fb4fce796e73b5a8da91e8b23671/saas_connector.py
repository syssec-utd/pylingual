from json import JSONDecodeError
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, cast
import pydash
from loguru import logger
from requests import Response
from fides.api.ops.common_exceptions import FidesopsException, PostProcessingException
from fides.api.ops.graph.traversal import TraversalNode
from fides.api.ops.models.connectionconfig import ConnectionConfig, ConnectionTestStatus
from fides.api.ops.models.policy import Policy
from fides.api.ops.models.privacy_request import Consent, PrivacyRequest
from fides.api.ops.schemas.limiter.rate_limit_config import RateLimitConfig
from fides.api.ops.schemas.saas.saas_config import ClientConfig, ConsentRequestMap, ParamValue, SaaSRequest
from fides.api.ops.schemas.saas.shared_schemas import SaaSRequestParams
from fides.api.ops.service.connectors.base_connector import BaseConnector
from fides.api.ops.service.connectors.saas.authenticated_client import AuthenticatedClient
from fides.api.ops.service.connectors.saas_query_config import SaaSQueryConfig
from fides.api.ops.service.pagination.pagination_strategy import PaginationStrategy
from fides.api.ops.service.processors.post_processor_strategy.post_processor_strategy import PostProcessorStrategy
from fides.api.ops.service.saas_request.saas_request_override_factory import SaaSRequestOverrideFactory, SaaSRequestType
from fides.api.ops.util.collection_util import Row
from fides.api.ops.util.saas_util import assign_placeholders, map_param_values

class SaaSConnector(BaseConnector[AuthenticatedClient]):
    """A connector type to integrate with third-party SaaS APIs"""

    def __init__(self, configuration: ConnectionConfig):
        super().__init__(configuration)
        required_saas_config = configuration.get_saas_config()
        assert required_saas_config is not None
        self.saas_config = required_saas_config
        self.endpoints = self.saas_config.top_level_endpoint_dict
        self.secrets = cast(Dict, configuration.secrets)
        self.current_collection_name: Optional[str] = None
        self.current_privacy_request: Optional[PrivacyRequest] = None
        self.current_saas_request: Optional[SaaSRequest] = None

    def query_config(self, node: TraversalNode) -> SaaSQueryConfig:
        """
        Returns the query config for a given node which includes the endpoints
        and connector param values for the current collection.
        """
        privacy_request = self.current_privacy_request
        assert privacy_request is not None
        return SaaSQueryConfig(node, self.endpoints, self.secrets, self.saas_config.data_protection_request, privacy_request)

    def get_client_config(self) -> ClientConfig:
        """Utility method for getting client config according to the current class state"""
        saas_config_client_config = self.saas_config.client_config
        required_current_saas_request = self.current_saas_request
        assert required_current_saas_request is not None
        current_request_client_config = required_current_saas_request.client_config
        return current_request_client_config or saas_config_client_config

    def get_rate_limit_config(self) -> Optional[RateLimitConfig]:
        """Utility method for getting rate limit config according to the current class state"""
        saas_config_rate_limit_config = self.saas_config.rate_limit_config
        required_current_saas_request = self.current_saas_request
        assert required_current_saas_request is not None
        current_request_rate_limit_config = required_current_saas_request.rate_limit_config
        return current_request_rate_limit_config or saas_config_rate_limit_config or None

    def set_privacy_request_state(self, privacy_request: PrivacyRequest, node: TraversalNode) -> None:
        """
        Sets the class state for the current privacy request
        """
        self.current_collection_name = node.address.collection
        self.current_privacy_request = privacy_request

    def set_saas_request_state(self, current_saas_request: SaaSRequest) -> None:
        """
        Sets the class state for the current saas request
        """
        self.current_saas_request = current_saas_request

    def unset_connector_state(self) -> None:
        """
        Unsets the class state. Called when privacy request execution is complete
        """
        self.current_collection_name = None
        self.current_privacy_request = None
        self.current_saas_request = None

    def test_connection(self) -> Optional[ConnectionTestStatus]:
        """Generates and executes a test connection based on the SaaS config"""
        test_request: SaaSRequest = self.saas_config.test_request
        self.set_saas_request_state(test_request)
        prepared_request = map_param_values('test', f'{self.configuration.name}', test_request, self.secrets)
        client: AuthenticatedClient = self.create_client()
        client.send(prepared_request, test_request.ignore_errors)
        self.unset_connector_state()
        return ConnectionTestStatus.succeeded

    def build_uri(self) -> str:
        """Build base URI for the given connector"""
        client_config = self.get_client_config()
        host = client_config.host
        return f'{client_config.protocol}://{assign_placeholders(host, self.secrets)}'

    def create_client(self) -> AuthenticatedClient:
        """Creates an authenticated request builder"""
        uri = self.build_uri()
        client_config = self.get_client_config()
        rate_limit_config = self.get_rate_limit_config()
        logger.info('Creating client to {}', uri)
        return AuthenticatedClient(uri, self.configuration, client_config, rate_limit_config)

    def retrieve_data(self, node: TraversalNode, policy: Policy, privacy_request: PrivacyRequest, input_data: Dict[str, List[Any]]) -> List[Row]:
        """Retrieve data from SaaS APIs"""
        self.set_privacy_request_state(privacy_request, node)
        query_config: SaaSQueryConfig = self.query_config(node)
        read_requests: List[SaaSRequest] = query_config.get_read_requests_by_identity()
        delete_request: Optional[SaaSRequest] = query_config.get_erasure_request_by_action('delete')
        if not read_requests:
            if delete_request:
                logger.info("Skipping read for the '{}' collection, it is delete-only", self.current_collection_name)
                return [{}]
            raise FidesopsException(f"The 'read' action is not defined for the '{self.current_collection_name}' endpoint in {self.saas_config.fides_key}")
        rows: List[Row] = []
        for read_request in read_requests:
            self.set_saas_request_state(read_request)
            if self._missing_dataset_reference_values(input_data, read_request.param_values):
                return []
            if read_request.request_override:
                return self._invoke_read_request_override(read_request.request_override, self.create_client(), policy, privacy_request, node, input_data, self.secrets)
            prepared_requests: List[SaaSRequestParams] = query_config.generate_requests(input_data, policy, read_request)
            for next_request in prepared_requests:
                while next_request:
                    processed_rows, next_request = self.execute_prepared_request(next_request, privacy_request.get_cached_identity_data(), read_request)
                    rows.extend(processed_rows)
        self.unset_connector_state()
        return rows

    def _missing_dataset_reference_values(self, input_data: Dict[str, Any], param_values: Optional[List[ParamValue]]) -> List[str]:
        """Return a list of dataset reference values that are not found in the input_data map"""
        required_param_value_references = [param_value.name for param_value in param_values or [] if param_value.references]
        provided_input_keys = (list(input_data.get('fidesops_grouped_inputs')[0].keys()) if input_data.get('fidesops_grouped_inputs') else []) + list(input_data.keys())
        missing_dataset_reference_values = list(set(required_param_value_references) - set(provided_input_keys))
        if missing_dataset_reference_values:
            logger.info("The '{}' request of {} is missing the following dataset reference values [{}], skipping traversal", self.current_collection_name, self.saas_config.fides_key, ', '.join(missing_dataset_reference_values))
        return missing_dataset_reference_values

    def execute_prepared_request(self, prepared_request: SaaSRequestParams, identity_data: Dict[str, Any], saas_request: SaaSRequest) -> Tuple[List[Row], Optional[SaaSRequestParams]]:
        """
        Executes the prepared request and handles response postprocessing and pagination.
        Returns processed data and request_params for next page of data if available.
        """
        client: AuthenticatedClient = self.create_client()
        response: Response = client.send(prepared_request, saas_request.ignore_errors)
        response = self._handle_errored_response(saas_request, response)
        response_data = self._unwrap_response_data(saas_request, response)
        rows = self.process_response_data(response_data, identity_data, cast(Optional[List[PostProcessorStrategy]], saas_request.postprocessors))
        logger.info("{} row(s) returned after postprocessing '{}' collection.", len(rows), self.current_collection_name)
        next_request = None
        if saas_request.pagination:
            strategy: PaginationStrategy = PaginationStrategy.get_strategy(saas_request.pagination.strategy, saas_request.pagination.configuration)
            next_request = strategy.get_next_request(prepared_request, self.secrets, response, saas_request.data_path)
        if next_request:
            logger.info("Using '{}' pagination strategy to get next page for '{}'.", saas_request.pagination.strategy, self.current_collection_name)
        return (rows, next_request)

    def process_response_data(self, response_data: Union[List[Dict[str, Any]], Dict[str, Any]], identity_data: Dict[str, Any], postprocessors: Optional[List[PostProcessorStrategy]]) -> List[Row]:
        """
        Runs the raw response through all available postprocessors for the request,
        forwarding the output of one postprocessor into the input of the next.

        The final result is returned as a list of processed objects.
        """
        rows: List[Row] = []
        processed_data = response_data
        for postprocessor in postprocessors or []:
            strategy: PostProcessorStrategy = PostProcessorStrategy.get_strategy(postprocessor.strategy, postprocessor.configuration)
            logger.info("Starting postprocessing of '{}' collection with '{}' strategy.", self.current_collection_name, postprocessor.strategy)
            try:
                processed_data = strategy.process(processed_data, identity_data)
            except Exception as exc:
                raise PostProcessingException(f"Exception occurred during the '{postprocessor.strategy}' postprocessor on the '{self.current_collection_name}' collection: {exc}")
        if not processed_data:
            return rows
        if isinstance(processed_data, list):
            if not all((isinstance(item, dict) for item in processed_data)):
                raise PostProcessingException('The list returned after postprocessing did not contain elements of the same type.')
            rows.extend(processed_data)
        elif isinstance(processed_data, dict):
            rows.append(processed_data)
        else:
            raise PostProcessingException(f"Not enough information to continue processing. The result of postprocessing must be an dict or a list of dicts, found value of '{processed_data}'")
        return rows

    def mask_data(self, node: TraversalNode, policy: Policy, privacy_request: PrivacyRequest, rows: List[Row], input_data: Dict[str, List[Any]]) -> int:
        """Execute a masking request. Return the number of rows that have been updated."""
        self.set_privacy_request_state(privacy_request, node)
        query_config = self.query_config(node)
        masking_request = query_config.get_masking_request()
        if not masking_request:
            raise Exception(f'Either no masking request configured or no valid masking request for {node.address.collection}. Check that MASKING_STRICT env var is appropriately set')
        self.set_saas_request_state(masking_request)
        if masking_request.request_override:
            return self._invoke_masking_request_override(masking_request.request_override, self.create_client(), policy, privacy_request, rows, query_config, masking_request, self.secrets)
        if masking_request.data_path and rows:
            unwrapped = []
            for row in rows:
                unwrapped.extend(pydash.get(row, masking_request.data_path))
            rows = unwrapped
        rows = self.process_response_data(rows, privacy_request.get_cached_identity_data(), cast(Optional[List[PostProcessorStrategy]], masking_request.postprocessors))
        rows_updated = 0
        client = self.create_client()
        for row in rows:
            try:
                prepared_request = query_config.generate_update_stmt(row, policy, privacy_request)
            except ValueError as exc:
                if masking_request.skip_missing_param_values:
                    logger.info('Skipping optional masking request on node {}: {}', node.address.value, exc)
                    continue
                raise exc
            client.send(prepared_request, masking_request.ignore_errors)
            rows_updated += 1
        self.unset_connector_state()
        return rows_updated

    def run_consent_request(self, node: TraversalNode, policy: Policy, privacy_request: PrivacyRequest, identity_data: Dict[str, Any], consent_preferences: List[Consent]) -> bool:
        """Execute a consent request. Return whether the consent request to the third party succeeded.
        Return True if 200 OK
        """
        logger.info("Starting consent request for node: '{}'", node.address.value)
        self.set_privacy_request_state(privacy_request, node)
        query_config = self.query_config(node)
        for consent_options in consent_preferences:
            query_config.action = 'opt_in' if consent_options.opt_in else 'opt_out'
            consent_requests: List[SaaSRequest] = self._get_consent_requests_by_preference(consent_options.opt_in)
            if not consent_requests:
                logger.info("Skipping consent requests on node {}: No '{}' requests defined", node.address.value, query_config.action)
                continue
            for consent_request in consent_requests:
                self.set_saas_request_state(consent_request)
                try:
                    prepared_request: SaaSRequestParams = query_config.generate_consent_stmt(policy, privacy_request, consent_request)
                except ValueError as exc:
                    if consent_request.skip_missing_param_values:
                        logger.info('Skipping optional consent request on node {}: {}', node.address.value, exc)
                        continue
                    raise exc
                client: AuthenticatedClient = self.create_client()
                client.send(prepared_request)
        self.unset_connector_state()
        return True

    def close(self) -> None:
        """Not required for this type"""

    @staticmethod
    def _handle_errored_response(saas_request: SaaSRequest, response: Response) -> Response:
        """
        Checks if given Response is an error and if SaasRequest is configured to ignore errors.
        If so, replaces given Response with empty dictionary.
        """
        if saas_request.ignore_errors and (not response.ok):
            logger.info('Ignoring and clearing errored response with status code {}.', response.status_code)
            response = Response()
            response._content = b'{}'
        return response

    @staticmethod
    def _unwrap_response_data(saas_request: SaaSRequest, response: Response) -> Any:
        """
        Unwrap given Response using data_path in the given SaasRequest
        """
        try:
            return pydash.get(response.json(), saas_request.data_path) if saas_request.data_path else response.json()
        except JSONDecodeError:
            raise FidesopsException(f'Unable to parse JSON response from {saas_request.path}')

    @staticmethod
    def _invoke_read_request_override(override_function_name: str, client: AuthenticatedClient, policy: Policy, privacy_request: PrivacyRequest, node: TraversalNode, input_data: Dict[str, List], secrets: Any) -> List[Row]:
        """
        Invokes the appropriate user-defined SaaS request override for read requests.

        Contains error handling for uncaught exceptions coming out of the override.
        """
        override_function: Callable[..., Union[List[Row], int]] = SaaSRequestOverrideFactory.get_override(override_function_name, SaaSRequestType.READ)
        try:
            return override_function(client, node, policy, privacy_request, input_data, secrets)
        except Exception as exc:
            logger.error("Encountered error executing override access function '{}'", override_function_name, exc_info=True)
            raise FidesopsException(str(exc))

    @staticmethod
    def _invoke_masking_request_override(override_function_name: str, client: AuthenticatedClient, policy: Policy, privacy_request: PrivacyRequest, rows: List[Row], query_config: SaaSQueryConfig, masking_request: SaaSRequest, secrets: Any) -> int:
        """
        Invokes the appropriate user-defined SaaS request override for masking
        (update, delete, data_protection_request) requests.

        Includes the necessary data preparations for override input
        and has error handling for uncaught exceptions coming out of the override
        """
        override_function: Callable[..., Union[List[Row], int]] = SaaSRequestOverrideFactory.get_override(override_function_name, SaaSRequestType(query_config.action))
        try:
            update_param_values: List[Dict[str, Any]] = [query_config.generate_update_param_values(row, policy, privacy_request, masking_request) for row in rows]
            return override_function(client, update_param_values, policy, privacy_request, secrets)
        except Exception:
            logger.error("Encountered error executing override mask function '{}", override_function_name, exc_info=True)
            raise FidesopsException(f"Error executing override mask function '{override_function_name}'")

    def _get_consent_requests_by_preference(self, opt_in: bool) -> List[SaaSRequest]:
        """Helper to either pull out the opt-in requests or the opt out requests that were defined."""
        consent_requests: Optional[ConsentRequestMap] = self.saas_config.consent_requests
        if not consent_requests:
            return []
        return consent_requests.opt_in if opt_in else consent_requests.opt_out