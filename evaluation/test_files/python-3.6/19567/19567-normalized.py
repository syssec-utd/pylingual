def get_comment_lesson_info(self):
    """
        获取教学评估内所有需要课程

        :return: 返回所以有需要进行教学评估的课程
        :rtype: list
        """
    echo = self._echo
    response = self._post('http://bkjws.sdu.edu.cn/b/pg/xs/list', data=self._aodata(echo, ['kch', 'kcm', 'jsm', 'function', 'function']))
    if self._check_response(response, echo=echo):
        return response['object']['aaData']
    else:
        self._unexpected(response)