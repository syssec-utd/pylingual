from typing import Collection, Union
from buz.query.query import Query
from buz.query.synchronous import QueryHandler
from buz.query.asynchronous import QueryHandler as AsyncQueryHandler

class MoreThanOneQueryHandlerRelatedException(Exception):

    def __init__(self, query: Query, query_handlers: Collection[Union[QueryHandler, AsyncQueryHandler]]):
        self.query = query
        self.query_handlers = query_handlers
        super().__init__(f'There is more than one handler registered for {query.fqn()}.')