def update_settings(self, integration_id, settings):
    """Updates settings for given integration."""
    (integration, created) = self.get_or_create(integration_id=integration_id)
    try:
        current_settings = json.loads(integration.settings)
    except ValueError:
        current_settings = {}
    current_settings.update(settings)
    integration.settings = json.dumps(current_settings)
    integration.save()