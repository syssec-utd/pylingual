def _build_common_attributes(self, operation_policy_name=None):
    """
         Build a list of common attributes that are shared across
         symmetric as well as asymmetric objects
        """
    common_attributes = []
    if operation_policy_name:
        common_attributes.append(self.attribute_factory.create_attribute(enums.AttributeType.OPERATION_POLICY_NAME, operation_policy_name))
    return common_attributes