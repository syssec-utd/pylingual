def _do_not_produce_file(self):
    """
        Check if we are allowed to produce a file based from the given
        information.

        :return:
            The state of the production.
            True: We do not produce file.
            False: We do produce file.
        :rtype: bool
        """
    if Inactive().is_present() and self.domain_status in [PyFunceble.STATUS['official']['down'], PyFunceble.STATUS['official']['invalid']] and (PyFunceble.INTERN['to_test'] not in PyFunceble.INTERN['extracted_list_to_test']):
        return True
    return False