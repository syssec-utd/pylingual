def get_student_messaging_for_sis_course_id_and_sis_user_id(self, sis_user_id, sis_course_id):
    """
        Returns student messaging data for the given user_id and course_id.

        https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_messaging
        """
    url = '/api/v1/courses/%s/analytics/users/sis_user_id:%s/communication.json' % (self._sis_id(sis_course_id, sis_field='course'), sis_user_id)
    return self._get_resource(url)