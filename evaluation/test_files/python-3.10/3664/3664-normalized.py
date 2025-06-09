async def reprompt_dialog(self):
    """
        Calls reprompt on the currently active dialog, if there is one. Used with Prompts that have a reprompt behavior.
        :return:
        """
    if self.active_dialog != None:
        dialog = await self.find_dialog(self.active_dialog.id)
        if not dialog:
            raise Exception("DialogSet.reprompt_dialog(): Can't find A dialog with an id of '%s'." % self.active_dialog.id)
        await dialog.reprompt_dialog(self.context, self.active_dialog)