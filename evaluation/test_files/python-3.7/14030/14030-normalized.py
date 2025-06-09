def instance_method(self, imeth: typing.Optional[typing.Callable[..., typing.Any]]) -> 'SeparateClassMethod':
    """Descriptor to change instance method.

        :param imeth: New instance method.
        :type imeth: typing.Optional[typing.Callable]
        :return: SeparateClassMethod
        :rtype: SeparateClassMethod
        """
    self.__instance_method = imeth
    return self