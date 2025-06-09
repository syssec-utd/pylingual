def __fetch_merge_requests(self, from_date):
    """Fetch the merge requests"""
    merges_groups = self.client.merges(from_date=from_date)
    for raw_merges in merges_groups:
        merges = json.loads(raw_merges)
        for merge in merges:
            merge_id = merge['iid']
            if self.blacklist_ids and merge_id in self.blacklist_ids:
                logger.warning('Skipping blacklisted merge request %s', merge_id)
                continue
            merge_full_raw = self.client.merge(merge_id)
            merge_full = json.loads(merge_full_raw)
            self.__init_merge_extra_fields(merge_full)
            merge_full['notes_data'] = self.__get_merge_notes(merge_id)
            merge_full['award_emoji_data'] = self.__get_award_emoji(GitLabClient.MERGES, merge_id)
            merge_full['versions_data'] = self.__get_merge_versions(merge_id)
            yield merge_full