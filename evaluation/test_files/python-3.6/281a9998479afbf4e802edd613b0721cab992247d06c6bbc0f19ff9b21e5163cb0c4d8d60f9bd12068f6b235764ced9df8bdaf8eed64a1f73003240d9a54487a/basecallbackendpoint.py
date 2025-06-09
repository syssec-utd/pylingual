from typing import NoReturn
import fastapi
from canonical import EmailAddress
from headless.ext.oauth2 import Client
from headless.ext.oauth2.models import OIDCToken
from headless.ext.oauth2.models import TokenResponse
from cbra.core import Endpoint
from ...params import Error
from ...params import ClientStorage
from ...types import AuthorizationState
from ...types import AuthorizeResponse
from ...types import FatalAuthorizationException
from ...types import IFrontendStorage
from ...types import OIDCProvider

class BaseCallbackEndpoint(Endpoint):
    __module__: str = 'cbra.ext.oauth2.server'
    error: Error | None = Error.depends()
    expects_id_token: bool = True
    params: AuthorizeResponse
    provider: OIDCProvider
    token: TokenResponse | None
    state: AuthorizationState
    storage: IFrontendStorage = ClientStorage
    verify_email: bool = True

    def get_redirect_uri(self) -> str:
        assert self.state is not None
        return self.state.redirect_uri

    def is_trusted_email(self, email: EmailAddress | None) -> bool:
        if not self.verify_email or not email:
            return False
        return self.provider.is_trusted_email(email)

    async def post(self) -> fastapi.Response:
        """Callback endpoint for responses from OAuth 2.x/OpenID Connect authorization
        servers. A `POST` request is used when the choses response mode produces such
        a request from the authorization server, such as `form_post` or `form_post.jwt`.
        """
        raise NotImplementedError

    async def get(self) -> fastapi.Response:
        """Callback endpoint for responses from OAuth 2.x/OpenID Connect authorization
        servers.
        """
        await self.session
        try:
            return await self.handle(self.params)
        except Exception as exception:
            response = await self.on_fatal_exception(exception)
            if response:
                return response
            raise

    async def get_client(self) -> Client:
        """Return a :class:`headless.ext.oauth2.Client` instance that can exchange
        the authorization code.
        """
        raise NotImplementedError

    async def on_fatal_exception(self, exception: Exception) -> fastapi.Response | None:
        raise exception

    async def on_malformed_id_token(self, exception: Exception) -> NoReturn:
        raise exception

    async def on_success(self, client: Client, params: AuthorizationState, response: TokenResponse, claims: OIDCToken | None, grant: None=None) -> fastapi.Response:
        return fastapi.responses.RedirectResponse(status_code=303, url=params.return_uri)

    async def handle(self, authorization: AuthorizeResponse) -> fastapi.Response:
        """Handles the response from the authorization server."""
        async with await self.get_client() as client:
            params = await authorization.verify(client, self.storage)
            token = await authorization.obtain(client, params)
            return await self.handle_token_response(client, params, token)

    async def handle_token_response(self, client: Client, params: AuthorizationState, response: TokenResponse) -> fastapi.Response:
        claims = None
        if self.expects_id_token:
            if not response.id_token:
                raise FatalAuthorizationException('The downstream authorization server did not include an OIDC ID Token in the response.')
            try:
                claims = response.id_token.parse()
            except Exception as exception:
                self.logger.exception('Caught fatal %s', type(exception).__name__)
                await self.on_malformed_id_token(exception)
            claims.email_verified = self.is_trusted_email(claims.email)
            self.logger.debug('Receiving OIDC token from %s', claims.iss)
        return await self.on_success(client, params, response, claims, await self.persist(client, params, response, claims))

    async def persist(self, client: Client, params: AuthorizationState, response: TokenResponse, claims: OIDCToken | None) -> None:
        pass