def _get_remote_settle_modes(pn_link):
    """Return a map containing the settle modes as provided by the remote.
    Skip any default value.
    """
    modes = {}
    snd = pn_link.remote_snd_settle_mode
    if snd == proton.Link.SND_UNSETTLED:
        modes['snd-settle-mode'] = 'unsettled'
    elif snd == proton.Link.SND_SETTLED:
        modes['snd-settle-mode'] = 'settled'
    if pn_link.remote_rcv_settle_mode == proton.Link.RCV_SECOND:
        modes['rcv-settle-mode'] = 'second'
    return modes