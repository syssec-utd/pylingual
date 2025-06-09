def formatmonthname(self, theyear, themonth, withyear=True):
    """
        Change colspan to "5", add "today" button, and return a month
        name as a table row.
        """
    display_month = month_name[themonth]
    if isinstance(display_month, six.binary_type) and self.encoding:
        display_month = display_month.decode(self.encoding)
    if withyear:
        s = u'%s %s' % (display_month, theyear)
    else:
        s = u'%s' % display_month
    return '<tr><th colspan="5" class="month"><button id="cal-today-btn" class="btn btn-small">Today</button> %s</th></tr>' % s