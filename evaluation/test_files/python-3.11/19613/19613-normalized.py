def add_userrnd_shot(project):
    """Add a rnd shot for every user in the project

    :param project: the project that needs its rnd shots updated
    :type project: :class:`muke.models.Project`
    :returns: None
    :rtype: None
    :raises: None
    """
    rndseq = project.sequence_set.get(name=RNDSEQ_NAME)
    users = [u for u in project.users.all()]
    for user in users:
        shot, created = Shot.objects.get_or_create(name=user.username, project=project, sequence=rndseq, defaults={'description': 'rnd shot for user %s' % user.username})
        for t in shot.tasks.all():
            t.users.add(user)
            t.full_clean()
            t.save()