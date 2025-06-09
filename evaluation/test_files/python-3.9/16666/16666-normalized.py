def has_quorum(self):
    """
        we've seen +2/3 of all eligible votes voting for one block.
        there is a quorum.
        """
    assert self.is_valid
    bhs = self.blockhashes()
    if bhs and bhs[0][1] > 2 / 3.0 * self.num_eligible_votes:
        return bhs[0][0]