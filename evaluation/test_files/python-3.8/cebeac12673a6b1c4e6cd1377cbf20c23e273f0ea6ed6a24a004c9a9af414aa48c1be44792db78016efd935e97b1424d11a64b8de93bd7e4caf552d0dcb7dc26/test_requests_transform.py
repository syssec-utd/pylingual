"""Requests transform tests."""
import dictdiffer
from invenio_rdm_migrator.streams.requests import InclusionRequestEntry, RequestEntry, RequestTransform

class MockRequestTransform(RequestTransform):
    """Mock class for request data transformation."""

    def _request(self, entry):
        """Transform the request."""
        return {'key': 'value'}

def test_request_transform():
    """Test the full request transformation."""
    result = MockRequestTransform()._transform({})
    expected = {'key': 'value'}
    assert not list(dictdiffer.diff(result, expected))

class MockRequestEntry(RequestEntry):
    """Transform a single mock request entry."""

    def _created(self, entry):
        """Returns the creation date of the request."""
        return '01/01/2023'

    def _updated(self, entry):
        """Returns the update date of the request."""
        return '01/01/2023'

    def _version_id(self, entry):
        """mock version."""
        return '1'

    def _json(self, entry):
        """Returns the request json body."""
        return {}

    def _number(self, entry):
        """Returns the request number."""
        return '1'

    def _expires_at(self, entry):
        """Returns the request expiration date."""
        return '01/01/2023'

def test_request_entry():
    """Test the request entry transformation."""
    result = MockRequestEntry().transform({})
    expected = {'created': '01/01/2023', 'updated': '01/01/2023', 'version_id': '1', 'json': {}, 'number': '1', 'expires_at': '01/01/2023'}
    assert not list(dictdiffer.diff(result, expected))

class MockInclusionRequestEntry(InclusionRequestEntry, MockRequestEntry):
    """Transform a single mock request entry."""

    def _title(self, entry):
        """Returns the request title."""
        return 'title'

    def _topic(self, entry):
        """Returns the request topic."""
        return 'topic'

    def _receiver(self, entry):
        """Returns the request receiver."""
        return 'receiver'

    def _created_by(self, entry):
        """Returns the request creation reference."""
        return 'someone'

def test_inclusion_request_entry():
    """Test the request entry transformation."""
    result = MockInclusionRequestEntry().transform({})
    expected = {'created': '01/01/2023', 'updated': '01/01/2023', 'version_id': '1', 'json': {'type': 'community-inclusion', 'title': 'title', 'topic': 'topic', 'status': 'submitted', 'receiver': 'receiver', 'created_by': 'someone', '$schema': 'local://requests/request-v1.0.0.json'}, 'number': '1', 'expires_at': '01/01/2023'}
    assert not list(dictdiffer.diff(result, expected))