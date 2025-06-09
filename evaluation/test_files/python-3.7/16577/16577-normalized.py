def download(self, url):
    """
        Downloads a MP3 file that is associated with the track at the URL passed.
        
        :param str url: URL of the track to be downloaded
        """
    try:
        track = self.client.get('/resolve', url=url)
    except HTTPError:
        log.error(f'{url} is not a Soundcloud URL.')
        return
    r = requests.get(self.client.get(track.stream_url, allow_redirects=False).location, stream=True)
    total_size = int(r.headers['content-length'])
    chunk_size = 1000000
    file_name = track.title + '.mp3'
    with open(file_name, 'wb') as f:
        for data in tqdm(r.iter_content(chunk_size), desc=track.title, total=total_size / chunk_size, unit='MB', file=sys.stdout):
            f.write(data)
    return file_name