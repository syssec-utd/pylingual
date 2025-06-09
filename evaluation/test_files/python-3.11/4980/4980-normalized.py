def issue(self, issue_id):
    """Get the issue data by its ID"""
    path = urijoin('bugs', str(issue_id))
    url_issue = self.__get_url(path)
    raw_text = self.__send_request(url_issue)
    return raw_text