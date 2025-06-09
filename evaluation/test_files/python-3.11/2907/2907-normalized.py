def parse_variant_playlist(cls, session_, url, name_key='name', name_prefix='', check_streams=False, force_restart=False, name_fmt=None, start_offset=0, duration=None, **request_params):
    """Attempts to parse a variant playlist and return its streams.

        :param url: The URL of the variant playlist.
        :param name_key: Prefer to use this key as stream name, valid keys are:
                         name, pixels, bitrate.
        :param name_prefix: Add this prefix to the stream names.
        :param check_streams: Only allow streams that are accessible.
        :param force_restart: Start at the first segment even for a live stream
        :param name_fmt: A format string for the name, allowed format keys are
                         name, pixels, bitrate.
        """
    locale = session_.localization
    name_key = request_params.pop('namekey', name_key)
    name_prefix = request_params.pop('nameprefix', name_prefix)
    audio_select = session_.options.get('hls-audio-select') or []
    res = session_.http.get(url, exception=IOError, **request_params)
    try:
        parser = hls_playlist.load(res.text, base_uri=res.url)
    except ValueError as err:
        raise IOError('Failed to parse playlist: {0}'.format(err))
    streams = {}
    for playlist in filter(lambda p: not p.is_iframe, parser.playlists):
        names = dict(name=None, pixels=None, bitrate=None)
        audio_streams = []
        fallback_audio = []
        default_audio = []
        preferred_audio = []
        for media in playlist.media:
            if media.type == 'VIDEO' and media.name:
                names['name'] = media.name
            elif media.type == 'AUDIO':
                audio_streams.append(media)
        for media in audio_streams:
            if not media.uri:
                continue
            if not fallback_audio and media.default:
                fallback_audio = [media]
            if not default_audio and (media.autoselect and locale.equivalent(language=media.language)):
                default_audio = [media]
            if ('*' in audio_select or media.language in audio_select or media.name in audio_select) or ((not preferred_audio or media.default) and locale.explicit and locale.equivalent(language=media.language)):
                preferred_audio.append(media)
        fallback_audio = fallback_audio or (len(audio_streams) and audio_streams[0].uri and [audio_streams[0]])
        if playlist.stream_info.resolution:
            width, height = playlist.stream_info.resolution
            names['pixels'] = '{0}p'.format(height)
        if playlist.stream_info.bandwidth:
            bw = playlist.stream_info.bandwidth
            if bw >= 1000:
                names['bitrate'] = '{0}k'.format(int(bw / 1000.0))
            else:
                names['bitrate'] = '{0}k'.format(bw / 1000.0)
        if name_fmt:
            stream_name = name_fmt.format(**names)
        else:
            stream_name = names.get(name_key) or names.get('name') or names.get('pixels') or names.get('bitrate')
        if not stream_name:
            continue
        if stream_name in streams:
            stream_name = '{0}_alt'.format(stream_name)
            num_alts = len(list(filter(lambda n: n.startswith(stream_name), streams.keys())))
            if num_alts >= 2:
                continue
            elif num_alts > 0:
                stream_name = '{0}{1}'.format(stream_name, num_alts + 1)
        if check_streams:
            try:
                session_.http.get(playlist.uri, **request_params)
            except KeyboardInterrupt:
                raise
            except Exception:
                continue
        external_audio = preferred_audio or default_audio or fallback_audio
        if external_audio and FFMPEGMuxer.is_usable(session_):
            external_audio_msg = ', '.join(['(language={0}, name={1})'.format(x.language, x.name or 'N/A') for x in external_audio])
            log.debug('Using external audio tracks for stream {0} {1}', name_prefix + stream_name, external_audio_msg)
            stream = MuxedHLSStream(session_, video=playlist.uri, audio=[x.uri for x in external_audio if x.uri], force_restart=force_restart, start_offset=start_offset, duration=duration, **request_params)
        else:
            stream = cls(session_, playlist.uri, force_restart=force_restart, start_offset=start_offset, duration=duration, **request_params)
        streams[name_prefix + stream_name] = stream
    return streams