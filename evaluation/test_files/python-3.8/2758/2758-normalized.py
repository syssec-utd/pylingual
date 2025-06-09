def add_face_from_stream(self, large_face_list_id, image, user_data=None, target_face=None, custom_headers=None, raw=False, callback=None, **operation_config):
    """Add a face to a large face list. The input face is specified as an
        image with a targetFace rectangle. It returns a persistedFaceId
        representing the added face, and persistedFaceId will not expire.

        :param large_face_list_id: Id referencing a particular large face
         list.
        :type large_face_list_id: str
        :param image: An image stream.
        :type image: Generator
        :param user_data: User-specified data about the face for any purpose.
         The maximum length is 1KB.
        :type user_data: str
        :param target_face: A face rectangle to specify the target face to be
         added to a person in the format of "targetFace=left,top,width,height".
         E.g. "targetFace=10,10,100,100". If there is more than one face in the
         image, targetFace is required to specify which face to add. No
         targetFace means there is only one face detected in the entire image.
        :type target_face: list[int]
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param callback: When specified, will be called with each chunk of
         data that is streamed. The callback should take two arguments, the
         bytes of the current chunk of data and the response object. If the
         data is uploading, response will be None.
        :type callback: Callable[Bytes, response=None]
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: PersistedFace or ClientRawResponse if raw=true
        :rtype: ~azure.cognitiveservices.vision.face.models.PersistedFace or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`APIErrorException<azure.cognitiveservices.vision.face.models.APIErrorException>`
        """
    url = self.add_face_from_stream.metadata['url']
    path_format_arguments = {'Endpoint': self._serialize.url('self.config.endpoint', self.config.endpoint, 'str', skip_quote=True), 'largeFaceListId': self._serialize.url('large_face_list_id', large_face_list_id, 'str', max_length=64, pattern='^[a-z0-9-_]+$')}
    url = self._client.format_url(url, **path_format_arguments)
    query_parameters = {}
    if user_data is not None:
        query_parameters['userData'] = self._serialize.query('user_data', user_data, 'str', max_length=1024)
    if target_face is not None:
        query_parameters['targetFace'] = self._serialize.query('target_face', target_face, '[int]', div=',')
    header_parameters = {}
    header_parameters['Accept'] = 'application/json'
    header_parameters['Content-Type'] = 'application/octet-stream'
    if custom_headers:
        header_parameters.update(custom_headers)
    body_content = self._client.stream_upload(image, callback)
    request = self._client.post(url, query_parameters, header_parameters, body_content)
    response = self._client.send(request, stream=False, **operation_config)
    if response.status_code not in [200]:
        raise models.APIErrorException(self._deserialize, response)
    deserialized = None
    if response.status_code == 200:
        deserialized = self._deserialize('PersistedFace', response)
    if raw:
        client_raw_response = ClientRawResponse(deserialized, response)
        return client_raw_response
    return deserialized