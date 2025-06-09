def get_checklists(self):
    """
        Get the checklists for this board. Returns a list of Checklist objects.
        """
    checklists = self.getChecklistsJson(self.base_uri)
    checklists_list = []
    for checklist_json in checklists:
        checklists_list.append(self.createChecklist(checklist_json))
    return checklists_list