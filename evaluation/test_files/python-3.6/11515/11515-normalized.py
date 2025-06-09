def add_pending(self, panel_obj, hgnc_gene, action, info=None):
    """Add a pending action to a gene panel

        Store the pending actions in panel.pending

        Args:
            panel_obj(dict): The panel that is about to be updated
            hgnc_gene(dict)
            action(str): choices=['add','delete','edit']
            info(dict): additional gene info (disease_associated_transcripts,
                        reduced_penetrance, mosaicism, database_entry_version ,
                        inheritance_models, comment)

        Returns:
            updated_panel(dict):

        """
    valid_actions = ['add', 'delete', 'edit']
    if action not in valid_actions:
        raise ValueError('Invalid action {0}'.format(action))
    info = info or {}
    pending_action = {'hgnc_id': hgnc_gene['hgnc_id'], 'action': action, 'info': info, 'symbol': hgnc_gene['hgnc_symbol']}
    updated_panel = self.panel_collection.find_one_and_update({'_id': panel_obj['_id']}, {'$addToSet': {'pending': pending_action}}, return_document=pymongo.ReturnDocument.AFTER)
    return updated_panel