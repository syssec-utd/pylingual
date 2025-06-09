import json
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.abstract_client import AbstractClient
from tencentcloud.yinsuda.v20220527 import models

class YinsudaClient(AbstractClient):
    _apiVersion = '2022-05-27'
    _endpoint = 'yinsuda.tencentcloudapi.com'
    _service = 'yinsuda'

    def BatchDescribeKTVMusicDetails(self, request):
        """批量获取歌曲详细信息，包括：歌词下载链接、播放凭证、音高数据下载链接信息等。

        :param request: Request instance for BatchDescribeKTVMusicDetails.
        :type request: :class:`tencentcloud.yinsuda.v20220527.models.BatchDescribeKTVMusicDetailsRequest`
        :rtype: :class:`tencentcloud.yinsuda.v20220527.models.BatchDescribeKTVMusicDetailsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('BatchDescribeKTVMusicDetails', params, headers=headers)
            response = json.loads(body)
            if 'Error' not in response['Response']:
                model = models.BatchDescribeKTVMusicDetailsResponse()
                model._deserialize(response['Response'])
                return model
            else:
                code = response['Response']['Error']['Code']
                message = response['Response']['Error']['Message']
                reqid = response['Response']['RequestId']
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def DescribeKTVPlaylistDetail(self, request):
        """根据歌单 Id 获取歌单详情。

        :param request: Request instance for DescribeKTVPlaylistDetail.
        :type request: :class:`tencentcloud.yinsuda.v20220527.models.DescribeKTVPlaylistDetailRequest`
        :rtype: :class:`tencentcloud.yinsuda.v20220527.models.DescribeKTVPlaylistDetailResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('DescribeKTVPlaylistDetail', params, headers=headers)
            response = json.loads(body)
            if 'Error' not in response['Response']:
                model = models.DescribeKTVPlaylistDetailResponse()
                model._deserialize(response['Response'])
                return model
            else:
                code = response['Response']['Error']['Code']
                message = response['Response']['Error']['Message']
                reqid = response['Response']['RequestId']
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def DescribeKTVPlaylists(self, request):
        """获取歌单列表。

        :param request: Request instance for DescribeKTVPlaylists.
        :type request: :class:`tencentcloud.yinsuda.v20220527.models.DescribeKTVPlaylistsRequest`
        :rtype: :class:`tencentcloud.yinsuda.v20220527.models.DescribeKTVPlaylistsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('DescribeKTVPlaylists', params, headers=headers)
            response = json.loads(body)
            if 'Error' not in response['Response']:
                model = models.DescribeKTVPlaylistsResponse()
                model._deserialize(response['Response'])
                return model
            else:
                code = response['Response']['Error']['Code']
                message = response['Response']['Error']['Message']
                reqid = response['Response']['RequestId']
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def DescribeKTVSuggestions(self, request):
        """根据关键词获取联想词列表。

        :param request: Request instance for DescribeKTVSuggestions.
        :type request: :class:`tencentcloud.yinsuda.v20220527.models.DescribeKTVSuggestionsRequest`
        :rtype: :class:`tencentcloud.yinsuda.v20220527.models.DescribeKTVSuggestionsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('DescribeKTVSuggestions', params, headers=headers)
            response = json.loads(body)
            if 'Error' not in response['Response']:
                model = models.DescribeKTVSuggestionsResponse()
                model._deserialize(response['Response'])
                return model
            else:
                code = response['Response']['Error']['Code']
                message = response['Response']['Error']['Message']
                reqid = response['Response']['RequestId']
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def SearchKTVMusics(self, request):
        """根据关键词搜索歌曲，返回相关歌曲列表。

        :param request: Request instance for SearchKTVMusics.
        :type request: :class:`tencentcloud.yinsuda.v20220527.models.SearchKTVMusicsRequest`
        :rtype: :class:`tencentcloud.yinsuda.v20220527.models.SearchKTVMusicsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('SearchKTVMusics', params, headers=headers)
            response = json.loads(body)
            if 'Error' not in response['Response']:
                model = models.SearchKTVMusicsResponse()
                model._deserialize(response['Response'])
                return model
            else:
                code = response['Response']['Error']['Code']
                message = response['Response']['Error']['Message']
                reqid = response['Response']['RequestId']
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)