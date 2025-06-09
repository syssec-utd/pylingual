def push(self, path, name, tag=None):
    """push an image to your Dropbox
   
       Parameters
       ==========
       path: should correspond to an absolute image path (or derive it)
       name: should be the complete uri that the user has requested to push.
       tag: should correspond with an image tag. This is provided to mirror Docker

       if the image is less than 150MB, the standard file_upload is used. If
       larger, the image is uploaded in chunks with a progress bar.

    """
    path = os.path.abspath(path)
    bot.debug('PUSH %s' % path)
    if not os.path.exists(path):
        bot.error('%s does not exist.' % path)
        sys.exit(1)
    names = parse_image_name(remove_uri(name), tag=tag)
    metadata = self.get_metadata(path, names=names)
    file_size = os.path.getsize(path)
    chunk_size = 4 * 1024 * 1024
    storage_path = '/%s' % names['storage']
    progress = 0
    bot.show_progress(progress, file_size, length=35)
    with open(path, 'rb') as F:
        if file_size <= chunk_size:
            self.dbx.files_upload(F.read(), storage_path)
        else:
            start = self.dbx.files_upload_session_start(F.read(chunk_size))
            cursor = dropbox.files.UploadSessionCursor(session_id=start.session_id, offset=F.tell())
            commit = dropbox.files.CommitInfo(path=storage_path)
            while F.tell() < file_size:
                progress += chunk_size
                if file_size - F.tell() <= chunk_size:
                    self.dbx.files_upload_session_finish(F.read(chunk_size), cursor, commit)
                else:
                    self.dbx.files_upload_session_append(F.read(chunk_size), cursor.session_id, cursor.offset)
                    cursor.offset = F.tell()
                bot.show_progress(iteration=progress, total=file_size, length=35, carriage_return=False)
    bot.show_progress(iteration=file_size, total=file_size, length=35, carriage_return=True)
    sys.stdout.write('\n')