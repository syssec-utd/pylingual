def get_cards(self, list_id):
    """ Returns an iterator for the cards in a given list, filtered
        according to configuration values of trello.only_if_assigned and
        trello.also_unassigned """
    params = {'fields': 'name,idShort,shortLink,shortUrl,url,labels,due'}
    member = self.config.get('only_if_assigned', None)
    unassigned = self.config.get('also_unassigned', False, asbool)
    if member is not None:
        params['members'] = 'true'
        params['member_fields'] = 'username'
    cards = self.api_request('/1/lists/{list_id}/cards/open'.format(list_id=list_id), **params)
    for card in cards:
        if member is None or member in [m['username'] for m in card['members']] or (unassigned and (not card['members'])):
            yield card