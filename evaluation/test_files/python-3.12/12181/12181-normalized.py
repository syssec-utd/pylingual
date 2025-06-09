def serve_image(image_id):
    """Serve the preview image with the given id
    """
    try:
        preview_dir = config()['capture']['preview_dir']
        filepath = config()['capture']['preview'][image_id]
        filepath = filepath.replace('{{previewdir}}', preview_dir)
        filepath = os.path.abspath(filepath)
        if os.path.isfile(filepath):
            directory, filename = filepath.rsplit('/', 1)
            return send_from_directory(directory, filename)
    except (IndexError, KeyError):
        pass
    return ('', 404)