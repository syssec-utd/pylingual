def include(self, issue):
    """ Return true if the issue in question should be included """
    only_if_assigned = self.config.get('only_if_assigned', None)
    if only_if_assigned:
        owner = self.get_owner(issue)
        include_owners = [only_if_assigned]
        if self.config.get('also_unassigned', None, asbool):
            include_owners.append(None)
        return owner in include_owners
    only_if_author = self.config.get('only_if_author', None)
    if only_if_author:
        return self.get_author(issue) == only_if_author
    return True