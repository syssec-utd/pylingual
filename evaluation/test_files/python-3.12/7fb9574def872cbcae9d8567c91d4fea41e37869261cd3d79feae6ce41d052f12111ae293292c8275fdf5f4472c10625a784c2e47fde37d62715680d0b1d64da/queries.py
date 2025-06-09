"""
GraphQL Queries of API keys
"""
from typing import Optional
from kili.graphql import BaseQueryWhere, GraphQLQuery

class APIKeyWhere(BaseQueryWhere):
    """
    Tuple to be passed to the APIKeyQuery to restrict the query
    """

    def __init__(self, api_key_id: Optional[str]=None, user_id: Optional[str]=None, api_key: Optional[str]=None):
        self.api_key_id = api_key_id
        self.user_id = user_id
        self.api_key = api_key
        super().__init__()

    def graphql_where_builder(self):
        """Build the GraphQL Where payload sent in the resolver from the SDK APIKeyWhere"""
        return {'user': {'id': self.user_id}, 'id': self.api_key_id, 'key': self.api_key}

class APIKeyQuery(GraphQLQuery):
    """APIKey query."""

    @staticmethod
    def query(fragment):
        """
        Return the GraphQL apiKeys query
        """
        return f'\n        query apiKeys($where: ApiKeyWhere!, $first: PageSize!, $skip: Int!) {{\n          data: apiKeys(where: $where, skip: $skip, first: $first) {{\n            {fragment}\n          }}\n        }}\n        '
    COUNT_QUERY = '\n    query countApiKeys($where: ApiKeyWhere!) {\n      data: countApiKeys(where: $where)\n    }\n    '