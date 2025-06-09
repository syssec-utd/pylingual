def validate_votes(self, validators_H, validators_prevH):
    """set of validators may change between heights"""
    assert self.sender

    def check(lockset, validators):
        if not lockset.num_eligible_votes == len(validators):
            raise InvalidProposalError('lockset num_eligible_votes mismatch')
        for v in lockset:
            if v.sender not in validators:
                raise InvalidProposalError('invalid signer')
    if self.round_lockset:
        check(self.round_lockset, validators_H)
    check(self.signing_lockset, validators_prevH)
    return True