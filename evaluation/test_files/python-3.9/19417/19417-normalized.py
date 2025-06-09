def upload_dir(bucket_name, path_prefix, source_dir, upload_dir_redirect_objects=True, surrogate_key=None, surrogate_control=None, cache_control=None, acl=None, aws_access_key_id=None, aws_secret_access_key=None, aws_profile=None):
    """Upload a directory of files to S3.

    This function places the contents of the Sphinx HTML build directory
    into the ``/path_prefix/`` directory of an *existing* S3 bucket.
    Existing files on S3 are overwritten; files that no longer exist in the
    ``source_dir`` are deleted from S3.

    Parameters
    ----------
    bucket_name : `str`
        Name of the S3 bucket where documentation is uploaded.
    path_prefix : `str`
        The root directory in the bucket where documentation is stored.
    source_dir : `str`
        Path of the Sphinx HTML build directory on the local file system.
        The contents of this directory are uploaded into the ``/path_prefix/``
        directory of the S3 bucket.
    upload_dir_redirect_objects : `bool`, optional
        A feature flag to enable uploading objects to S3 for every directory.
        These objects contain ``x-amz-meta-dir-redirect=true`` HTTP headers
        that tell Fastly to issue a 301 redirect from the directory object to
        the `index.html`` in that directory.
    surrogate_key : `str`, optional
        The surrogate key to insert in the header of all objects
        in the ``x-amz-meta-surrogate-key`` field. This key is used to purge
        builds from the Fastly CDN when Editions change.
        If `None` then no header will be set.
    cache_control : `str`, optional
        This sets the ``Cache-Control`` header on the uploaded
        files. The ``Cache-Control`` header specifically dictates how content
        is cached by the browser (if ``surrogate_control`` is also set).
    surrogate_control : `str`, optional
        This sets the ``x-amz-meta-surrogate-control`` header
        on the uploaded files. The ``Surrogate-Control``
        or ``x-amz-meta-surrogate-control`` header is used in priority by
        Fastly to givern it's caching. This caching policy is *not* passed
        to the browser.
    acl : `str`, optional
        The pre-canned AWS access control list to apply to this upload.
        Can be ``'public-read'``, which allow files to be downloaded
        over HTTP by the public. See
        https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#canned-acl
        for an overview of S3's pre-canned ACL lists. Note that ACL settings
        are not validated locally. Default is `None`, meaning that no ACL
        is applied to an individual object. In this case, use ACLs applied
        to the bucket itself.
    aws_access_key_id : `str`, optional
        The access key for your AWS account. Also set
        ``aws_secret_access_key``.
    aws_secret_access_key : `str`, optional
        The secret key for your AWS account.
    aws_profile : `str`, optional
        Name of AWS profile in :file:`~/.aws/credentials`. Use this instead
        of ``aws_access_key_id`` and ``aws_secret_access_key`` for file-based
        credentials.

    Notes
    -----
    ``cache_control`` and  ``surrogate_control`` can be used together.
    ``surrogate_control`` takes priority in setting Fastly's POP caching,
    while ``cache_control`` then sets the browser's caching. For example:

    - ``cache_control='no-cache'``
    - ``surrogate_control='max-age=31536000'``

    together will ensure that the browser always does an ETAG server query,
    but that Fastly will cache the content for one year (or until purged).
    This configuration is good for files that are frequently changed in place.

    For immutable uploads simply using ``cache_control`` is more efficient
    since it allows the browser to also locally cache content.

    .. seelso:

       - `Fastly: Cache control tutorial
         <https://docs.fastly.com/guides/tutorials/cache-control-tutorial>`_.
       - `Google: HTTP caching <http://ls.st/39v>`_.
    """
    logger = logging.getLogger(__name__)
    logger.debug('s3upload.upload({0}, {1}, {2})'.format(bucket_name, path_prefix, source_dir))
    session = boto3.session.Session(profile_name=aws_profile, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket_name)
    metadata = {}
    if surrogate_key is not None:
        metadata['surrogate-key'] = surrogate_key
    if surrogate_control is not None:
        metadata['surrogate-control'] = surrogate_control
    manager = ObjectManager(session, bucket_name, path_prefix)
    for (rootdir, dirnames, filenames) in os.walk(source_dir):
        bucket_root = os.path.relpath(rootdir, start=source_dir)
        if bucket_root in ('.', '/'):
            bucket_root = ''
        bucket_dirnames = manager.list_dirnames_in_directory(bucket_root)
        for bucket_dirname in bucket_dirnames:
            if bucket_dirname not in dirnames:
                logger.debug('Deleting bucket directory {0}'.format(bucket_dirname))
                manager.delete_directory(bucket_dirname)
        bucket_filenames = manager.list_filenames_in_directory(bucket_root)
        for bucket_filename in bucket_filenames:
            if bucket_filename not in filenames:
                bucket_filename = os.path.join(bucket_root, bucket_filename)
                logger.debug('Deleting bucket file {0}'.format(bucket_filename))
                manager.delete_file(bucket_filename)
        for filename in filenames:
            local_path = os.path.join(rootdir, filename)
            bucket_path = os.path.join(path_prefix, bucket_root, filename)
            logger.debug('Uploading to {0}'.format(bucket_path))
            upload_file(local_path, bucket_path, bucket, metadata=metadata, acl=acl, cache_control=cache_control)
        if upload_dir_redirect_objects is True:
            bucket_dir_path = os.path.join(path_prefix, bucket_root)
            create_dir_redirect_object(bucket_dir_path, bucket, metadata=metadata, acl=acl, cache_control=cache_control)