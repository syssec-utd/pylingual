def attach(self, filename=None, content_type=None, data=None, disposition=None, headers=None):
    """Adds an attachment to the message.

        :param filename: filename of attachment
        :param content_type: file mimetype
        :param data: the raw file data
        :param disposition: content-disposition (if any)
        """
    self.attachments.append(Attachment(filename, content_type, data, disposition, headers))