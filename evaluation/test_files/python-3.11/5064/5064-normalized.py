def __get_pull_review_comments(self, pr_number):
    """Get pull request review comments"""
    comments = []
    group_comments = self.client.pull_review_comments(pr_number)
    for raw_comments in group_comments:
        for comment in json.loads(raw_comments):
            comment_id = comment.get('id')
            user = comment.get('user', None)
            if not user:
                logger.warning('Missing user info for %s', comment['url'])
                comment['user_data'] = None
            else:
                comment['user_data'] = self.__get_user(user['login'])
            comment['reactions_data'] = self.__get_pull_review_comment_reactions(comment_id, comment['reactions']['total_count'])
            comments.append(comment)
    return comments