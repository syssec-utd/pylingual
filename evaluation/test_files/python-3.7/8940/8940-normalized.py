def check_and_adjust_sighandlers(self):
    """Check to see if any of the signal handlers we are interested in have
        changed or is not initially set. Change any that are not right. """
    for signame in list(self.sigs.keys()):
        if not self.check_and_adjust_sighandler(signame, self.sigs):
            break
        pass
    return