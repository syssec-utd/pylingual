def push(self, path, name, tag=None):
    """push an image to Google Cloud Drive, meaning uploading it
    
    path: should correspond to an absolte image path (or derive it)
    name: should be the complete uri that the user has requested to push.
    tag: should correspond with an image tag. This is provided to mirror Docker
    """
    parent = self._get_or_create_folder(self._base)
    image = None
    path = os.path.abspath(path)
    bot.debug('PUSH %s' % path)
    if not os.path.exists(path):
        bot.error('%s does not exist.' % path)
        sys.exit(1)
    names = parse_image_name(remove_uri(name), tag=tag)
    if names['version'] is None:
        version = get_image_hash(path)
        names = parse_image_name(remove_uri(name), tag=tag, version=version)
    metadata = self.get_metadata(path, names=names)
    metadata = metadata['data']
    metadata.update(names)
    metadata.update(metadata['attributes']['labels'])
    del metadata['attributes']
    file_metadata = {'name': names['storage'], 'mimeType': 'application/octet-stream', 'parents': [parent['id']], 'properties': metadata}
    media = MediaFileUpload(path, resumable=True)
    try:
        bot.spinner.start()
        image = self._service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        thumbnail = get_thumbnail()
        with open(thumbnail, 'rb') as f:
            body = {'contentHints': {'thumbnail': {'image': base64.urlsafe_b64encode(f.read()).decode('utf8'), 'mimeType': 'image/png'}}}
            image = self._service.files().update(fileId=image['id'], body=body).execute()
        bot.spinner.stop()
        print(image['name'])
    except HttpError:
        bot.error('Error uploading %s' % path)
        pass
    return image