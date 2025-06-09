def parse_image_name(image_name, tag=None, version=None, defaults=True, ext='sif', default_collection='library', default_tag='latest', base=None, lowercase=True):
    """return a collection and repo name and tag
    for an image file.
    
    Parameters
    =========
    image_name: a user provided string indicating a collection,
                image, and optionally a tag.
    tag: optionally specify tag as its own argument
         over-rides parsed image tag
    defaults: use defaults "latest" for tag and "library"
              for collection. 
    base: if defined, remove from image_name, appropriate if the
          user gave a registry url base that isn't part of namespace.
    lowercase: turn entire URI to lowercase (default is True)
    """
    original = image_name
    if base is not None:
        image_name = image_name.replace(base, '').strip('/')
    image_name = re.sub('[.](img|simg|sif)', '', image_name)
    uri_regexes = [_reduced_uri, _default_uri, _docker_uri]
    for r in uri_regexes:
        match = r.match(image_name)
        if match:
            break
    if not match:
        bot.exit('Could not parse image "%s"! Exiting.' % image)
    registry = match.group('registry')
    collection = match.group('collection')
    repo_name = match.group('repo')
    repo_tag = match.group('tag')
    version = match.group('version')
    assert repo_name
    collection = set_default(collection, default_collection, defaults)
    repo_tag = set_default(repo_tag, default_tag, defaults)
    if lowercase:
        collection = collection.lower().rstrip('/')
        repo_name = repo_name.lower()
        repo_tag = repo_tag.lower()
    else:
        collection = collection.rstrip('/')
    if version != None:
        version = version.lower()
    if registry == None:
        uri = '%s/%s' % (collection, repo_name)
    else:
        uri = '%s/%s/%s' % (registry, collection, repo_name)
    url = uri
    if repo_tag != None:
        uri = '%s-%s' % (uri, repo_tag)
        tag_uri = '%s:%s' % (url, repo_tag)
    storage_version = None
    if version is not None:
        uri = '%s@%s' % (uri, version)
        tag_uri = '%s@%s' % (tag_uri, version)
        storage_version = '%s@%s.%s' % (tag_uri, version, ext)
    storage = '%s.%s' % (uri, ext)
    storage_uri = '%s.%s' % (tag_uri, ext)
    result = {'collection': collection, 'original': original, 'registry': registry, 'image': repo_name, 'url': url, 'tag': repo_tag, 'version': version, 'storage': storage, 'storage_uri': storage_uri, 'storage_version': storage_version or storage_uri, 'tag_uri': tag_uri, 'uri': uri}
    return result