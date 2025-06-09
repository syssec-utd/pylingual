def content_url(url: str, content_type: str, name: str=None, text: str=None, speak: str=None, input_hint: Union[InputHints, str]=None):
    """
        Returns a message that will display a single image or video to a user.

        :Example:
        message = MessageFactory.content_url('https://example.com/hawaii.jpg', 'image/jpeg',
                                             'Hawaii Trip', 'A photo from our family vacation.')
        await context.send_activity(message)

        :param url:
        :param content_type:
        :param name:
        :param text:
        :param speak:
        :param input_hint:
        :return:
        """
    attachment = Attachment(content_type=content_type, content_url=url)
    if name:
        attachment.name = name
    return attachment_activity(AttachmentLayoutTypes.list, [attachment], text, speak, input_hint)