def f_remove_link(self, name):
    """ Removes a link from from the current group node with a given name.

        Does not delete the link from the hard drive. If you want to do this,
        checkout :func:`~pypet.trajectory.Trajectory.f_delete_links`

        """
    if name not in self._links:
        raise ValueError('No link with name `%s` found under `%s`.' % (name, self._full_name))
    self._nn_interface._remove_link(self, name)