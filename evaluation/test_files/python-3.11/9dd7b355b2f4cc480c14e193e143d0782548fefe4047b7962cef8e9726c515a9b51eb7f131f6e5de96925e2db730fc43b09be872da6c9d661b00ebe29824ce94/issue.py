"""
Issue module.

This module provides the following classes:

- Role
- RolesSchema
- RoleList
- Credit
- CreditsSchema
- Issue
- IssueSchema
- IssuesList
"""
from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load
from mokkari import arc, character, exceptions, publisher, reprint, series, team, variant

class Role:
    """
    The Role object contains information for creators' role.

    :param `**kwargs`: The keyword arguments is used for setting role data from Metron.
    """

    def __init__(self, **kwargs):
        """Initialize a new Role."""
        for k, v in kwargs.items():
            setattr(self, k, v)

class RolesSchema(Schema):
    """Schema for the Roles."""
    id = fields.Int()
    name = fields.Str()

    @post_load
    def make_object(self, data, **kwargs):
        """
        Make the Role object.

        :param data: Data from Metron response.

        :returns: :class:`Role` object
        :rtype: Role
        """
        return Role(**data)

class RoleList:
    """The RoleList object contains a list of `Role` objects."""

    def __init__(self, response):
        """Initialize a new RoleList."""
        self.roles = []
        schema = RolesSchema()
        for role_dict in response['results']:
            try:
                result = schema.load(role_dict)
            except ValidationError as error:
                raise exceptions.ApiError(error) from error
            self.roles.append(result)

    def __iter__(self):
        """Return an iterator object."""
        return iter(self.roles)

    def __len__(self):
        """Return the length of the object."""
        return len(self.roles)

    def __getitem__(self, index: int):
        """Return the object of a at index."""
        return self.roles[index]

class Credit:
    """
    The Credit object contains information for creators credits for an issue.

    :param `**kwargs`: The keyword arguments is used for setting creator credit data.
    """

    def __init__(self, **kwargs):
        """Initialize a new Credit."""
        for k, v in kwargs.items():
            setattr(self, k, v)

class CreditsSchema(Schema):
    """Schema for the Credits."""
    id = fields.Int()
    creator = fields.Str()
    role = fields.Nested(RolesSchema, many=True)

    @post_load
    def make_object(self, data, **kwargs):
        """
        Make the Credit object.

        :param data: Data from Metron response.

        :returns: :class:`Credit` object
        :rtype: Credit
        """
        return Credit(**data)

class Issue:
    """
    The Issue object contains information for an issue.

    :param `**kwargs`: The keyword arguments is used for setting issue data from Metron.
    """

    def __init__(self, **kwargs):
        """Initialize a new Issue."""
        for k, v in kwargs.items():
            setattr(self, k, v)

class IssueSchema(Schema):
    """
    Schema for the Issue API.

    .. versionchanged:: 0.1.6

        - ``name`` field  changed to ``story_titles``
        - ``__str__`` field change to ``issue_name``

    .. versionchanged:: 0.2.0
        Added ``price`` and ``sku`` fields

    .. versionchanged:: 0.2.2
        Added ``upc`` field

    .. versionchanged:: 0.2.4

        - Added ``page_count`` field
        - Changed ``price`` field from a string to float value.

    .. versionchanged:: 1.0.0

        - Changed ``price`` field to a decimal type.
        - Added ``modified`` field

    .. versionchanged:: 2.1.0

        - Add ``reprints`` field

    .. versionadded:: 2.2.2

        - Add ``collection_title`` field

    .. versionchanged:: 2.3.0

        - Removed ``volume`` field. The series object will have that information.
    """
    id = fields.Int()
    publisher = fields.Nested(publisher.PublisherSchema)
    series = fields.Nested(series.SeriesSchema)
    number = fields.Str()
    collection_title = fields.Str(allow_none=True, data_key='title')
    story_titles = fields.List(fields.Str(allow_none=True), data_key='name')
    cover_date = fields.Date()
    store_date = fields.Date(allow_none=True)
    price = fields.Decimal(places=2, allow_none=True)
    sku = fields.Str()
    upc = fields.Str()
    page_count = fields.Int(allow_none=True, data_key='page')
    desc = fields.Str(allow_none=True)
    image = fields.URL()
    arcs = fields.Nested(arc.ArcSchema, many=True)
    credits = fields.Nested(CreditsSchema, many=True)
    characters = fields.Nested(character.CharacterSchema, many=True)
    teams = fields.Nested(team.TeamSchema, many=True)
    reprints = fields.Nested(reprint.ReprintSchema, many=True)
    issue_name = fields.Str(data_key='issue')
    variants = fields.Nested(variant.VariantSchema, many=True)
    modified = fields.DateTime()

    class Meta:
        """Any unknown fields will be excluded."""
        unknown = EXCLUDE
        datetime = '%Y-%m-%dT%H:%M:%S%z'

    @post_load
    def make_object(self, data, **kwargs):
        """
        Make the arc object.

        :param data: Data from Metron response.

        :returns: :class:`Issue` object
        :rtype: Issue
        """
        return Issue(**data)

class IssuesList:
    """The IssuesList object contains a list of `Issue` objects."""

    def __init__(self, response):
        """Initialize a new IssuesList."""
        self.issues = []
        schema = IssueSchema()
        for issue_dict in response['results']:
            try:
                result = schema.load(issue_dict)
            except ValidationError as error:
                raise exceptions.ApiError(error) from error
            self.issues.append(result)

    def __iter__(self):
        """Return an iterator object."""
        return iter(self.issues)

    def __len__(self):
        """Return the length of the object."""
        return len(self.issues)

    def __getitem__(self, index: int):
        """Return the object of a at index."""
        return self.issues[index]