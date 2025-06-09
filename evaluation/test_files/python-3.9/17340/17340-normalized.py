def _add_header(self):
    """Add email header info."""
    self.message['From'] = self.from_
    self.message['Subject'] = self.subject
    if self.to:
        self.message['To'] = self.list_to_string(self.to)
    if self.cc:
        self.message['Cc'] = self.list_to_string(self.cc)
    if self.bcc:
        self.message['Bcc'] = self.list_to_string(self.bcc)