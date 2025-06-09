def f_get_explored_parameters(self, fast_access=False, copy=True):
    """ Returns a dictionary containing the full parameter names as keys and the parameters
         or the parameter data items as values.

         IMPORTANT: This dictionary always contains all explored parameters as keys.
         Even when they are not loaded, in this case the value is simply `None`.
         `fast_access` only works if all explored parameters are loaded.


        :param fast_access:

            Determines whether the parameter objects or their values are returned
            in the dictionary.

        :param copy:

            Whether the original dictionary or a shallow copy is returned.
            If you want the real dictionary please do not modify it at all!
            Not Copying and fast access do not work at the same time! Raises ValueError
            if fast access is true and copy false.

        :return: Dictionary containing the parameters.

        :raises: ValueError

        """
    return self._return_item_dictionary(self._explored_parameters, fast_access, copy)