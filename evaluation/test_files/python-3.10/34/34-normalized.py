def acfun_download_by_vid(vid, title, output_dir='.', merge=True, info_only=False, **kwargs):
    """str, str, str, bool, bool ->None

    Download Acfun video by vid.

    Call Acfun API, decide which site to use, and pass the job to its
    extractor.
    """
    info = json.loads(get_content('http://www.acfun.cn/video/getVideo.aspx?id=' + vid))
    sourceType = info['sourceType']
    if 'sourceId' in info:
        sourceId = info['sourceId']
    if sourceType == 'sina':
        sina_download_by_vid(sourceId, title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'youku':
        youku_download_by_vid(sourceId, title=title, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)
    elif sourceType == 'tudou':
        tudou_download_by_iid(sourceId, title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'qq':
        qq_download_by_vid(sourceId, title, True, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'letv':
        letvcloud_download_by_vu(sourceId, '2d8c027396', title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'zhuzhan':
        url = 'http://www.acfun.cn/v/ac' + vid
        yk_streams = youku_acfun_proxy(info['sourceId'], info['encode'], url)
        seq = ['mp4hd3', 'mp4hd2', 'mp4hd', 'flvhd']
        for t in seq:
            if yk_streams.get(t):
                preferred = yk_streams[t]
                break
        size = 0
        for url in preferred[0]:
            (_, _, seg_size) = url_info(url)
            size += seg_size
        if re.search('fid=[0-9A-Z\\-]*.flv', preferred[0][0]):
            ext = 'flv'
        else:
            ext = 'mp4'
        print_info(site_info, title, ext, size)
        if not info_only:
            download_urls(preferred[0], title, ext, size, output_dir=output_dir, merge=merge)
    else:
        raise NotImplementedError(sourceType)
    if not info_only and (not dry_run):
        if not kwargs['caption']:
            print('Skipping danmaku.')
            return
        try:
            title = get_filename(title)
            print('Downloading %s ...\n' % (title + '.cmt.json'))
            cmt = get_srt_json(vid)
            with open(os.path.join(output_dir, title + '.cmt.json'), 'w', encoding='utf-8') as x:
                x.write(cmt)
        except:
            pass