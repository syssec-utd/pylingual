def register_messages_from_checker(self, checker):
    """Register all messages from a checker.

        :param BaseChecker checker:
        """
    checker.check_consistency()
    for message in checker.messages:
        self.register_message(message)