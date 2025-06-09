def get_course(self, course_id, params={}):
    """
        Return course resource for given canvas course id.

        https://canvas.instructure.com/doc/api/courses.html#method.courses.show
        """
    include = params.get('include', [])
    if 'term' not in include:
        include.append('term')
    params['include'] = include
    url = COURSES_API.format(course_id)
    return CanvasCourse(data=self._get_resource(url, params=params))