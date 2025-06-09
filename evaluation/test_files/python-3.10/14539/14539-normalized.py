def get_checklists(self, **query_params):
    """
        Get the checklists for this card. Returns a list of Checklist objects.

        Returns:
            list(Checklist): The checklists attached to this card
        """
    checklists = self.get_checklist_json(self.base_uri, query_params=query_params)
    checklists_list = []
    for checklist_json in checklists:
        checklists_list.append(self.create_checklist(checklist_json))
    return checklists_list