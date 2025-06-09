from __future__ import absolute_import
import datetime
import re
import importlib
import six
from huaweicloudsdkcore.client import Client, ClientBuilder
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.utils import http_utils
from huaweicloudsdkcore.sdk_stream_request import SdkStreamRequest

class VcmAsyncClient(Client):
    PRIMITIVE_TYPES = (float, bool, bytes, six.text_type) + six.integer_types
    NATIVE_TYPES_MAPPING = {'int': int, 'long': int if six.PY3 else long, 'float': float, 'str': str, 'bool': bool, 'date': datetime.date, 'datetime': datetime.datetime, 'object': object}

    def __init__(self):
        super(VcmAsyncClient, self).__init__()
        self.model_package = importlib.import_module('huaweicloudsdkvcm.v2.model')
        self.preset_headers = {'User-Agent': 'HuaweiCloud-SDK-Python'}

    @classmethod
    def new_builder(cls, clazz=None):
        if clazz is None:
            return ClientBuilder(cls)
        if clazz.__name__ != 'VcmClient':
            raise TypeError('client type error, support client type is VcmClient')
        return ClientBuilder(clazz)

    def check_audio_job_async(self, request):
        """查询单个作业

        该 API 用于查询并显示单个作业详情。
        
        Please refer to HUAWEI cloud API Explorer for details.


        :param request: Request instance for CheckAudioJob
        :type request: :class:`huaweicloudsdkvcm.v2.CheckAudioJobRequest`
        :rtype: :class:`huaweicloudsdkvcm.v2.CheckAudioJobResponse`
        """
        return self.check_audio_job_with_http_info(request)

    def check_audio_job_with_http_info(self, request):
        all_params = ['task_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)
        cname = None
        collection_formats = {}
        path_params = {}
        if 'task_id' in local_var_params:
            path_params['task_id'] = local_var_params['task_id']
        query_params = []
        header_params = {}
        form_params = {}
        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()
        response_headers = []
        header_params['Content-Type'] = http_utils.select_header_content_type(['application/json'])
        auth_settings = []
        return self.call_api(resource_path='/v2/{project_id}/services/audio-moderation/tasks/{task_id}', method='GET', path_params=path_params, query_params=query_params, header_params=header_params, body=body_params, post_params=form_params, cname=cname, response_type='CheckAudioJobResponse', response_headers=response_headers, auth_settings=auth_settings, collection_formats=collection_formats, request_type=request.__class__.__name__)

    def check_video_job_async(self, request):
        """查询单个作业

        该API用于查询并显示单个作业详情。
        
        Please refer to HUAWEI cloud API Explorer for details.


        :param request: Request instance for CheckVideoJob
        :type request: :class:`huaweicloudsdkvcm.v2.CheckVideoJobRequest`
        :rtype: :class:`huaweicloudsdkvcm.v2.CheckVideoJobResponse`
        """
        return self.check_video_job_with_http_info(request)

    def check_video_job_with_http_info(self, request):
        all_params = ['task_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)
        cname = None
        collection_formats = {}
        path_params = {}
        if 'task_id' in local_var_params:
            path_params['task_id'] = local_var_params['task_id']
        query_params = []
        header_params = {}
        form_params = {}
        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()
        response_headers = []
        header_params['Content-Type'] = http_utils.select_header_content_type(['application/json'])
        auth_settings = []
        return self.call_api(resource_path='/v2/{project_id}/services/video-moderation/tasks/{task_id}', method='GET', path_params=path_params, query_params=query_params, header_params=header_params, body=body_params, post_params=form_params, cname=cname, response_type='CheckVideoJobResponse', response_headers=response_headers, auth_settings=auth_settings, collection_formats=collection_formats, request_type=request.__class__.__name__)

    def create_audio_job_async(self, request):
        """创建作业

        该接口用于创建语音内容审核的作业。
        
        Please refer to HUAWEI cloud API Explorer for details.


        :param request: Request instance for CreateAudioJob
        :type request: :class:`huaweicloudsdkvcm.v2.CreateAudioJobRequest`
        :rtype: :class:`huaweicloudsdkvcm.v2.CreateAudioJobResponse`
        """
        return self.create_audio_job_with_http_info(request)

    def create_audio_job_with_http_info(self, request):
        all_params = ['create_audio_job_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)
        cname = None
        collection_formats = {}
        path_params = {}
        query_params = []
        header_params = {}
        form_params = {}
        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()
        response_headers = []
        header_params['Content-Type'] = http_utils.select_header_content_type(['application/json;charset=UTF-8'])
        auth_settings = []
        return self.call_api(resource_path='/v2/{project_id}/services/audio-moderation/tasks', method='POST', path_params=path_params, query_params=query_params, header_params=header_params, body=body_params, post_params=form_params, cname=cname, response_type='CreateAudioJobResponse', response_headers=response_headers, auth_settings=auth_settings, collection_formats=collection_formats, request_type=request.__class__.__name__)

    def create_video_job_async(self, request):
        """创建作业

        该接口用于创建视频内容审核的作业。
        
        Please refer to HUAWEI cloud API Explorer for details.


        :param request: Request instance for CreateVideoJob
        :type request: :class:`huaweicloudsdkvcm.v2.CreateVideoJobRequest`
        :rtype: :class:`huaweicloudsdkvcm.v2.CreateVideoJobResponse`
        """
        return self.create_video_job_with_http_info(request)

    def create_video_job_with_http_info(self, request):
        all_params = ['create_video_job_request_body']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)
        cname = None
        collection_formats = {}
        path_params = {}
        query_params = []
        header_params = {}
        form_params = {}
        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()
        response_headers = []
        header_params['Content-Type'] = http_utils.select_header_content_type(['application/json;charset=UTF-8'])
        auth_settings = []
        return self.call_api(resource_path='/v2/{project_id}/services/video-moderation/tasks', method='POST', path_params=path_params, query_params=query_params, header_params=header_params, body=body_params, post_params=form_params, cname=cname, response_type='CreateVideoJobResponse', response_headers=response_headers, auth_settings=auth_settings, collection_formats=collection_formats, request_type=request.__class__.__name__)

    def delete_demo_info_async(self, request):
        """删除语音作业

        删除语音作业
        
        Please refer to HUAWEI cloud API Explorer for details.


        :param request: Request instance for DeleteDemoInfo
        :type request: :class:`huaweicloudsdkvcm.v2.DeleteDemoInfoRequest`
        :rtype: :class:`huaweicloudsdkvcm.v2.DeleteDemoInfoResponse`
        """
        return self.delete_demo_info_with_http_info(request)

    def delete_demo_info_with_http_info(self, request):
        all_params = ['task_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)
        cname = None
        collection_formats = {}
        path_params = {}
        if 'task_id' in local_var_params:
            path_params['task_id'] = local_var_params['task_id']
        query_params = []
        header_params = {}
        form_params = {}
        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()
        response_headers = []
        header_params['Content-Type'] = http_utils.select_header_content_type(['application/json'])
        auth_settings = []
        return self.call_api(resource_path='/v2/{project_id}/services/audio-moderation/tasks/{task_id}', method='DELETE', path_params=path_params, query_params=query_params, header_params=header_params, body=body_params, post_params=form_params, cname=cname, response_type='DeleteDemoInfoResponse', response_headers=response_headers, auth_settings=auth_settings, collection_formats=collection_formats, request_type=request.__class__.__name__)

    def delete_video_job_async(self, request):
        """删除作业

        该API用于删除指定作业。
        
        Please refer to HUAWEI cloud API Explorer for details.


        :param request: Request instance for DeleteVideoJob
        :type request: :class:`huaweicloudsdkvcm.v2.DeleteVideoJobRequest`
        :rtype: :class:`huaweicloudsdkvcm.v2.DeleteVideoJobResponse`
        """
        return self.delete_video_job_with_http_info(request)

    def delete_video_job_with_http_info(self, request):
        all_params = ['task_id']
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)
        cname = None
        collection_formats = {}
        path_params = {}
        if 'task_id' in local_var_params:
            path_params['task_id'] = local_var_params['task_id']
        query_params = []
        header_params = {}
        form_params = {}
        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()
        response_headers = []
        header_params['Content-Type'] = http_utils.select_header_content_type(['application/json'])
        auth_settings = []
        return self.call_api(resource_path='/v2/{project_id}/services/video-moderation/tasks/{task_id}', method='DELETE', path_params=path_params, query_params=query_params, header_params=header_params, body=body_params, post_params=form_params, cname=cname, response_type='DeleteVideoJobResponse', response_headers=response_headers, auth_settings=auth_settings, collection_formats=collection_formats, request_type=request.__class__.__name__)

    def list_audio_jobs_async(self, request):
        """查询作业列表

        查询作业列表
        
        Please refer to HUAWEI cloud API Explorer for details.


        :param request: Request instance for ListAudioJobs
        :type request: :class:`huaweicloudsdkvcm.v2.ListAudioJobsRequest`
        :rtype: :class:`huaweicloudsdkvcm.v2.ListAudioJobsResponse`
        """
        return self.list_audio_jobs_with_http_info(request)

    def list_audio_jobs_with_http_info(self, request):
        all_params = []
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)
        cname = None
        collection_formats = {}
        path_params = {}
        query_params = []
        header_params = {}
        form_params = {}
        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()
        response_headers = []
        header_params['Content-Type'] = http_utils.select_header_content_type(['application/json'])
        auth_settings = []
        return self.call_api(resource_path='/v2/{project_id}/services/audio-moderation/tasks', method='GET', path_params=path_params, query_params=query_params, header_params=header_params, body=body_params, post_params=form_params, cname=cname, response_type='ListAudioJobsResponse', response_headers=response_headers, auth_settings=auth_settings, collection_formats=collection_formats, request_type=request.__class__.__name__)

    def list_video_jobs_async(self, request):
        """查询作业列表

        该API用于查询并显示视频内容审核的作业列表。
        
        Please refer to HUAWEI cloud API Explorer for details.


        :param request: Request instance for ListVideoJobs
        :type request: :class:`huaweicloudsdkvcm.v2.ListVideoJobsRequest`
        :rtype: :class:`huaweicloudsdkvcm.v2.ListVideoJobsResponse`
        """
        return self.list_video_jobs_with_http_info(request)

    def list_video_jobs_with_http_info(self, request):
        all_params = []
        local_var_params = {}
        for attr in request.attribute_map:
            if hasattr(request, attr):
                local_var_params[attr] = getattr(request, attr)
        cname = None
        collection_formats = {}
        path_params = {}
        query_params = []
        header_params = {}
        form_params = {}
        body_params = None
        if isinstance(request, SdkStreamRequest):
            body_params = request.get_file_stream()
        response_headers = []
        header_params['Content-Type'] = http_utils.select_header_content_type(['application/json'])
        auth_settings = []
        return self.call_api(resource_path='/v2/{project_id}/services/video-moderation/tasks', method='GET', path_params=path_params, query_params=query_params, header_params=header_params, body=body_params, post_params=form_params, cname=cname, response_type='ListVideoJobsResponse', response_headers=response_headers, auth_settings=auth_settings, collection_formats=collection_formats, request_type=request.__class__.__name__)

    def call_api(self, resource_path, method, path_params=None, query_params=None, header_params=None, body=None, post_params=None, cname=None, response_type=None, response_headers=None, auth_settings=None, collection_formats=None, request_type=None):
        """Makes the HTTP request and returns deserialized data.

        :param resource_path: Path to method endpoint.
        :param method: Method to call.
        :param path_params: Path parameters in the url.
        :param query_params: Query parameters in the url.
        :param header_params: Header parameters to be
            placed in the request header.
        :param body: Request body.
        :param post_params: Request post form parameters,
            for `application/x-www-form-urlencoded`, `multipart/form-data`.
        :param cname: Used for obs endpoint.
        :param auth_settings: Auth Settings names for the request.
        :param response_type: Response data type.
        :param response_headers: Header should be added to response data.
        :param collection_formats: dict of collection formats for path, query,
            header, and post parameters.
        :param request_type: Request data type.
        :return:
            Return the response directly.
        """
        return self.do_http_request(method=method, resource_path=resource_path, path_params=path_params, query_params=query_params, header_params=header_params, body=body, post_params=post_params, cname=cname, response_type=response_type, response_headers=response_headers, collection_formats=collection_formats, request_type=request_type, async_request=True)