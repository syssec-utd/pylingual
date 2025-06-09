def get_service_metadata(self):
    """
        Return extra config options to be passed to the TrelloIssue class
        """
    return {'import_labels_as_tags': self.config.get('import_labels_as_tags', False, asbool), 'label_template': self.config.get('label_template', DEFAULT_LABEL_TEMPLATE)}