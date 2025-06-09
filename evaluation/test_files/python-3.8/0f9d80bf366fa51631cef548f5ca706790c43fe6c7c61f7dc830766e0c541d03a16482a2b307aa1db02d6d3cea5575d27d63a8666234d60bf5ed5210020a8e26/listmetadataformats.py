"""
Implementation of ListMetadataFormats verb
"""
import re
import validators
from lxml import etree
from .request import OAIRequest
from .response import OAIResponse
from .exceptions import OAIErrorIdDoesNotExist, OAIErrorNoMetadataFormats, OAIRepoInternalException

class MetadataFormatValidator:
    """Validator for the MetadataFormat class"""

    def errors(self):
        """
        Verify fields are valid and present where required. Returning a list of descriptive
        errors if any issues were found.
        """
        failures = []
        failures.extend(self._metadata_prefix_failures())
        failures.extend(self._schema_failures())
        failures.extend(self._metadata_namespace_failures())
        return failures

    def _metadata_prefix_failures(self):
        """Return a list of metadata_prefix failures"""
        pattern = re.compile("^[A-Za-z0-9-_.!~*'\\(\\)]+$")
        return [] if pattern.search(self.metadata_prefix) is not None else ["metadata_prefix contains invalid character(s); allowed chars: A-Za-z0-9-_.!~*'()"]

    def _schema_failures(self):
        """Return a list of schema failures"""
        return ['schema must be a valid URL'] if not validators.url(self.schema) else []

    def _metadata_namespace_failures(self):
        """Return a list of metadata_namespace failures"""
        return ['metadata_namespace must be a valid URL'] if not validators.url(self.metadata_namespace) else []

class ListMetadataFormatsRequest(OAIRequest):
    """
    Parse a request for the ListMetadataFormats verb
    raises:
        OAIErrorBadArgument
    """

    def __init__(self):
        super().__init__()
        self.optional_args = ['identifier']
        self.identifier: str = None

    def post_parse(self):
        """Runs after args are parsed"""
        if self.args:
            self.identifier = self.args['identifier']

    def __repr__(self):
        return f'ListMetadataFormatsRequest(identifier={self.identifier})'

class ListMetadataFormatsResponse(OAIResponse):
    """
    Generate a resposne for the ListMetadataFormats verb
    raises:
        OAIErrorIdDoesNotExist
        OAIErrorNoMetadataFormats
    """

    def __repr__(self):
        return f'ListMetadataFormatsResponse(identifier={self.request.identifier})'

    def body(self) -> etree.Element:
        """Response body"""
        identifier = self.request.identifier
        if identifier and (not self.repository.data.is_valid_identifier(identifier)):
            raise OAIErrorIdDoesNotExist('The given identifier does not exist.')
        mdformats = self.repository.data.get_metadata_formats(identifier)
        if not mdformats:
            raise OAIErrorNoMetadataFormats('No metadata fomats found for given identifier.')
        xmlb = etree.Element('ListMetadataFormats')
        for mdformat in mdformats:
            errors = mdformat.errors()
            if errors:
                raise OAIRepoInternalException(f'Invalid MetadataFormat instance: {errors}')
            self.add_format(xmlb, mdformat)
        return xmlb

    def add_format(self, xmlb: etree.Element, mdformat: dict):
        """
        Add the given metadta format to the provided xml element
        """
        mdf_elem = etree.SubElement(xmlb, 'metadataFormat')
        elem = etree.SubElement(mdf_elem, 'metadataPrefix')
        elem.text = mdformat.metadata_prefix
        elem = etree.SubElement(mdf_elem, 'schema')
        elem.text = mdformat.schema
        elem = etree.SubElement(mdf_elem, 'metadataNamespace')
        elem.text = mdformat.metadata_namespace