def list_memberships(self, team):
    """
        **Description**
            List all memberships for specified team.

        **Arguments**
            - **team**: the name of the team for which we want to see memberships

        **Result**
            Dictionary of (user-name, team-role) pairs that should describe memberships of the team.

        **Example**
            `examples/user_team_mgmt_extended.py <https://github.com/draios/python-sdc-client/blob/master/examples/user_team_mgmt_extended.py>`_
        """
    res = self.get_team(team)
    if res[0] == False:
        return res
    raw_memberships = res[1]['userRoles']
    user_ids = [m['userId'] for m in raw_memberships]
    res = self._get_id_user_dict(user_ids)
    if res[0] == False:
        return [False, 'Could not fetch IDs for user names']
    else:
        id_user_dict = res[1]
    return [True, dict([(id_user_dict[m['userId']], m['role']) for m in raw_memberships])]