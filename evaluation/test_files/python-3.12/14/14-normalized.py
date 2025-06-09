def download_by_id(self, vid='', title=None, output_dir='.', merge=True, info_only=False, **kwargs):
    """self, str->None
        
        Keyword arguments:
        self: self
        vid: The video ID for BokeCC cloud, something like
        FE3BB999594978049C33DC5901307461
        
        Calls the prepare() to download the video.
        
        If no title is provided, this method shall try to find a proper title
        with the information providin within the
        returned content of the API."""
    assert vid
    self.prepare(vid=vid, title=title, **kwargs)
    self.extract(**kwargs)
    self.download(output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)