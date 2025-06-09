"""
    Copyright 2017 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""
from typing import List, Optional, Set, Tuple
from inmanta.ast import CompilerException, Locatable, Location, RuntimeException, TypingException
from inmanta.ast.type import NullableType, TypedList
from inmanta.execute import runtime
from inmanta.execute.util import Unknown
from inmanta.stable_api import stable_api
try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False
if TYPE_CHECKING:
    from inmanta.ast.entity import Entity
    from inmanta.ast.type import Type
    from inmanta.execute.runtime import Instance

@stable_api
class Attribute(Locatable):
    """
    The attribute base class for entity attributes.

    :param entity: The entity this attribute belongs to
    """

    def __init__(self, entity: 'Entity', value_type: 'Type', name: str, location: Location, multi: bool=False, nullable: bool=False) -> None:
        Locatable.__init__(self)
        self.location = location
        self.__name: str = name
        entity.add_attribute(self)
        self.__entity = entity
        self.__multi = multi
        self.__nullable = nullable
        self.__type: Type = value_type
        if multi:
            self.__type = TypedList(self.__type)
        if nullable:
            self.__type = NullableType(self.__type)
        self.comment = None
        self.end: Optional[RelationAttribute] = None

    def get_type(self) -> 'Type':
        """
        Get the type of this attribute.
        """
        return self.__type
    type: 'Type' = property(get_type)

    def get_name(self) -> str:
        """
        Get the name of the attribute. This is the name this attribute
        is associated with in the entity.
        """
        return self.__name
    name = property(get_name)

    def __hash__(self) -> 'int':
        """
        The hash of this object is based on the name of the attribute
        """
        return hash(self.__name)

    def __repr__(self) -> str:
        return self.__name

    def get_entity(self) -> 'Entity':
        """
        Return the entity this attribute belongs to
        """
        return self.__entity
    entity = property(get_entity)

    def validate(self, value: object) -> None:
        """
        Validate a value that is going to be assigned to this attribute. Raises a :py:class:`inmanta.ast.RuntimeException`
        if validation fails.
        """
        if isinstance(value, Unknown):
            return
        self.type.validate(value)

    def get_new_result_variable(self, instance: 'Instance', queue: 'runtime.QueueScheduler') -> 'runtime.ResultVariable':
        out: runtime.ResultVariable[object] = runtime.ResultVariable()
        out.set_type(self.type)
        return out

    def is_optional(self) -> bool:
        """
        Returns true iff this attribute accepts null values.
        Deprecated but still used internally.
        """
        return self.__nullable

    def is_multi(self) -> bool:
        """
        Returns true iff this attribute expects a list of values of its base type.
        Deprecated but still used internally.
        """
        return self.__multi

    def final(self, excns: List[CompilerException]) -> None:
        pass

    def has_relation_precedence_rules(self) -> bool:
        """
        Return true iff a relation precedence rule exists that defines that this Attribute should
        be frozen before another Attribute.
        """
        return False

@stable_api
class RelationAttribute(Attribute):
    """
    An attribute that is a relation
    """

    def __init__(self, entity: 'Entity', value_type: 'Type', name: str, location: Location) -> None:
        """
        :ivar freeze_dependents: Contains the set of RelationAttributes that can only be frozen
                                 once this attribute is frozen.
        """
        Attribute.__init__(self, entity, value_type, name, location)
        self.end: Optional[RelationAttribute] = None
        self.low = 1
        self.high = 1
        self.depends = False
        self.source_annotations = []
        self.target_annotations = []
        self.freeze_dependents: Set[RelationAttribute] = set()

    def __str__(self) -> str:
        return '%s.%s' % (self.get_entity().get_full_name(), self.name)

    def __repr__(self) -> str:
        return '[%d:%s] %s' % (self.low, self.high if self.high is not None else '', self.name)

    def set_multiplicity(self, values: 'Tuple[int, Optional[int]]') -> None:
        """
        Set the multiplicity of this end
        """
        self.low = values[0]
        self.high = values[1]

    def get_new_result_variable(self, instance: 'Instance', queue: 'runtime.QueueScheduler') -> 'runtime.ResultVariable':
        out: runtime.ResultVariable
        if self.low == 1 and self.high == 1:
            out = runtime.AttributeVariable(self, instance)
        elif self.low == 0 and self.high == 1:
            out = runtime.OptionVariable(self, instance, queue)
        else:
            out = runtime.ListVariable(self, instance, queue)
        out.set_type(self.type)
        return out

    def is_optional(self) -> bool:
        return self.low == 0

    def is_multi(self) -> bool:
        return self.high != 1

    def final(self, excns: List[CompilerException]) -> None:
        for rv in self.source_annotations:
            try:
                if isinstance(rv.get_value(), Unknown):
                    excns.append(TypingException(self, 'Relation annotation can not be Unknown'))
            except RuntimeException as e:
                excns.append(e)
        for rv in self.target_annotations:
            try:
                if isinstance(rv.get_value(), Unknown):
                    excns.append(TypingException(self, 'Relation annotation can not be Unknown'))
            except RuntimeException as e:
                excns.append(e)

    def add_freeze_dependent(self, successor: 'RelationAttribute') -> None:
        """
        Attach a constraint to this RelationAttribute that this RelationAttribute should
        be frozen before `successor`.
        """
        self.freeze_dependents.add(successor)

    def has_relation_precedence_rules(self) -> bool:
        """
        Return true iff a relation precedence rule exists that defines that this Attribute should
        be frozen before another Attribute.
        """
        return bool(self.freeze_dependents)