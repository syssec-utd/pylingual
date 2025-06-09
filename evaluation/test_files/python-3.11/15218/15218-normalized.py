def setLCDCmd(self, display_list, password='00000000'):
    """ Single call wrapper for LCD set."

        Wraps :func:`~ekmmeters.V4Meter.setLcd` and associated init and add methods.

        Args:
            display_list (list): List composed of :class:`~ekmmeters.LCDItems`
            password (str): Optional password.

        Returns:
            bool: Passthrough from :func:`~ekmmeters.V4Meter.setLcd`
        """
    result = False
    try:
        self.initLcd()
        item_cnt = len(display_list)
        if item_cnt > 45 or item_cnt <= 0:
            ekm_log('LCD item list must have between 1 and 40 items')
            return False
        for display_item in display_list:
            self.addLcdItem(int(display_item))
        result = self.setLCD(password)
    except:
        ekm_log(traceback.format_exc(sys.exc_info()))
    return result