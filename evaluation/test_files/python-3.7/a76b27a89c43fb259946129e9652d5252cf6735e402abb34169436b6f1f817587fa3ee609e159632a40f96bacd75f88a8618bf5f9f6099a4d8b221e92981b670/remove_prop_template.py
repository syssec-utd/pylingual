import ifcopenshell.util.element

class Usecase:

    def __init__(self, file, prop_template=None):
        """Removes a property template

        Note that a property set template should always have at least one
        property template to be valid, so take care when removing property
        templates.

        :param prop_template: The IfcSimplePropertyTemplate to remove.
        :type prop_template: ifcopenshell.entity_instance.entity_instance
        :return: None
        :rtype: None

        Example:

        .. code:: python

            template = ifcopenshell.api.run("pset_template.add_pset_template", model, name="ABC_RiskFactors")

            # Here's two propertes with just default values.
            prop1 = ifcopenshell.api.run("pset_template.add_prop_template", model, pset_template=template)
            prop2 = ifcopenshell.api.run("pset_template.add_prop_template", model, pset_template=template)

            # Let's remove the second one.
            ifcopenshell.api.run("pset_template.remove_prop_template", model, prop_template=prop2)
        """
        self.file = file
        self.settings = {'prop_template': prop_template}

    def execute(self):
        for inverse in self.file.get_inverse(self.settings['prop_template']):
            if len(inverse.HasPropertyTemplates) == 1:
                inverse.HasPropertyTemplates = []
            else:
                has_property_templates = list(inverse.HasPropertyTemplates)
                has_property_templates.remove(self.settings['prop_template'])
                inverse.HasPropertyTemplates = has_property_templates
        ifcopenshell.util.element.remove_deep(self.file, self.settings['prop_template'])