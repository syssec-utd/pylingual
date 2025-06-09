def f_get(self, *args):
    """Returns items handled by the result.

         If only a single name is given, a single data item is returned. If several names are
         given, a list is returned. For integer inputs the result returns `resultname_X`.

         If the result contains only a single entry you can call `f_get()` without arguments.
         If you call `f_get()` and the result contains more than one element a ValueError is
         thrown.

         If the requested item(s) cannot be found an AttributeError is thrown.

        :param args: strings-names or integers

        :return: Single data item or tuple of data

        Example:

        >>> res = Result('supergroup.subgroup.myresult', comment='I am a neat example!'         [1000,2000], {'a':'b','c':333}, hitchhiker='Arthur Dent')
        >>> res.f_get('hitchhiker')
        'Arthur Dent'
        >>> res.f_get(0)
        [1000,2000]
        >>> res.f_get('hitchhiker', 'myresult')
        ('Arthur Dent', [1000,2000])

        """
    if len(args) == 0:
        if len(self._data) == 1:
            return list(self._data.values())[0]
        elif len(self._data) > 1:
            raise ValueError('Your result `%s` contains more than one entry: `%s` Please use >>f_get<< with one of these.' % (self.v_full_name, str(list(self._data.keys()))))
        else:
            raise AttributeError('Your result `%s` is empty, cannot access data.' % self.v_full_name)
    result_list = []
    for name in args:
        name = self.f_translate_key(name)
        if not name in self._data:
            if name == 'data' and len(self._data) == 1:
                return self._data[list(self._data.keys())[0]]
            else:
                raise AttributeError('`%s` is not part of your result `%s`.' % (name, self.v_full_name))
        result_list.append(self._data[name])
    if len(args) == 1:
        return result_list[0]
    else:
        return result_list