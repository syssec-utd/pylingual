def splitEkmDate(dateint):
    """Break out a date from Omnimeter read.

        Note a corrupt date will raise an exception when you
        convert it to int to hand to this method.

        Args:
            dateint (int):  Omnimeter datetime as int.

        Returns:
            tuple: Named tuple which breaks out as followws:

            ========== =====================
            yy         Last 2 digits of year
            mm         Month 1-12
            dd         Day 1-31
            weekday    Zero based weekday
            hh         Hour 0-23
            minutes    Minutes 0-59
            ss         Seconds 0-59
            ========== =====================

        """
    date_str = str(dateint)
    dt = namedtuple('EkmDate', ['yy', 'mm', 'dd', 'weekday', 'hh', 'minutes', 'ss'])
    if len(date_str) != 14:
        dt.yy = dt.mm = dt.dd = dt.weekday = dt.hh = dt.minutes = dt.ss = 0
        return dt
    dt.yy = int(date_str[0:2])
    dt.mm = int(date_str[2:4])
    dt.dd = int(date_str[4:6])
    dt.weekday = int(date_str[6:8])
    dt.hh = int(date_str[8:10])
    dt.minutes = int(date_str[10:12])
    dt.ss = int(date_str[12:14])
    return dt