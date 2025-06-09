def build(self, name, recipe='Singularity', context=None, preview=False):
    """trigger a build on Google Cloud (builder then storage) given a name
       recipe, and Github URI where the recipe can be found.
    
       Parameters
       ==========
       recipe: the local recipe to build.
       name: should be the complete uri that the user has requested to push.
       context: the dependency files needed for the build. If not defined, only
                the recipe is uploaded.
       preview: if True, preview but don't run the build

       Environment
       ===========
       SREGISTRY_GOOGLE_BUILD_SINGULARITY_VERSION: the version of Singularity
           to use, defaults to 3.0.2-slim
       SREGISTRY_GOOGLE_BUILD_CLEANUP: after build, delete intermediate 
           dependencies in cloudbuild bucket.

    """
    bot.debug('BUILD %s' % recipe)
    names = parse_image_name(remove_uri(name))
    config = self._load_build_config(name=names['uri'], recipe=recipe)
    build_package = [recipe]
    if context not in [None, '', []]:
        if '.' in context:
            context = glob(os.getcwd() + '/**/*', recursive=True)
        build_package = build_package + context
    package = create_build_package(build_package)
    destination = 'source/%s' % os.path.basename(package)
    blob = self._build_bucket.blob(destination)
    if not blob.exists() and preview is False:
        bot.log('Uploading build package!')
        manifest = self._upload(source=package, bucket=self._build_bucket, destination=destination)
    else:
        bot.log('Build package found in %s.' % self._build_bucket.name)
    config['source']['storageSource']['bucket'] = self._build_bucket.name
    config['source']['storageSource']['object'] = destination
    if preview is False:
        config = self._run_build(config, self._bucket, names)
    if not self._get_and_update_setting('SREGISTRY_GOOGLE_BUILD_CACHE'):
        blob.delete()
    shutil.rmtree(os.path.dirname(package))
    return config