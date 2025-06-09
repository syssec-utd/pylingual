from typing import Optional, TYPE_CHECKING
from mstrio.utils.error_handlers import ErrorHandler
if TYPE_CHECKING:
    from requests_futures.sessions import FuturesSession
    from mstrio.connection import Connection

@ErrorHandler(err_msg='Error listing Contact Groups.')
def get_contact_groups(connection: 'Connection', offset: int=0, limit: int=1000, error_msg: Optional[str]=None):
    """Get a list of all contact groups that the authenticated user has access
        to.

    Args:
        connection: MicroStrategy REST API connection object
        offset (int, optional): Starting point within the collection of returned
            results. Used to control paging behavior. Default is 0.
        limit (int, optional): Maximum number of items returned for a single
            request. Used to control paging behavior. Use -1 for no limit.
            Default is 1000.
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. Expected status is 200.
    """
    url = f'{connection.base_url}/api/contactGroups'
    params = {'offset': offset, 'limit': limit}
    return connection.get(url=url, params=params)

def get_contact_groups_async(future_session: 'FuturesSession', connection: 'Connection', offset: int=0, limit: int=1000):
    """Get a list of all contact groups that the authenticated user has access
        to.

    Args:
        future_session(object): Future Session object to call MicroStrategy REST
            Server asynchronously
        connection: MicroStrategy REST API connection object
        offset (int, optional): Starting point within the collection of returned
            results. Used to control paging behavior. Default is 0.
        limit (int, optional): Maximum number of items returned for a single
            request. Used to control paging behavior. Use -1 for no limit.
            Default is 1000.

    Returns:
        Complete Future object.
    """
    url = f'{connection.base_url}/api/contactGroups'
    params = {'offset': offset, 'limit': limit}
    future = future_session.get(url, params=params)
    return future

@ErrorHandler(err_msg='Error creating Contact Group.')
def create_contact_group(connection: 'Connection', body: dict, error_msg: Optional[str]=None):
    """Create a new contact group.

    Args:
        connection: MicroStrategy REST API connection object
        body: Contact group creation body
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. Expected status is 201.
    """
    url = f'{connection.base_url}/api/contactGroups'
    return connection.post(url=url, json=body)

@ErrorHandler(err_msg='Error getting Contact Group with ID {id}')
def get_contact_group(connection: 'Connection', id: str, error_msg: Optional[str]=None):
    """Get contact group by a specific id.

    Args:
        connection: MicroStrategy REST API connection object
        id: ID of the contact group
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. Expected status is 200.
    """
    url = f'{connection.base_url}/api/contactGroups/{id}'
    return connection.get(url=url)

@ErrorHandler(err_msg='Error updating Contact Group with ID {id}')
def update_contact_group(connection: 'Connection', id: str, body: dict, error_msg: Optional[str]=None):
    """Update a contact group.

    Args:
        connection: MicroStrategy REST API connection object
        id: ID of the contact group
        body: Contact group update info.
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. Expected status is 200.
    """
    url = f'{connection.base_url}/api/contactGroups/{id}'
    return connection.put(url=url, json=body)

@ErrorHandler(err_msg='Error deleting Contact Group with ID {id}')
def delete_contact_group(connection: 'Connection', id: str, error_msg: Optional[str]=None):
    """Delete a contact group.

    Args:
        connection: MicroStrategy REST API connection object
        id: ID of the contact group
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. Expected status is 204.
    """
    url = f'{connection.base_url}/api/contactGroups/{id}'
    return connection.delete(url=url)