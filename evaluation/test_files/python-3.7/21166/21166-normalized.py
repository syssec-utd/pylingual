def object_info(self, oname, detail_level=0):
    """Get metadata information about an object.

        Parameters
        ----------
        oname : str
            A string specifying the object name.
        detail_level : int, optional
            The level of detail for the introspection (0-2)

        Returns
        -------
        The msg_id of the message sent.
        """
    content = dict(oname=oname, detail_level=detail_level)
    msg = self.session.msg('object_info_request', content)
    self._queue_send(msg)
    return msg['header']['msg_id']