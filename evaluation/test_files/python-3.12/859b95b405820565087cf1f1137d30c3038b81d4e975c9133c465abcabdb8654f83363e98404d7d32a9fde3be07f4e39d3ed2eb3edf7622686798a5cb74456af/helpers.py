from dataclasses import dataclass
from enum import auto
from typing import List, Optional, TYPE_CHECKING, Union
from mstrio.utils.enum_helper import AutoName
from mstrio.utils.helper import Dictable, exception_handler
if TYPE_CHECKING:
    from mstrio.modeling.schema import UserHierarchy
    from mstrio.modeling.schema.attribute import Attribute
    from mstrio.modeling.schema.helpers import SchemaObjectReference
    from mstrio.connection import Connection

class ObjectSubType(AutoName):
    """String literal used to identify the type of a metadata object.
    Some MicroStrategy APIs make a distinction between an object's type
    and subtype because in some cases (e.g. the different kinds of reports)
    it can be useful to see one "report" concept rather than to have to always
    distinguish between different kinds of reports. But there are cases
    (e.g. filters versus custom-groups or users versus user-groups ) where
    users want to see the different subtypes of the same type as fundamentally
    different.
    Used across different modeling modules e.g. attributes, user hierarchies.
    """
    FILTER = auto()
    CUSTOM_GROUP = auto()
    FILTER_PARTITION = auto()
    SEGMENT = auto()
    TEMPLATE = auto()
    REPORT_GRID = auto()
    REPORT_GRAPH = auto()
    REPORT_ENGINE = auto()
    REPORT_TEXT = auto()
    REPORT_DATAMART = auto()
    REPORT_BASE = auto()
    REPORT_GRID_AND_GRAPH = auto()
    REPORT_NON_INTERACTIVE = auto()
    REPORT_CUBE = auto()
    REPORT_INCREMENT_REFRESH = auto()
    REPORT_TRANSACTION = auto()
    REPORT_EMMA_CUBE = auto()
    REPORT_EMMA_CUBE_IRR = auto()
    REPORT_HYPER_CARD = auto()
    METRIC = auto()
    METRIC_SUBTOTAL = auto()
    SYSTEM_SUBTOTAL = auto()
    METRIC_DMX = auto()
    METRIC_TRAINING = auto()
    METRIC_EXTREME = auto()
    METRIC_REFERENCE_LINE = auto()
    METRIC_RELATIONSHIP = auto()
    STYLE = auto()
    AGG_METRIC = auto()
    FOLDER = auto()
    FOLDER_SYSTEM = auto()
    DEVICE = auto()
    PROMPT = auto()
    PROMPT_BOOLEAN = auto()
    PROMPT_LONG = auto()
    PROMPT_STRING = auto()
    PROMPT_DOUBLE = auto()
    PROMPT_DATE = auto()
    PROMPT_OBJECTS = auto()
    PROMPT_ELEMENTS = auto()
    PROMPT_EXPRESSION = auto()
    PROMPT_EXPRESSION_DRAFT = auto()
    PROMPT_DIMTY = auto()
    PROMPT_BIG_DECIMAL = auto()
    FUNCTION = auto()
    FUNCTION_THIRD_PARTY = auto()
    ATTRIBUTE = auto()
    ATTRIBUTE_ROLE = auto()
    ATTRIBUTE_TRANSFORMATION = auto()
    ATTRIBUTE_ABSTRACT = auto()
    ATTRIBUTE_RECURSIVE = auto()
    ATTRIBUTE_DERIVED = auto()
    FACT = auto()
    DIMENSION_SYSTEM = auto()
    DIMENSION_USER = auto()
    DIMENSION_ORDERED = auto()
    DIMENSION_USER_HIERARCHY = auto()
    LOGICAL_TABLE = auto()
    TABLE_PARTITION_MD = auto()
    TABLE_PARTITION_WH = auto()
    DATAMART_REPORT = auto()
    FACT_GROUP = auto()
    SHORTCUT = auto()
    SHORTCUT_WEAK_REF = auto()
    RESOLUTION = auto()
    ATTRIBUTE_FORM_SYSTEM = auto()
    ATTRIBUTE_FORM_NORMAL = auto()
    ATTRIBUTE_FORM_CUSTOM = auto()
    SCHEMA = auto()
    FORMAT = auto()
    CATALOG = auto()
    CATALOG_DEFN = auto()
    COLUMN = auto()
    COLUMN_NORMAL = auto()
    COLUMN_CUSTOM = auto()
    PROPERTY_GROUP = auto()
    PROPERTY_SET = auto()
    DB_ROLE = auto()
    DB_ROLE_IMPORT = auto()
    DB_ROLE_IMPORT_PRIMARY = auto()
    DB_ROLE_O_AUTH = auto()
    DB_ROLE_REMOTE_DATE_SOURCE = auto()
    DB_ROLE_URL_AUTH = auto()
    DB_ROLE_GENERIC_DATA_CONNECTOR = auto()
    DB_ROLE_DATA_IMPORT_SERVER = auto()
    DB_ROLE_CLOUD_ELEMENT = auto()
    DB_LOGIN = auto()
    DB_CONNECTION = auto()
    PROJECT = auto()
    SERVER_DEF = auto()
    USER = auto()
    USER_GROUP = auto()
    TRANSMITTER = auto()
    CONFIGURATION = auto()
    REQUEST = auto()
    SEARCH = auto()
    INDEXED_SEARCH = auto()
    RELATIONSHIP_SEARCH = auto()
    SEARCH_FOLDER = auto()
    SEARCH_FOLDER_CROSS_PROJECT = auto()
    DATAMART = auto()
    FUNCTION_PACKAGE_DEFINITION = auto()
    ROLE = auto()
    ROLE_TRANSFORMATION = auto()
    SECURITY_ROLE = auto()
    LOCALE = auto()
    CONSOLIDATION = auto()
    CONSOLIDATION_DERIVED = auto()
    CONSOLIDATION_ELEMENT = auto()
    SCHEDULE_EVENT = auto()
    SCHEDULE_OBJECT = auto()
    SCHEDULE_TRIGGER = auto()
    LINK = auto()
    PHYSICAL_TABLE = auto()
    DB_TABLE_PMT = auto()
    DB_TABLE_SOURCE = auto()
    DOCUMENT_DEFINITION = auto()
    REPORT_WRITING_DOCUMENT = auto()
    DOCUMENT_THEME = auto()
    DOSSIER = auto()
    DRILL_MAP = auto()
    DBMS = auto()
    MD_SECURITY_FILTER = auto()
    MONITOR_PERFORMANCE = auto()
    MONITOR_JOBS = auto()
    MONITOR_USER_CONNECTIONS = auto()
    MONITOR_DB_CONNECTIONS = auto()
    PROMPT_ANSWER = auto()
    PROMPT_ANSWER_BOOLEAN = auto()
    PROMPT_ANSWER_LONG = auto()
    PROMPT_ANSWER_STRING = auto()
    PROMPT_ANSWER_DOUBLE = auto()
    PROMPT_ANSWER_DATE = auto()
    PROMPT_ANSWER_OBJECTS = auto()
    PROMPT_ANSWER_ELEMENTS = auto()
    PROMPT_ANSWER_EXPRESSION = auto()
    PROMPT_ANSWER_EXPRESSION_DRAFT = auto()
    PROMPT_ANSWER_DIMTY = auto()
    PROMPT_ANSWER_BIG_DECIMAL = auto()
    PROMPT_ANSWER_INT64 = auto()
    PROMPT_ANSWERS = auto()
    GRAPH_STYLE = auto()
    CHANGE_JOURNAL_SEARCH = auto()
    BLOB_UNKNOWN = auto()
    BLOB_OTHER = auto()
    BLOB_IMAGE = auto()
    BLOB_PROJECT_PACKAGE = auto()
    BLOB_EXCEL = auto()
    BLOB_HTML_TEMPLATE = auto()
    DASHBOARD_TEMPLATE = auto()
    FLAG = auto()
    CHANGE_JOURNAL = auto()
    EXTERNAL_SHORTCUT_UNKNOWN = auto()
    EXTERNAL_SHORTCUT_URL = auto()
    EXTERNAL_SHORTCUT_SNAPSHOT = auto()
    EXTERNAL_SHORTCUT_TARGET = auto()
    RECONCILIATION = auto()
    PALETTE_SYSTEM = auto()
    PALETTE_CUSTOM = auto()
    THRESHOLDS = auto()
    SUBSCRIPTION_ADDRESS = auto()
    SUBSCRIPTION_CONTACT = auto()
    SUBSCRIPTION_INSTANCE = auto()

@dataclass(eq=False)
class SchemaObjectReference(Dictable):
    """Information about an object referenced within the specification
    of another object. An object reference typically contains only enough
    fields to uniquely identify the referenced objects.

    Attributes:
        object_id: object's id, a globally unique identifier used to
            distinguish between metadata objects within the same project
        sub_type:  string literal used to identify the type of a metadata object
        name: the name of the metadata object
        is_embedded: if true indicates that the target object of this reference
            is embedded within this object, bool
    """
    _DELETE_NONE_VALUES_RECURSION = False
    _FROM_DICT_MAP = {'sub_type': ObjectSubType}
    sub_type: ObjectSubType
    object_id: Optional[str] = None
    name: Optional[str] = None
    is_embedded: Optional[bool] = None

    def __eq__(self, other):
        if not isinstance(other, SchemaObjectReference):
            return False
        return self.object_id == other.object_id and self.sub_type == other.sub_type

    def __hash__(self):
        return hash(self.object_id)

    @classmethod
    def create_from(cls, schema_object: Union['Attribute', 'UserHierarchy'], is_embedded: bool=None) -> 'SchemaObjectReference':
        """Converts a schema object into a schema object reference

            Args:
                schema_object: a schema object
                is_embeded: a boolean indicating whether the schema object
                    is embedded or not

            Returns:
                SchemaObjectReference of the given schema object
        """
        reference_body = {'object_id': schema_object.id, 'name': schema_object.name, 'sub_type': schema_object.sub_type, 'is_embeded': is_embedded}
        return cls.from_dict(reference_body)

    def to_object(self, connection: 'Connection') -> Union['Attribute', 'UserHierarchy']:
        """Converts a schema object reference into a schema object.

            Args:
                connection: a connection object required to fetch
                    the schema object
        """
        if self.sub_type == ObjectSubType.ATTRIBUTE:
            from mstrio.modeling.schema.attribute import Attribute
            return Attribute(connection, id=self.object_id)
        else:
            raise NotImplementedError(f'{self.sub_type} object sub type is not supported yet.')

class DataType(Dictable):
    """Representation in the object model for a data-type that could be used
    for a SQL column.

    Attributes:
        type: gross data type of an actual or proposed column in a database.
        precision: for relevant data types, the length of the representation
        scale: for relevant data types, the fixed position used
        in the representation
    """
    _DELETE_NONE_VALUES_RECURSION = False

    class Type(AutoName):
        """String literal used to identify the gross data type of an actual
        or proposed column in a database."""
        UNKNOWN = auto()
        RESERVED = auto()
        INTEGER = auto()
        UNSIGNED = auto()
        NUMERIC = auto()
        DECIMAL = auto()
        REAL = auto()
        FLOAT = auto()
        CHAR = auto()
        FIXED_LENGTH_STRING = auto()
        VARIABLE_LENGTH_STRING = auto()
        BINARY = auto()
        VAR_BIN = auto()
        LONGVARBIN = auto()
        DATE = auto()
        TIME = auto()
        TIME_STAMP = auto()
        N_CHAR = auto()
        N_VAR_CHAR = auto()
        SHORT = auto()
        LONG = auto()
        MB_CHAR = auto()
        BOOL = auto()
        PATTERN = auto()
        N_PATTERN = auto()
        CELL_FORMAT_DATA = auto()
        MISSING = auto()
        UTF8_CHAR = auto()
        INT64 = auto()
        GUID = auto()
        DOUBLE_DOUBLE = auto()

    def __init__(self, type: Type, precision: str, scale: str) -> None:
        self.type = type
        self.precision = precision
        self.scale = scale

class FormReference(Dictable):
    """	The reference that identifies a form object within the context of a
        given attribute. When writing back an attribute, either id or name is
        needed to identify a form, and if both are provided, id will take
        the higher priority.

        Attributes:
            id: id of the form
            name: name of the form
    """
    _DELETE_NONE_VALUES_RECURSION = False

    def __init__(self, id: str=None, name: str=None) -> None:
        if id is None and name is None:
            exception_handler('Provide either `id` or `name` of a form object.', AttributeError)
        self.id = id
        self.name = name

class AttributeDisplays(Dictable):
    """The collections of report displays and browse displays of the attribute.

    Attributes:
        report_displays: list of an AttributeSorts for report displays
        browse_displays: list of an AttributeSorts for browse displays
    """
    _DELETE_NONE_VALUES_RECURSION = False
    _FROM_DICT_MAP = {'report_displays': lambda source, connection: [FormReference.from_dict(content, connection) for content in source], 'browse_displays': lambda source, connection: [FormReference.from_dict(content, connection) for content in source]}

    def __init__(self, report_displays: List[FormReference], browse_displays: List[FormReference]) -> None:
        self.report_displays = report_displays
        self.browse_displays = browse_displays

class AttributeSort(Dictable):
    """An individual sort element in an AttributeSorts list.

    Attributes:
        form: A form reference
        ascending: whether the sort is in ascending or descending order
    """
    _DELETE_NONE_VALUES_RECURSION = False
    _FROM_DICT_MAP = {'form': FormReference.from_dict}

    def __init__(self, form: FormReference, ascending: bool=False) -> None:
        self.form = form
        self.ascending = ascending

class AttributeSorts(Dictable):
    """The collections of report sorts and browse sorts of the attribute.

    Attributes:
        report_sorts: list of an AttributeSorts for report sorts
        browse_sorts: list of an AttributeSorts for browse sorts
    """
    _DELETE_NONE_VALUES_RECURSION = False
    _FROM_DICT_MAP = {'report_sorts': lambda source, connection: [AttributeSort.from_dict(content, connection) for content in source], 'browse_sorts': lambda source, connection: [AttributeSort.from_dict(content, connection) for content in source]}

    def __init__(self, report_sorts: List[AttributeSort], browse_sorts: List[AttributeSort]) -> None:
        self.report_sorts = report_sorts
        self.browse_sorts = browse_sorts