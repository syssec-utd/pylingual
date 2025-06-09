def poke(self, context):
    """
        Pokes for a mail attachment on the mail server.

        :param context: The context that is being provided when poking.
        :type context: dict
        :return: True if attachment with the given name is present and False if not.
        :rtype: bool
        """
    self.log.info('Poking for %s', self.attachment_name)
    with ImapHook(imap_conn_id=self.conn_id) as imap_hook:
        return imap_hook.has_mail_attachment(name=self.attachment_name, mail_folder=self.mail_folder, check_regex=self.check_regex)