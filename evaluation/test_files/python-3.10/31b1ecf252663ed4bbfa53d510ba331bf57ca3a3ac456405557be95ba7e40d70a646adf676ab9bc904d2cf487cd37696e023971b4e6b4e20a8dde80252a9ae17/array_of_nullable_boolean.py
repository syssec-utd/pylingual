""" avro python class for file: array_of_nullable_boolean """
import typing
from etptypes import ETPModel, Field, Strict
avro_schema: typing.Final[str] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfNullableBoolean", "fields": [{"name": "values", "type": {"type": "array", "items": ["null", "boolean"]}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfNullableBoolean", "depends": []}'

class ArrayOfNullableBoolean(ETPModel):
    values: typing.List[typing.Optional[Strict[bool]]] = Field(alias='values')