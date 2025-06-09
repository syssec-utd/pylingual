def get_users_for_sis_course_id(self, sis_course_id, params={}):
    """
        Returns a list of users for the given sis course id.
        """
    return self.get_users_for_course(self._sis_id(sis_course_id, sis_field='course'), params)