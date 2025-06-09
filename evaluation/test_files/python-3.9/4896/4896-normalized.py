def __get_issue_notes(self, issue_id):
    """Get issue notes"""
    notes = []
    group_notes = self.client.notes(GitLabClient.ISSUES, issue_id)
    for raw_notes in group_notes:
        for note in json.loads(raw_notes):
            note_id = note['id']
            note['award_emoji_data'] = self.__get_note_award_emoji(GitLabClient.ISSUES, issue_id, note_id)
            notes.append(note)
    return notes