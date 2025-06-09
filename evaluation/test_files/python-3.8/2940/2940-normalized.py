def _get_streams(self):
    """
            Find all the streams for the ITV url
            :return: Mapping of quality to stream
        """
    self.session.http.headers.update({'User-Agent': useragents.FIREFOX})
    video_info = self.video_info()
    video_info_url = video_info.get('data-html5-playlist') or video_info.get('data-video-id')
    res = self.session.http.post(video_info_url, data=json.dumps(self.device_info), headers={'hmac': video_info.get('data-video-hmac')})
    data = self.session.http.json(res, schema=self._video_info_schema)
    log.debug('Video ID info response: {0}'.format(data))
    stype = data['Playlist']['VideoType']
    for media in data['Playlist']['Video']['MediaFiles']:
        url = urljoin(data['Playlist']['Video']['Base'], media['Href'])
        name_fmt = '{pixels}_{bitrate}' if stype == 'CATCHUP' else None
        for s in HLSStream.parse_variant_playlist(self.session, url, name_fmt=name_fmt).items():
            yield s