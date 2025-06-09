def get_digests(self):
    """return a list of layers from a manifest.
       The function is intended to work with both version
       1 and 2 of the schema. All layers (including redundant)
       are returned. By default, we try version 2 first,
       then fall back to version 1.

       For version 1 manifests: extraction is reversed

       Parameters
       ==========
       manifest: the manifest to read_layers from

    """
    if not hasattr(self, 'manifests'):
        bot.error('Please retrieve manifests for an image first.')
        sys.exit(1)
    digests = []
    reverseLayers = False
    schemaVersions = list(self.manifests.keys())
    schemaVersions.reverse()
    for schemaVersion in schemaVersions:
        manifest = self.manifests[schemaVersion]
        if manifest['schemaVersion'] == 1:
            reverseLayers = True
        layer_key = 'layers'
        digest_key = 'digest'
        if 'layers' in manifest:
            bot.debug('Image manifest version 2.2 found.')
            break
        elif 'fsLayers' in manifest:
            layer_key = 'fsLayers'
            digest_key = 'blobSum'
            bot.debug('Image manifest version 2.1 found.')
            break
        else:
            msg = 'Improperly formed manifest, '
            msg += 'layers, manifests, or fsLayers must be present'
            bot.error(msg)
            sys.exit(1)
    for layer in manifest[layer_key]:
        if digest_key in layer:
            bot.debug('Adding digest %s' % layer[digest_key])
            digests.append(layer[digest_key])
    if reverseLayers is True:
        message = 'v%s manifest, reversing layers' % schemaVersion
        bot.debug(message)
        digests.reverse()
    return digests