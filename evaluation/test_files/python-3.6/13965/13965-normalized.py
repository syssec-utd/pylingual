def dismiss_prompt(self, text=None, wait=None):
    """
        Execute the wrapped code, dismissing a prompt.

        Args:
            text (str | RegexObject, optional): Text to match against the text in the modal.
            wait (int | float, optional): Maximum time to wait for the modal to appear after
                executing the wrapped code.

        Raises:
            ModalNotFound: If a modal dialog hasn't been found.
        """
    with self.driver.dismiss_modal('prompt', text=text, wait=wait):
        yield