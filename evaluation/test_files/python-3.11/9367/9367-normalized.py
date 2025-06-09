def _access_user_info(self):
    """
        Accesses the :attr:`.user_info_url`.

        :returns:
            :class:`.UserInfoResponse`

        """
    url = self.user_info_url.format(**self.user.__dict__)
    return self.access(url)