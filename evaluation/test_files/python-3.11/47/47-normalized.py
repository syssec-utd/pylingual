def showroom_download_by_room_id(room_id, output_dir='.', merge=False, info_only=False, **kwargs):
    """Source: Android mobile"""
    while True:
        timestamp = str(int(time() * 1000))
        api_endpoint = 'https://www.showroom-live.com/api/live/streaming_url?room_id={room_id}&_={timestamp}'.format(room_id=room_id, timestamp=timestamp)
        html = get_content(api_endpoint)
        html = json.loads(html)
        if len(html) >= 1:
            break
        log.w('The live show is currently offline.')
        sleep(1)
    stream_url = [i['url'] for i in html['streaming_url_list'] if i['is_default'] and i['type'] == 'hls'][0]
    assert stream_url
    title = ''
    profile_api = 'https://www.showroom-live.com/api/room/profile?room_id={room_id}'.format(room_id=room_id)
    html = loads(get_content(profile_api))
    try:
        title = html['main_name']
    except KeyError:
        title = 'Showroom_{room_id}'.format(room_id=room_id)
    type_, ext, size = url_info(stream_url)
    print_info(site_info, title, type_, size)
    if not info_only:
        download_url_ffmpeg(url=stream_url, title=title, ext='mp4', output_dir=output_dir)