from epyk.core.html.options import Enums

class ExtsValidators(Enums):

    def custom(self, validator, module_alias):
        """
    Description:
    -----------

    Related Pages:

      http://tabulator.info/docs/4.0/mutators

    Attributes:
    ----------
    :param validator:
    :param module_alias:
    """
        self.component.jsImports.add(module_alias)
        self._set_value(value=validator)
        return self