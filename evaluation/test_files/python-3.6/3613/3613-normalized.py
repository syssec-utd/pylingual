def list(attachments: List[Attachment], text: str=None, speak: str=None, input_hint: Union[InputHints, str]=None) -> Activity:
    """
        Returns a message that will display a set of attachments in list form.

        :Example:
        message = MessageFactory.list([CardFactory.hero_card(HeroCard(title='title1',
                                                             images=[CardImage(url='imageUrl1')],
                                                             buttons=[CardAction(title='button1')])),
                                       CardFactory.hero_card(HeroCard(title='title2',
                                                             images=[CardImage(url='imageUrl2')],
                                                             buttons=[CardAction(title='button2')])),
                                       CardFactory.hero_card(HeroCard(title='title3',
                                                             images=[CardImage(url='imageUrl3')],
                                                             buttons=[CardAction(title='button3')]))])
        await context.send_activity(message)

        :param attachments:
        :param text:
        :param speak:
        :param input_hint:
        :return:
        """
    return attachment_activity(AttachmentLayoutTypes.list, attachments, text, speak, input_hint)