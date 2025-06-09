def _convert_or_shorten_month(cls, data):
    """
        Convert a given month into our unified format.

        :param data: The month to convert or shorten.
        :type data: str

        :return: The unified month name.
        :rtype: str
        """
    short_month = {'jan': [str(1), '01', 'Jan', 'January'], 'feb': [str(2), '02', 'Feb', 'February'], 'mar': [str(3), '03', 'Mar', 'March'], 'apr': [str(4), '04', 'Apr', 'April'], 'may': [str(5), '05', 'May'], 'jun': [str(6), '06', 'Jun', 'June'], 'jul': [str(7), '07', 'Jul', 'July'], 'aug': [str(8), '08', 'Aug', 'August'], 'sep': [str(9), '09', 'Sep', 'September'], 'oct': [str(10), 'Oct', 'October'], 'nov': [str(11), 'Nov', 'November'], 'dec': [str(12), 'Dec', 'December']}
    for month in short_month:
        if data in short_month[month]:
            return month
    return data