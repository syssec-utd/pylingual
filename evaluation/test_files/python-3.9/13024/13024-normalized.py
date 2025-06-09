def get_enrollments_for_regid(self, regid, params={}, include_courses=True):
    """
        Return a list of enrollments for the passed user regid.

        https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index
        """
    sis_user_id = self._sis_id(regid, sis_field='user')
    url = USERS_API.format(sis_user_id) + '/enrollments'
    courses = Courses() if include_courses else None
    enrollments = []
    for datum in self._get_paged_resource(url, params=params):
        enrollment = CanvasEnrollment(data=datum)
        if include_courses:
            course_id = datum['course_id']
            course = courses.get_course(course_id)
            if course.sis_course_id is not None:
                enrollment.course = course
                enrollment.course_url = course.course_url
                enrollment.course_name = course.name
                enrollment.sis_course_id = course.sis_course_id
        else:
            enrollment.course_url = re.sub('/users/\\d+$', '', enrollment.html_url)
        enrollments.append(enrollment)
    return enrollments