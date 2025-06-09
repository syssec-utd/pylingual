class GitInfo(object):
    """Class that keeps information about a git repository in experiment.

    When :meth:`~neptune.projects.Project.create_experiment` is invoked, instance of this class is created to
    store information about git repository.
    This information is later presented in the experiment details tab in the Neptune web application.

    Args:
        commit_id (:obj:`str`): commit id sha.
        message (:obj:`str`, optional, default is ``""``): commit message.
        author_name (:obj:`str`, optional, default is ``""``): commit author username.
        author_email (:obj:`str`, optional, default is ``""``): commit author email.
        commit_date (:obj:`datetime.datetime`, optional, default is ``""``): commit datetime.
        repository_dirty (:obj:`bool`, optional, default is ``True``):
            ``True``, if the repository has uncommitted changes, ``False`` otherwise.
    """

    def __init__(self, commit_id, message='', author_name='', author_email='', commit_date='', repository_dirty=True, active_branch='', remote_urls=None):
        if remote_urls is None:
            remote_urls = []
        if commit_id is None:
            raise TypeError('commit_id must not be None')
        self.commit_id = commit_id
        self.message = message
        self.author_name = author_name
        self.author_email = author_email
        self.commit_date = commit_date
        self.repository_dirty = repository_dirty
        self.active_branch = active_branch
        self.remote_urls = remote_urls

    def __eq__(self, o):
        return o is not None and self.__dict__ == o.__dict__

    def __ne__(self, o):
        return not self.__eq__(o)

    def __str__(self):
        return 'GitInfo({})'.format(self.commit_id)

    def __repr__(self):
        return str(self)