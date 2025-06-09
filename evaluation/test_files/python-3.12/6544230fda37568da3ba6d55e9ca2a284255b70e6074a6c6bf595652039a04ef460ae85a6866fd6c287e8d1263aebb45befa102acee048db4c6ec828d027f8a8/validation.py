import asyncio
import functools
import inspect
from collections import ChainMap
from typing import Awaitable
from typing import Union, Any, Dict, Callable
import pandas
import pandera
from decorator import decorator
from pandera.api.pandas.model import _extract_config_options_and_extras
from typing_extensions import TypeAlias
PanderaSchema: TypeAlias = Union[pandera.DataFrameSchema, pandera.SeriesSchema]
PandasType: TypeAlias = Union[pandas.DataFrame, pandas.Series]
LibrarySchema: TypeAlias = Union[PanderaSchema]
AsyncOrSyncCallable: TypeAlias = Union[Callable[..., Any], Callable[..., Awaitable]]

def async_sync(wrapped_fn: AsyncOrSyncCallable, *fn_args, **fn_kwargs):
    if asyncio.iscoroutinefunction(wrapped_fn):

        @functools.wraps(wrapped_fn)
        async def _decorated(*args, **kwargs) -> Any:
            return await wrapped_fn(*args, **kwargs)
    else:

        @functools.wraps(wrapped_fn)
        def _decorated(*args, **kwargs) -> Any:
            return wrapped_fn(*args, **kwargs)
    return _decorated(*fn_args, **fn_kwargs)

class DataValidationError(Exception):
    pass

def pandera_schema_from_pydantic_schema(schema: LibrarySchema):
    if isinstance(schema, (pandera.DataFrameSchema, pandera.SeriesSchema)):
        return schema
    return schema.to_schema()

def _pydantic_schema_fix_config_inheritance(schema: Any=None):
    config = getattr(schema, pandera.api.pandas.model._CONFIG_KEY, {})
    bases = inspect.getmro(config)[:-1]
    bases = tuple((base for base in bases if issubclass(base, pandera.api.pandas.model.BaseConfig)))
    options = []
    for index, config in enumerate(bases):
        model_options, _ = _extract_config_options_and_extras(config)
        options.append(model_options)
    return type(f'{str(schema.__module__)}.Config', (pandera.api.pandas.model.BaseConfig,), dict(ChainMap(*options)))

def _pandera_checks(data: PandasType=None, schema: LibrarySchema=None, schema_validation_options: Dict[str, Any]=None):
    row_total = len(data)
    sample_row_total = round(row_total * 0.25)
    head_row_total = round(row_total * 0.15)
    schema_validation_options = schema_validation_options or {'head': max(0, min(head_row_total if row_total > 100 else row_total, row_total)), 'tail': max(0, min(head_row_total if row_total > 100 else row_total, row_total)), 'sample': max(0, min(sample_row_total if row_total > 100 else row_total, row_total)), 'lazy': False, 'inplace': True}
    if schema is None:
        raise ValueError('Missing schema')
    try:
        pandera_schema = schema
        if not isinstance(schema, (pandera.DataFrameSchema, pandera.SeriesSchema)):
            schema.__config__ = _pydantic_schema_fix_config_inheritance(schema=schema)
            pandera_schema = pandera_schema_from_pydantic_schema(schema=schema)
        return pandera_schema.validate(data, **schema_validation_options)
    except pandera.errors.SchemaError as e:
        i = 10
        msg = f"\n\n------- Schema Error # --------\nSchema:{schema.__name__}\nDetail: {''.join(list(e.args))}\nFailure Cases: {e.failure_cases}\nRuled failed:{e.schema}"
        raise DataValidationError(msg) from e
    except pandera.errors.SchemaErrors as e:
        msg = ''
        for index, se in enumerate(e.schema_errors):
            error = se.get('error')
            msg += f"\n\n------- Schema Error #{index} --------\nSchema:{schema.__name__}\nReason: {se.get('reason_code')}\nDetail: {''.join(list(error.args))}\nFailure Cases: {error.failure_cases}\nRuled failed:{error.schema}"
        raise DataValidationError(msg) from e

@decorator
def pandas_data_coerce_and_validate(fn: Callable, schema: LibrarySchema=None, schema_validation_options: Dict[str, Any]=None, *fn_args, **fn_kwargs):
    """

    :param fn: Callable:
    :param schema: LibrarySchema:  (Default value = None)
    :param schema_validation_options: Dict[str:
    :param Any]:  (Default value = None)
    :param *fn_args:
    :param **fn_kwargs:

    """
    fn_check = None
    if isinstance(schema, (pandera.DataFrameSchema, pandera.SeriesSchema, pandera.api.base.model.MetaModel)):
        fn_check = _pandera_checks
    else:
        raise NotImplementedError()
    fn_read_and_check = None
    if asyncio.iscoroutinefunction(fn):

        async def _read_and_check(fn_check=None, fn=None, schema=None, schema_validation_options=None, *fn_args, **fn_kwargs):
            data = await fn(*fn_args, **fn_kwargs)
            return fn_check(data=data, schema=schema, schema_validation_options=schema_validation_options)
        fn_read_and_check = _read_and_check
    else:

        def _read_and_check(fn_check=None, fn=None, schema=None, schema_validation_options=None, *fn_args, **fn_kwargs):
            data = fn(*fn_args, **fn_kwargs)
            return fn_check(data=data, schema=schema, schema_validation_options=schema_validation_options)
        fn_read_and_check = _read_and_check
    return _read_and_check(fn_check, fn, schema, schema_validation_options, *fn_args, **fn_kwargs)