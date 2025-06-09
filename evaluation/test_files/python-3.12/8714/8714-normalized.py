def get_short_uid_dict(self, query=None):
    """Create a dictionary of shortend UIDs for all contacts.

        All arguments are only used if the address book is not yet initialized
        and will just be handed to self.load().

        :param query: see self.load()
        :type query: str
        :returns: the contacts mapped by the shortes unique prefix of their UID
        :rtype: dict(str: CarddavObject)
        """
    if self._short_uids is None:
        if not self._loaded:
            self.load(query)
        if not self.contacts:
            self._short_uids = {}
        elif len(self.contacts) == 1:
            self._short_uids = {uid[0:1]: contact for uid, contact in self.contacts.items()}
        else:
            self._short_uids = {}
            sorted_uids = sorted(self.contacts)
            item0, item1 = sorted_uids[:2]
            same1 = self._compare_uids(item0, item1)
            self._short_uids[item0[:same1 + 1]] = self.contacts[item0]
            for item_new in sorted_uids[2:]:
                item0, item1 = (item1, item_new)
                same0, same1 = (same1, self._compare_uids(item0, item1))
                same = max(same0, same1)
                self._short_uids[item0[:same + 1]] = self.contacts[item0]
            self._short_uids[item1[:same1 + 1]] = self.contacts[item1]
    return self._short_uids