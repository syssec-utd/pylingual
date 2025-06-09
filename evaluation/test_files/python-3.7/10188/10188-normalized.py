def run_build(self, config, bucket, names):
    """run a build, meaning creating a build. Retry if there is failure
    """
    project = self._get_project()
    bot.custom('PROJECT', project, 'CYAN')
    bot.custom('BUILD  ', config['steps'][0]['name'], 'CYAN')
    response = self._build_service.projects().builds().create(body=config, projectId=project).execute()
    build_id = response['metadata']['build']['id']
    status = response['metadata']['build']['status']
    bot.log('build %s: %s' % (build_id, status))
    start = time.time()
    while status not in ['COMPLETE', 'FAILURE', 'SUCCESS']:
        time.sleep(15)
        response = self._build_service.projects().builds().get(id=build_id, projectId=project).execute()
        build_id = response['id']
        status = response['status']
        bot.log('build %s: %s' % (build_id, status))
    end = time.time()
    bot.log('Total build time: %s seconds' % round(end - start, 2))
    if status == 'SUCCESS':
        env = 'SREGISTRY_GOOGLE_STORAGE_PRIVATE'
        blob = bucket.blob(response['artifacts']['objects']['paths'][0])
        if self._get_and_update_setting(env) == None:
            blob.make_public()
            response['public_url'] = blob.public_url
        update_blob_metadata(blob, response, config, bucket, names)
        response['media_link'] = blob.media_link
        response['size'] = blob.size
        response['file_hash'] = blob.md5_hash
    return response