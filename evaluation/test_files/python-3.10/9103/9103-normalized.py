def reset_store(self):
    """
        Clears out the current store and gets a cookie. Set the cross site
        request forgery token for each subsequent request.

        :return: A response having cleared the current store.
        :rtype: requests.Response
        """
    response = self.__get('/Store/Reset')
    token = self.session.cookies['XSRF-TOKEN']
    self.session.headers.update({'X-XSRF-TOKEN': token})
    return response