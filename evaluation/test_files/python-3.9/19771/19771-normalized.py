def music_info(songid):
    """
    Get music info from baidu music api
    """
    if isinstance(songid, list):
        songid = ','.join(songid)
    data = {'hq': 1, 'songIds': songid}
    res = requests.post(MUSIC_INFO_URL, data=data)
    info = res.json()
    music_data = info['data']
    songs = []
    for song in music_data['songList']:
        (song_link, size) = _song_link(song, music_data['xcode'])
        songs.append({'name': song['songName'], 'singer': song['artistName'], 'lrc_link': song['lrcLink'], 'song_link': song_link, 'size': size})
    return songs