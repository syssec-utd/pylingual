from kentik_api.api_calls import query_methods
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.public.query_object import QueryChartResult, QueryDataResult, QueryObject, QueryURLResult
from kentik_api.public.query_sql import QuerySQL, QuerySQLResult
from kentik_api.requests_payload.queries_payload import QueryChartResponse, QueryDataResponse, QueryURLResponse

class QueryAPI(BaseAPI):
    """Exposes Kentik API's Query API methods"""

    def sql(self, query: QuerySQL) -> QuerySQLResult:
        apicall = query_methods.query_sql()
        payload = query
        response = self.send(apicall, payload)
        return QuerySQLResult.from_json(response.text)

    def data(self, query: QueryObject) -> QueryDataResult:
        apicall = query_methods.query_data()
        payload = query
        response = self.send(apicall, payload)
        return QueryDataResponse.from_json(response.text).to_query_data_result()

    def chart(self, query: QueryObject) -> QueryChartResult:
        apicall = query_methods.query_chart()
        payload = query
        response = self.send(apicall, payload)
        return QueryChartResponse.from_json(response.text).to_query_chart_result()

    def url(self, query: QueryObject) -> QueryURLResult:
        apicall = query_methods.query_url()
        payload = query
        response = self.send(apicall, payload)
        return QueryURLResponse(response.text).to_query_url_result()