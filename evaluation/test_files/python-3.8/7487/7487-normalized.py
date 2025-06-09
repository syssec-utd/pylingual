def get_team(self, name):
    """**Description**
            Return the team with the specified team name, if it is present.

        **Arguments**
            - **name**: the name of the team to return

        **Success Return Value**
            The requested team.

        **Example**
            `examples/user_team_mgmt.py <https://github.com/draios/python-sdc-client/blob/master/examples/user_team_mgmt.py>`_
        """
    res = self.get_teams(name)
    if res[0] == False:
        return res
    for t in res[1]:
        if t['name'] == name:
            return [True, t]
    return [False, 'Could not find team']