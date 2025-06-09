from velait.common.exceptions import VelaitError

class SearchError(VelaitError):
    status_code = 400

    def __init__(self, name: str, description: str):
        super(SearchError, self).__init__(description)
        self.description = description
        self.name = name

class PaginationLimitsError(VelaitError):
    description = 'page'
    name = 'Pagination limits are invalid'
    status_code = 400
__all__ = ['SearchError', 'PaginationLimitsError']