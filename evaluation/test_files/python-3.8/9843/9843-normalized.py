def geturls_new_api(song_ids):
    """ 批量获取音乐的地址 """
    br_to_quality = {128000: 'MD 128k', 320000: 'HD 320k'}
    alters = NetEase().songs_detail_new_api(song_ids)
    urls = [alter['url'] for alter in alters]
    return urls