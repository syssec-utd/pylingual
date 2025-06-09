def _deprecated_register(self, py_class, to_om, om_cd, om_name, to_py=None):
    """
        This is a shorthand for:

           ``self.register_to_python(om_cd, om_name, to_py)``
           ``self.register_to_openmath(py_class, to_om)``
        """
    self.register_to_python(om_cd, om_name, to_py)
    self.register_to_openmath(py_class, to_om)