def content(cls):
    """
        Get the content of the database.

        :return: The content of the database.
        :rtype: list
        """
    result = []
    if PyFunceble.CONFIGURATION['inactive_database'] and PyFunceble.INTERN['inactive_db']:
        for key in PyFunceble.INTERN['inactive_db'][PyFunceble.INTERN['file_to_test']]:
            if key == 'to_test':
                continue
            result.extend(PyFunceble.INTERN['inactive_db'][PyFunceble.INTERN['file_to_test']][key])
    return result