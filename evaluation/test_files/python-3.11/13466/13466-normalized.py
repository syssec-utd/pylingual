def add_operator(self, operator):
    """Add an ``Operator`` to the ``Expression``.

        The ``Operator`` may result in a new ``Expression`` if an ``Operator``
        already exists and is of a different precedence.

        There are three possibilities when adding an ``Operator`` to an
        ``Expression`` depending on whether or not an ``Operator`` already
        exists:

          - No ``Operator`` on the working ``Expression``; Simply set the
            ``Operator`` and return ``self``.
          - ``Operator`` already exists and is higher in precedence; The
            ``Operator`` and last ``Constraint`` belong in a sub-expression of
            the working ``Expression``.
          - ``Operator`` already exists and is lower in precedence; The
            ``Operator`` belongs to the parent of the working ``Expression``
            whether one currently exists or not. To remain in the context of
            the top ``Expression``, this method will return the parent here
            rather than ``self``.

        Args:
            operator (Operator): What we are adding.

        Returns:
            Expression: ``self`` or related ``Expression``.

        Raises:
            FiqlObjectExpression: Operator is not a valid ``Operator``.
        """
    if not isinstance(operator, Operator):
        raise FiqlObjectException('%s is not a valid element type' % operator.__class__)
    if not self._working_fragment.operator:
        self._working_fragment.operator = operator
    elif operator > self._working_fragment.operator:
        last_constraint = self._working_fragment.elements.pop()
        self._working_fragment = self._working_fragment.create_nested_expression()
        self._working_fragment.add_element(last_constraint)
        self._working_fragment.add_operator(operator)
    elif operator < self._working_fragment.operator:
        if self._working_fragment.parent:
            return self._working_fragment.parent.add_operator(operator)
        else:
            return Expression().add_element(self._working_fragment).add_operator(operator)
    return self