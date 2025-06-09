from __future__ import annotations
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from . import education_assignment, education_assignment_defaults, education_assignment_settings, education_category, education_course, education_external_source, education_school, education_term, education_user, entity, group, identity_set
from . import entity

class EducationClass(entity.Entity):

    def __init__(self) -> None:
        """
        Instantiates a new educationClass and sets the default values.
        """
        super().__init__()
        self._assignment_categories: Optional[List[education_category.EducationCategory]] = None
        self._assignment_defaults: Optional[education_assignment_defaults.EducationAssignmentDefaults] = None
        self._assignment_settings: Optional[education_assignment_settings.EducationAssignmentSettings] = None
        self._assignments: Optional[List[education_assignment.EducationAssignment]] = None
        self._class_code: Optional[str] = None
        self._course: Optional[education_course.EducationCourse] = None
        self._created_by: Optional[identity_set.IdentitySet] = None
        self._description: Optional[str] = None
        self._display_name: Optional[str] = None
        self._external_id: Optional[str] = None
        self._external_name: Optional[str] = None
        self._external_source: Optional[education_external_source.EducationExternalSource] = None
        self._external_source_detail: Optional[str] = None
        self._grade: Optional[str] = None
        self._group: Optional[group.Group] = None
        self._mail_nickname: Optional[str] = None
        self._members: Optional[List[education_user.EducationUser]] = None
        self.odata_type: Optional[str] = None
        self._schools: Optional[List[education_school.EducationSchool]] = None
        self._teachers: Optional[List[education_user.EducationUser]] = None
        self._term: Optional[education_term.EducationTerm] = None

    @property
    def assignment_categories(self) -> Optional[List[education_category.EducationCategory]]:
        """
        Gets the assignmentCategories property value. All categories associated with this class. Nullable.
        Returns: Optional[List[education_category.EducationCategory]]
        """
        return self._assignment_categories

    @assignment_categories.setter
    def assignment_categories(self, value: Optional[List[education_category.EducationCategory]]=None) -> None:
        """
        Sets the assignmentCategories property value. All categories associated with this class. Nullable.
        Args:
            value: Value to set for the assignment_categories property.
        """
        self._assignment_categories = value

    @property
    def assignment_defaults(self) -> Optional[education_assignment_defaults.EducationAssignmentDefaults]:
        """
        Gets the assignmentDefaults property value. Specifies class-level defaults respected by new assignments created in the class.
        Returns: Optional[education_assignment_defaults.EducationAssignmentDefaults]
        """
        return self._assignment_defaults

    @assignment_defaults.setter
    def assignment_defaults(self, value: Optional[education_assignment_defaults.EducationAssignmentDefaults]=None) -> None:
        """
        Sets the assignmentDefaults property value. Specifies class-level defaults respected by new assignments created in the class.
        Args:
            value: Value to set for the assignment_defaults property.
        """
        self._assignment_defaults = value

    @property
    def assignment_settings(self) -> Optional[education_assignment_settings.EducationAssignmentSettings]:
        """
        Gets the assignmentSettings property value. Specifies class-level assignments settings.
        Returns: Optional[education_assignment_settings.EducationAssignmentSettings]
        """
        return self._assignment_settings

    @assignment_settings.setter
    def assignment_settings(self, value: Optional[education_assignment_settings.EducationAssignmentSettings]=None) -> None:
        """
        Sets the assignmentSettings property value. Specifies class-level assignments settings.
        Args:
            value: Value to set for the assignment_settings property.
        """
        self._assignment_settings = value

    @property
    def assignments(self) -> Optional[List[education_assignment.EducationAssignment]]:
        """
        Gets the assignments property value. All assignments associated with this class. Nullable.
        Returns: Optional[List[education_assignment.EducationAssignment]]
        """
        return self._assignments

    @assignments.setter
    def assignments(self, value: Optional[List[education_assignment.EducationAssignment]]=None) -> None:
        """
        Sets the assignments property value. All assignments associated with this class. Nullable.
        Args:
            value: Value to set for the assignments property.
        """
        self._assignments = value

    @property
    def class_code(self) -> Optional[str]:
        """
        Gets the classCode property value. Class code used by the school to identify the class.
        Returns: Optional[str]
        """
        return self._class_code

    @class_code.setter
    def class_code(self, value: Optional[str]=None) -> None:
        """
        Sets the classCode property value. Class code used by the school to identify the class.
        Args:
            value: Value to set for the class_code property.
        """
        self._class_code = value

    @property
    def course(self) -> Optional[education_course.EducationCourse]:
        """
        Gets the course property value. The course property
        Returns: Optional[education_course.EducationCourse]
        """
        return self._course

    @course.setter
    def course(self, value: Optional[education_course.EducationCourse]=None) -> None:
        """
        Sets the course property value. The course property
        Args:
            value: Value to set for the course property.
        """
        self._course = value

    @property
    def created_by(self) -> Optional[identity_set.IdentitySet]:
        """
        Gets the createdBy property value. Entity who created the class
        Returns: Optional[identity_set.IdentitySet]
        """
        return self._created_by

    @created_by.setter
    def created_by(self, value: Optional[identity_set.IdentitySet]=None) -> None:
        """
        Sets the createdBy property value. Entity who created the class
        Args:
            value: Value to set for the created_by property.
        """
        self._created_by = value

    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode]=None) -> EducationClass:
        """
        Creates a new instance of the appropriate class based on discriminator value
        Args:
            parseNode: The parse node to use to read the discriminator value and create the object
        Returns: EducationClass
        """
        if parse_node is None:
            raise Exception('parse_node cannot be undefined')
        return EducationClass()

    @property
    def description(self) -> Optional[str]:
        """
        Gets the description property value. Description of the class.
        Returns: Optional[str]
        """
        return self._description

    @description.setter
    def description(self, value: Optional[str]=None) -> None:
        """
        Sets the description property value. Description of the class.
        Args:
            value: Value to set for the description property.
        """
        self._description = value

    @property
    def display_name(self) -> Optional[str]:
        """
        Gets the displayName property value. Name of the class.
        Returns: Optional[str]
        """
        return self._display_name

    @display_name.setter
    def display_name(self, value: Optional[str]=None) -> None:
        """
        Sets the displayName property value. Name of the class.
        Args:
            value: Value to set for the display_name property.
        """
        self._display_name = value

    @property
    def external_id(self) -> Optional[str]:
        """
        Gets the externalId property value. ID of the class from the syncing system.
        Returns: Optional[str]
        """
        return self._external_id

    @external_id.setter
    def external_id(self, value: Optional[str]=None) -> None:
        """
        Sets the externalId property value. ID of the class from the syncing system.
        Args:
            value: Value to set for the external_id property.
        """
        self._external_id = value

    @property
    def external_name(self) -> Optional[str]:
        """
        Gets the externalName property value. Name of the class in the syncing system.
        Returns: Optional[str]
        """
        return self._external_name

    @external_name.setter
    def external_name(self, value: Optional[str]=None) -> None:
        """
        Sets the externalName property value. Name of the class in the syncing system.
        Args:
            value: Value to set for the external_name property.
        """
        self._external_name = value

    @property
    def external_source(self) -> Optional[education_external_source.EducationExternalSource]:
        """
        Gets the externalSource property value. How this class was created. Possible values are: sis, manual.
        Returns: Optional[education_external_source.EducationExternalSource]
        """
        return self._external_source

    @external_source.setter
    def external_source(self, value: Optional[education_external_source.EducationExternalSource]=None) -> None:
        """
        Sets the externalSource property value. How this class was created. Possible values are: sis, manual.
        Args:
            value: Value to set for the external_source property.
        """
        self._external_source = value

    @property
    def external_source_detail(self) -> Optional[str]:
        """
        Gets the externalSourceDetail property value. The name of the external source this resources was generated from.
        Returns: Optional[str]
        """
        return self._external_source_detail

    @external_source_detail.setter
    def external_source_detail(self, value: Optional[str]=None) -> None:
        """
        Sets the externalSourceDetail property value. The name of the external source this resources was generated from.
        Args:
            value: Value to set for the external_source_detail property.
        """
        self._external_source_detail = value

    def get_field_deserializers(self) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from . import education_assignment, education_assignment_defaults, education_assignment_settings, education_category, education_course, education_external_source, education_school, education_term, education_user, entity, group, identity_set
        fields: Dict[str, Callable[[Any], None]] = {'assignments': lambda n: setattr(self, 'assignments', n.get_collection_of_object_values(education_assignment.EducationAssignment)), 'assignmentCategories': lambda n: setattr(self, 'assignment_categories', n.get_collection_of_object_values(education_category.EducationCategory)), 'assignmentDefaults': lambda n: setattr(self, 'assignment_defaults', n.get_object_value(education_assignment_defaults.EducationAssignmentDefaults)), 'assignmentSettings': lambda n: setattr(self, 'assignment_settings', n.get_object_value(education_assignment_settings.EducationAssignmentSettings)), 'classCode': lambda n: setattr(self, 'class_code', n.get_str_value()), 'course': lambda n: setattr(self, 'course', n.get_object_value(education_course.EducationCourse)), 'createdBy': lambda n: setattr(self, 'created_by', n.get_object_value(identity_set.IdentitySet)), 'description': lambda n: setattr(self, 'description', n.get_str_value()), 'displayName': lambda n: setattr(self, 'display_name', n.get_str_value()), 'externalId': lambda n: setattr(self, 'external_id', n.get_str_value()), 'externalName': lambda n: setattr(self, 'external_name', n.get_str_value()), 'externalSource': lambda n: setattr(self, 'external_source', n.get_enum_value(education_external_source.EducationExternalSource)), 'externalSourceDetail': lambda n: setattr(self, 'external_source_detail', n.get_str_value()), 'grade': lambda n: setattr(self, 'grade', n.get_str_value()), 'group': lambda n: setattr(self, 'group', n.get_object_value(group.Group)), 'mailNickname': lambda n: setattr(self, 'mail_nickname', n.get_str_value()), 'members': lambda n: setattr(self, 'members', n.get_collection_of_object_values(education_user.EducationUser)), 'schools': lambda n: setattr(self, 'schools', n.get_collection_of_object_values(education_school.EducationSchool)), 'teachers': lambda n: setattr(self, 'teachers', n.get_collection_of_object_values(education_user.EducationUser)), 'term': lambda n: setattr(self, 'term', n.get_object_value(education_term.EducationTerm))}
        super_fields = super().get_field_deserializers()
        fields.update(super_fields)
        return fields

    @property
    def grade(self) -> Optional[str]:
        """
        Gets the grade property value. Grade level of the class.
        Returns: Optional[str]
        """
        return self._grade

    @grade.setter
    def grade(self, value: Optional[str]=None) -> None:
        """
        Sets the grade property value. Grade level of the class.
        Args:
            value: Value to set for the grade property.
        """
        self._grade = value

    @property
    def group(self) -> Optional[group.Group]:
        """
        Gets the group property value. The underlying Microsoft 365 group object.
        Returns: Optional[group.Group]
        """
        return self._group

    @group.setter
    def group(self, value: Optional[group.Group]=None) -> None:
        """
        Sets the group property value. The underlying Microsoft 365 group object.
        Args:
            value: Value to set for the group property.
        """
        self._group = value

    @property
    def mail_nickname(self) -> Optional[str]:
        """
        Gets the mailNickname property value. Mail name for sending email to all members, if this is enabled.
        Returns: Optional[str]
        """
        return self._mail_nickname

    @mail_nickname.setter
    def mail_nickname(self, value: Optional[str]=None) -> None:
        """
        Sets the mailNickname property value. Mail name for sending email to all members, if this is enabled.
        Args:
            value: Value to set for the mail_nickname property.
        """
        self._mail_nickname = value

    @property
    def members(self) -> Optional[List[education_user.EducationUser]]:
        """
        Gets the members property value. All users in the class. Nullable.
        Returns: Optional[List[education_user.EducationUser]]
        """
        return self._members

    @members.setter
    def members(self, value: Optional[List[education_user.EducationUser]]=None) -> None:
        """
        Sets the members property value. All users in the class. Nullable.
        Args:
            value: Value to set for the members property.
        """
        self._members = value

    @property
    def schools(self) -> Optional[List[education_school.EducationSchool]]:
        """
        Gets the schools property value. All schools that this class is associated with. Nullable.
        Returns: Optional[List[education_school.EducationSchool]]
        """
        return self._schools

    @schools.setter
    def schools(self, value: Optional[List[education_school.EducationSchool]]=None) -> None:
        """
        Sets the schools property value. All schools that this class is associated with. Nullable.
        Args:
            value: Value to set for the schools property.
        """
        self._schools = value

    def serialize(self, writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        Args:
            writer: Serialization writer to use to serialize this model
        """
        if writer is None:
            raise Exception('writer cannot be undefined')
        super().serialize(writer)
        writer.write_collection_of_object_values('assignments', self.assignments)
        writer.write_collection_of_object_values('assignmentCategories', self.assignment_categories)
        writer.write_object_value('assignmentDefaults', self.assignment_defaults)
        writer.write_object_value('assignmentSettings', self.assignment_settings)
        writer.write_str_value('classCode', self.class_code)
        writer.write_object_value('course', self.course)
        writer.write_object_value('createdBy', self.created_by)
        writer.write_str_value('description', self.description)
        writer.write_str_value('displayName', self.display_name)
        writer.write_str_value('externalId', self.external_id)
        writer.write_str_value('externalName', self.external_name)
        writer.write_enum_value('externalSource', self.external_source)
        writer.write_str_value('externalSourceDetail', self.external_source_detail)
        writer.write_str_value('grade', self.grade)
        writer.write_object_value('group', self.group)
        writer.write_str_value('mailNickname', self.mail_nickname)
        writer.write_collection_of_object_values('members', self.members)
        writer.write_collection_of_object_values('schools', self.schools)
        writer.write_collection_of_object_values('teachers', self.teachers)
        writer.write_object_value('term', self.term)

    @property
    def teachers(self) -> Optional[List[education_user.EducationUser]]:
        """
        Gets the teachers property value. All teachers in the class. Nullable.
        Returns: Optional[List[education_user.EducationUser]]
        """
        return self._teachers

    @teachers.setter
    def teachers(self, value: Optional[List[education_user.EducationUser]]=None) -> None:
        """
        Sets the teachers property value. All teachers in the class. Nullable.
        Args:
            value: Value to set for the teachers property.
        """
        self._teachers = value

    @property
    def term(self) -> Optional[education_term.EducationTerm]:
        """
        Gets the term property value. Term for this class.
        Returns: Optional[education_term.EducationTerm]
        """
        return self._term

    @term.setter
    def term(self, value: Optional[education_term.EducationTerm]=None) -> None:
        """
        Sets the term property value. Term for this class.
        Args:
            value: Value to set for the term property.
        """
        self._term = value