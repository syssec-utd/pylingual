def get_courses_for_regid(self, regid, params={}):
    """
        Return a list of courses for the passed regid.

        https://canvas.instructure.com/doc/api/courses.html#method.courses.index
        """
    self._as_user = regid
    data = self._get_resource('/api/v1/courses', params=params)
    self._as_user = None
    courses = []
    for datum in data:
        if 'sis_course_id' in datum:
            courses.append(CanvasCourse(data=datum))
        else:
            courses.append(self.get_course(datum['id'], params))
    return courses