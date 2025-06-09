class PageRuleOnlyPriority(object):

    def __init__(self, id=None, priority=None):
        """
        :param id: (Optional) API item identifier tag
        :param priority: (Optional) A number that indicates the preference for a page rule over another.
In the case where you may have a catch-all page rule (e.g., #1: '/images/')
but want a rule that is more specific to take precedence (e.g., #2: '/images/special/'),
you'll want to specify a higher priority on the latter (#2) so it will override the first.

        """
        self.id = id
        self.priority = priority