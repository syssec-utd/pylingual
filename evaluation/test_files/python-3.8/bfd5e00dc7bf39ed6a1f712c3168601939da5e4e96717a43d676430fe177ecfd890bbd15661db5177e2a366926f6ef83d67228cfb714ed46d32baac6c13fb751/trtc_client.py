import json
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.abstract_client import AbstractClient
from tencentcloud.trtc.v20190722 import models

class TrtcClient(AbstractClient):
    _apiVersion = '2019-07-22'
    _endpoint = 'trtc.tencentcloudapi.com'
    _service = 'trtc'

    def CreateCloudRecording(self, request):
        """API description:
        This API is used to start an on-cloud recording task. It records the audio and video streams in a room and saves them to the specified cloud storage. You can use this API to record the streams in a room separately, or you can mix the streams first and then record the mixed stream.

        You can use this API to perform the following operations:
        * Specify the anchors whose streams you want or do not want to record by using the `RecordParams` parameter
        * Specify the storage service you want to save recording files to by using the `StorageParams` parameter. Currently, you can only save recording files to VOD (`CloudVod`).
        * Specify transcoding settings for mixed-stream recording, including video resolution, video bitrate, frame rate, and audio quality, by using `MixTranscodeParams`
        * Specify the layout of different videos in mixed-stream recording mode or select an auto-arranged layout template

        Key concepts:
        * Single-stream recording: Record the audio and video of each subscribed user (`UserId`) in a room and save the recording files to VOD.
        * Mixed-stream recording: Mix the audios and videos of subscribed users (`UserId`) in a room, record the mixed stream, and save the recording files to VOD. After a recording task ends, you can go to the VOD console (https://console.cloud.tencent.com/vod/media) to view the recording files.

        :param request: Request instance for CreateCloudRecording.
        :type request: :class:`tencentcloud.trtc.v20190722.models.CreateCloudRecordingRequest`
        :rtype: :class:`tencentcloud.trtc.v20190722.models.CreateCloudRecordingResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('CreateCloudRecording', params, headers=headers)
            response = json.loads(body)
            model = models.CreateCloudRecordingResponse()
            model._deserialize(response['Response'])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def DeleteCloudRecording(self, request):
        """This API is used to stop a recording task. If a task is stopped successfully, but the uploading of recording files has not completed, the backend will continue to upload the files and will notify you via a callback when the upload is completed.

        :param request: Request instance for DeleteCloudRecording.
        :type request: :class:`tencentcloud.trtc.v20190722.models.DeleteCloudRecordingRequest`
        :rtype: :class:`tencentcloud.trtc.v20190722.models.DeleteCloudRecordingResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('DeleteCloudRecording', params, headers=headers)
            response = json.loads(body)
            model = models.DeleteCloudRecordingResponse()
            model._deserialize(response['Response'])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def DescribeCloudRecording(self, request):
        """This API is used to query the status of a recording task after it starts. It works only when a task is in progress. If the task has already ended when this API is called, an error will be returned.
        If a recording file is being uploaded to VOD, the response parameter `StorageFileList` will not contain the information of the recording file. Please listen for the recording file callback to get the information.

        :param request: Request instance for DescribeCloudRecording.
        :type request: :class:`tencentcloud.trtc.v20190722.models.DescribeCloudRecordingRequest`
        :rtype: :class:`tencentcloud.trtc.v20190722.models.DescribeCloudRecordingResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('DescribeCloudRecording', params, headers=headers)
            response = json.loads(body)
            model = models.DescribeCloudRecordingResponse()
            model._deserialize(response['Response'])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def DescribeMixTranscodingUsage(self, request):
        """This API is used to query your usage of TRTC’s On-Cloud MixTranscoding service.
        - If the period queried is one day or shorter, the statistics returned are on a five-minute basis. If the period queried is longer than one day, the statistics returned are on a daily basis.
        - The period queried per request cannot be longer than 31 days.
        - If you query the statistics of the current day, the statistics returned may be inaccurate due to the delay in data collection.
        - You can use this API to query your historical usage or to reconcile data, but we do not recommend you use it for crucial business logic.
        - The rate limit of this API is five calls per second.

        :param request: Request instance for DescribeMixTranscodingUsage.
        :type request: :class:`tencentcloud.trtc.v20190722.models.DescribeMixTranscodingUsageRequest`
        :rtype: :class:`tencentcloud.trtc.v20190722.models.DescribeMixTranscodingUsageResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('DescribeMixTranscodingUsage', params, headers=headers)
            response = json.loads(body)
            model = models.DescribeMixTranscodingUsageResponse()
            model._deserialize(response['Response'])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def DescribeRecordingUsage(self, request):
        """This API is used to query your TRTC recording usage.
        - If the period queried is one day or shorter, the statistics returned are on a five-minute basis. If the period queried is longer than one day, the statistics returned are on a daily basis.
        - The period queried per request cannot be longer than 31 days.
        - If you query the statistics of the current day, the statistics returned may be inaccurate due to the delay in data collection.
        - You can use this API to query your historical usage or to reconcile data, but we do not recommend you use it for crucial business logic.
        - The rate limit of this API is five calls per second.

        :param request: Request instance for DescribeRecordingUsage.
        :type request: :class:`tencentcloud.trtc.v20190722.models.DescribeRecordingUsageRequest`
        :rtype: :class:`tencentcloud.trtc.v20190722.models.DescribeRecordingUsageResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('DescribeRecordingUsage', params, headers=headers)
            response = json.loads(body)
            model = models.DescribeRecordingUsageResponse()
            model._deserialize(response['Response'])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def DescribeRelayUsage(self, request):
        """This API is used to query your usage of TRTC’s relay to CDN service.
        - If the period queried is one day or shorter, the statistics returned are on a five-minute basis. If the period queried is longer than one day, the statistics returned are on a daily basis.
        - The period queried per request cannot be longer than 31 days.
        - If you query the statistics of the current day, the statistics returned may be inaccurate due to the delay in data collection.
        - You can use this API to query your historical usage or to reconcile data, but we do not recommend you use it for crucial business logic.
        - The rate limit of this API is five calls per second.

        :param request: Request instance for DescribeRelayUsage.
        :type request: :class:`tencentcloud.trtc.v20190722.models.DescribeRelayUsageRequest`
        :rtype: :class:`tencentcloud.trtc.v20190722.models.DescribeRelayUsageResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('DescribeRelayUsage', params, headers=headers)
            response = json.loads(body)
            model = models.DescribeRelayUsageResponse()
            model._deserialize(response['Response'])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def DescribeTrtcUsage(self, request):
        """This API is used to query your TRTC audio/video duration.
        - If the period queried is one day or shorter, the statistics returned are on a five-minute basis. If the period queried is longer than one day, the statistics returned are on a daily basis.
        - The period queried per request cannot be longer than 31 days.
        - If you query the statistics of the current day, the statistics returned may be inaccurate due to the delay in data collection.
        - You can use this API to query your historical usage or to reconcile data, but we do not recommend you use it for crucial business logic.
        - The rate limit of this API is five calls per second.

        :param request: Request instance for DescribeTrtcUsage.
        :type request: :class:`tencentcloud.trtc.v20190722.models.DescribeTrtcUsageRequest`
        :rtype: :class:`tencentcloud.trtc.v20190722.models.DescribeTrtcUsageResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('DescribeTrtcUsage', params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTrtcUsageResponse()
            model._deserialize(response['Response'])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def DismissRoom(self, request):
        """This API is used to remove all users from a room and dismiss the room. It supports all platforms. For Android, iOS, Windows, and macOS, the TRTC SDK needs to be upgraded to v6.6 or above.

        :param request: Request instance for DismissRoom.
        :type request: :class:`tencentcloud.trtc.v20190722.models.DismissRoomRequest`
        :rtype: :class:`tencentcloud.trtc.v20190722.models.DismissRoomResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('DismissRoom', params, headers=headers)
            response = json.loads(body)
            model = models.DismissRoomResponse()
            model._deserialize(response['Response'])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def DismissRoomByStrRoomId(self, request):
        """This API is used to remove all users from a room and close the room. It works on all platforms. For Android, iOS, Windows, and macOS, you need to update the TRTC SDK to version 6.6 or above.

        :param request: Request instance for DismissRoomByStrRoomId.
        :type request: :class:`tencentcloud.trtc.v20190722.models.DismissRoomByStrRoomIdRequest`
        :rtype: :class:`tencentcloud.trtc.v20190722.models.DismissRoomByStrRoomIdResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('DismissRoomByStrRoomId', params, headers=headers)
            response = json.loads(body)
            model = models.DismissRoomByStrRoomIdResponse()
            model._deserialize(response['Response'])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def ModifyCloudRecording(self, request):
        """This API is used to modify a recording task. It works only when a task is in progress. If the task has already ended when this API is called, an error will be returned. You need to specify all the parameters for each request instead of just the ones you want to modify.

        :param request: Request instance for ModifyCloudRecording.
        :type request: :class:`tencentcloud.trtc.v20190722.models.ModifyCloudRecordingRequest`
        :rtype: :class:`tencentcloud.trtc.v20190722.models.ModifyCloudRecordingResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('ModifyCloudRecording', params, headers=headers)
            response = json.loads(body)
            model = models.ModifyCloudRecordingResponse()
            model._deserialize(response['Response'])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def RemoveUser(self, request):
        """This API is used to remove a user from a room. It is applicable to scenarios where the anchor, room owner, or admin wants to kick out a user. It supports all platforms. For Android, iOS, Windows, and macOS, the TRTC SDK needs to be upgraded to v6.6 or above.

        :param request: Request instance for RemoveUser.
        :type request: :class:`tencentcloud.trtc.v20190722.models.RemoveUserRequest`
        :rtype: :class:`tencentcloud.trtc.v20190722.models.RemoveUserResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('RemoveUser', params, headers=headers)
            response = json.loads(body)
            model = models.RemoveUserResponse()
            model._deserialize(response['Response'])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def RemoveUserByStrRoomId(self, request):
        """This API is used to remove a user from a room. It allows the anchor, room owner, or admin to kick out a user, and works on all platforms. For Android, iOS, Windows, and macOS, you need to update the TRTC SDK to version 6.6 or above.

        :param request: Request instance for RemoveUserByStrRoomId.
        :type request: :class:`tencentcloud.trtc.v20190722.models.RemoveUserByStrRoomIdRequest`
        :rtype: :class:`tencentcloud.trtc.v20190722.models.RemoveUserByStrRoomIdResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('RemoveUserByStrRoomId', params, headers=headers)
            response = json.loads(body)
            model = models.RemoveUserByStrRoomIdResponse()
            model._deserialize(response['Response'])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def SetUserBlocked(self, request):
        """This API is used to disable or enable the audio and video of a user. It can be used by an anchor, room owner, or admin to block or unblock a user. It supports platforms including Android, iOS, Windows, macOS, web, and WeChat Mini Program. Use this API if the room ID is a number.

        :param request: Request instance for SetUserBlocked.
        :type request: :class:`tencentcloud.trtc.v20190722.models.SetUserBlockedRequest`
        :rtype: :class:`tencentcloud.trtc.v20190722.models.SetUserBlockedResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('SetUserBlocked', params, headers=headers)
            response = json.loads(body)
            model = models.SetUserBlockedResponse()
            model._deserialize(response['Response'])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def SetUserBlockedByStrRoomId(self, request):
        """This API allows an anchor, room owner, admin to mute/unmute a user. It can be used on platforms including Android, iOS, Windows, macOS, web, and WeChat Mini Program. Use this API when the room ID is a string.

        :param request: Request instance for SetUserBlockedByStrRoomId.
        :type request: :class:`tencentcloud.trtc.v20190722.models.SetUserBlockedByStrRoomIdRequest`
        :rtype: :class:`tencentcloud.trtc.v20190722.models.SetUserBlockedByStrRoomIdResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('SetUserBlockedByStrRoomId', params, headers=headers)
            response = json.loads(body)
            model = models.SetUserBlockedByStrRoomIdResponse()
            model._deserialize(response['Response'])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def StartPublishCdnStream(self, request):
        """This API is used to mix streams and relay the mixed stream to CDNs. You can use this API to do the following:
        1. Publish (also known as “relay”) the audio/video stream of one anchor to CDNs. For details, see example 2 (starting a task to relay the audio and video of a stream) and example 3 (starting a task to relay only the audio of a stream).
        2. Mix the streams of multiple anchors in a room or in different rooms and publish the mixed stream to CDNs. You can use `AudioParams.SubscribeAudioList` to specify the users whose audios are mixed, and use `VideoParams.LayoutParams` to specify the layout of the anchors’ videos. For details, see example 1 (mixing streams and publishing the mixed stream to a CDN).
        3. Mix multiple streams in a room according to a template and publish the mixed stream to CDNs. The TRTC backend will detect the change of anchors in the room and adjust the video layout automatically according to the stream mixing template. The following template types are supported:
             - Floating: The entire screen is covered by the video of the first user who enters the room, and the videos of other users are displayed as small windows in rows in the bottom-left corner in room entry sequence. The screen allows up to 4 rows of 4 small videos, which float over the large video. Up to 1 large and 15 small videos can be displayed.
             - Grid: The videos of all users split the screen evenly. The more the users, the smaller the video dimensions. Up to 16 videos are supported.
             - Screen sharing: This is designed for video conferencing and online education. The shared screen (or camera video of the anchor) is always displayed as the large video, which occupies the left half of the screen, and the videos of other users occupy the right half in up to two columns of up to eight small videos each. Up to 1 large video and 15 small videos can be displayed. If the upstream aspect ratio does not match the output, the large video on the left will be scaled and displayed in whole, while the small videos on the right will be cropped.
        4. Publish audio/video streams to up to 10 CDNs at a time. You can use `PublishCdnParams.PublishCdnUrl` to specify the URLs of the CDNs to publish to. To publish to Tencent Cloud’s CDN, set `PublishCdnParams.IsTencentCdn` to 1.
        5. Configure a server-side callback to have Tencent Cloud send relay status updates to your server in the form of HTTP/HTTPS POST requests. To use the callback for relay events, please contact Technical Support.
        6. The API supports four regions: Guangzhou, Shanghai, Beijing, and Hong Kong. If you relay to regions outside the Chinese mainland, select Hong Kong.

        Notes:
        1. **Because On-Cloud MixTranscoding is a paid feature, calling this API will incur MixTranscoding fees. For details, see [Billing of MixTranscoding and Relay to CDN](https://intl.cloud.tencent.com/document/product/647/49446?from_cn_redirect=1).**
        2. **Relaying to third-party CDNs will incur relaying fees. For details, see [Billing of MixTranscoding and Relay to CDN](https://intl.cloud.tencent.com/document/product/647/82155?from_cn_redirect=1).**

        Others:
        1. You need to first call `StartPublishCdnStream` to start a relay task and get the task ID before you can use the `UpdatePublishCdnStream` API to modify the task and `StopPublishCdnStream` to stop the task.
        2. To ensure the stability of relaying, you cannot switch between relaying audio only, relaying audio and video, and relaying video only for the same task.
        3. To ensure the stability of relaying, you cannot change the video codec, audio codec, audio sample rate, audio bitrate, or sound channels using the `UpdatePublishCdnStream` API. We recommend you pass in all the other parameters.
        4. When you relay a single stream, specify both `AudioParams` and `VideoParams` to publish both audio and video, and specify only `AudioParams` to publish audio only. You cannot switch between the two modes during the relaying process. For `VideoParams`, set `Width`, `Height`, `Fps`, `Bitrate`, and `Gop` according to the actual settings used for publishing.
        5. The `SequenceNumber` parameter is required when you call `UpdatePublishCdnStream` to change the relaying parameters. It ensures that multiple requests for the same relaying task are in the correct order. The value of `SequenceNumber` increases each time a new request is made for the same task. If `InternalError` is returned, try again using the same `SequenceNumber`. You don’t need to handle the `FailedOperation.OutdateRequest` error.
        6. You can create a relay task before anchors enter a room, in which case you need to manually call `StopPublishCdnStream` to stop the task. If you don’t, after all the users whose streams are mixed leave the room, the TRTC backend will wait for the timeout period (`AgentParams.MaxIdleTime`) to elapse before stopping the relaying task.

        :param request: Request instance for StartPublishCdnStream.
        :type request: :class:`tencentcloud.trtc.v20190722.models.StartPublishCdnStreamRequest`
        :rtype: :class:`tencentcloud.trtc.v20190722.models.StartPublishCdnStreamResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('StartPublishCdnStream', params, headers=headers)
            response = json.loads(body)
            model = models.StartPublishCdnStreamResponse()
            model._deserialize(response['Response'])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def StopPublishCdnStream(self, request):
        """This API is used to stop a relaying task.

        :param request: Request instance for StopPublishCdnStream.
        :type request: :class:`tencentcloud.trtc.v20190722.models.StopPublishCdnStreamRequest`
        :rtype: :class:`tencentcloud.trtc.v20190722.models.StopPublishCdnStreamResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('StopPublishCdnStream', params, headers=headers)
            response = json.loads(body)
            model = models.StopPublishCdnStreamResponse()
            model._deserialize(response['Response'])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)

    def UpdatePublishCdnStream(self, request):
        """This API is used to change the parameters of a relaying task.
        Note: For details about how to use this API, see the `StartPublishCdnStream` document.

        :param request: Request instance for UpdatePublishCdnStream.
        :type request: :class:`tencentcloud.trtc.v20190722.models.UpdatePublishCdnStreamRequest`
        :rtype: :class:`tencentcloud.trtc.v20190722.models.UpdatePublishCdnStreamResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call('UpdatePublishCdnStream', params, headers=headers)
            response = json.loads(body)
            model = models.UpdatePublishCdnStreamResponse()
            model._deserialize(response['Response'])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)