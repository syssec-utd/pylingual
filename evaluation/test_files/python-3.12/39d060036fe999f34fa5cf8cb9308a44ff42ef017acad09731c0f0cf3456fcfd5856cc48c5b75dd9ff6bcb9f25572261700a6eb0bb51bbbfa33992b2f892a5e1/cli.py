"""Cli tools."""
from __future__ import annotations
import logging
import sys
from collections import defaultdict
from typing import Any, DefaultDict, Iterable
import click
import jsonschema
import requests
import sqlalchemy
from deepdiff import DeepDiff
from json_encoder import json
from jsonschema import draft7_format_checker
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.schema import CreateTable
from schematools import DEFAULT_PROFILE_URL, DEFAULT_SCHEMA_URL, validation
from schematools.datasetcollection import DatasetCollection, set_schema_loader
from schematools.events.export import export_events
from schematools.events.full import EventsProcessor
from schematools.exceptions import DatasetNotFound, ParserError
from schematools.factories import tables_factory
from schematools.importer.base import BaseImporter
from schematools.importer.geojson import GeoJSONImporter
from schematools.importer.ndjson import NDJSONImporter
from schematools.introspect.db import introspect_db_schema
from schematools.introspect.geojson import introspect_geojson_files
from schematools.maps import create_mapfile
from schematools.permissions.db import apply_schema_and_profile_permissions, introspect_permissions, revoke_permissions
from schematools.provenance.create import ProvenanceIteration
from schematools.types import DatasetSchema
from schematools.utils import dataset_schema_from_path, dataset_schema_from_url, dataset_schemas_from_url
logger = logging.getLogger('schematools.permissions')
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
option_db_url = click.option('--db-url', envvar='DATABASE_URL', required=True, help='DSN of database, can also use DATABASE_URL environment.')
option_schema_url = click.option('--schema-url', envvar='SCHEMA_URL', default=DEFAULT_SCHEMA_URL, show_default=True, required=True, help='Url where valid amsterdam schema files are found. SCHEMA_URL can also be provided as environment variable.')
argument_dataset_id = click.argument('dataset_id')
option_profile_url = click.option('--profile-url', envvar='PROFILE_URL', default=DEFAULT_PROFILE_URL, show_default=True, required=True, help='Url where valid amsterdam profile files are found. PROFILE_URL can also be provided as environment variable.')
argument_profile_location = click.argument('profile_location', metavar='(PROFILE-FILENAME | NONE)')
argument_role = click.argument('role')

def _get_engine(db_url: str, pg_schemas: list[str] | None=None) -> sqlalchemy.engine.Engine:
    """Initialize the SQLAlchemy engine, and report click errors."""
    kwargs = {}
    if pg_schemas is not None:
        csearch_path = ','.join(pg_schemas + ['public'])
        kwargs['connect_args'] = {'options': f'-csearch_path={csearch_path}'}
    try:
        return create_engine(db_url, **kwargs)
    except SQLAlchemyError as e:
        raise click.BadParameter(str(e), param_hint='--db-url') from e

def main() -> None:
    """Main entry point.

    This catches relevant errors, so the user is not
    confronted with internal tracebacks.
    """
    try:
        schema()
    except (OSError, SQLAlchemyError, ParserError) as e:
        click.echo(f'{e.__class__.__name__}: {e}', err=True)
        exit(1)

@click.group()
def schema() -> None:
    """Command line utility to work with Amsterdam Schema files."""
    pass

@schema.group('import')
def import_() -> None:
    """Subcommand to import data."""
    pass

@schema.group('export')
def export() -> None:
    """Subcommand to export data."""
    pass

@schema.group()
def show() -> None:
    """Show existing metadata."""
    pass

@schema.group()
def permissions() -> None:
    """Subcommand for permissions."""
    pass

@schema.group()
def kafka() -> None:
    """Subcommand to consume or produce kafka events."""
    pass

@permissions.command('introspect')
@option_db_url
@argument_role
def permissions_introspect(db_url: str, role: str) -> None:
    """Retrieve ACLs from a database."""
    engine = _get_engine(db_url)
    introspect_permissions(engine, role)

@permissions.command('revoke')
@option_db_url
@argument_role
@click.option('-v', '--verbose', count=True)
def permissions_revoke(db_url: str, role: str, verbose: int) -> None:
    """Revoke all table select priviliges for role."""
    engine = _get_engine(db_url)
    revoke_permissions(engine, role, verbose=verbose)

@permissions.command('apply')
@option_db_url
@option_schema_url
@option_profile_url
@click.option('--schema-filename', is_flag=False, help='Filename of local Amsterdam Schema (single dataset). If specified, it will be used instead of schema-url')
@click.option('--profile-filename', is_flag=False, help='Filename of local Profile. If specified, it will be used instead of profile-url')
@click.option('--pg_schema', is_flag=False, default='public', show_default=True, help='Postgres schema containing the data')
@click.option('--auto', is_flag=True, default=False, help='Grant each scope X to their associated db role scope_x.')
@click.option('--role', is_flag=False, default='', help='Role to receive grants. Ignored when --auto=True')
@click.option('--scope', is_flag=False, default='', help='Scope to be granted. Ignored when --auto=True')
@click.option('--execute/--dry-run', default=False, help='Execute SQL statements or dry-run [default]')
@click.option('--read/--no-read', 'set_read_permissions', default=True, help='Set read permissions [default=read]')
@click.option('--write/--no-write', 'set_write_permissions', default=True, help='Set dataset-level write permissions [default=write]')
@click.option('--create-roles', is_flag=True, default=False, help='Create missing postgres roles')
@click.option('--revoke', is_flag=True, default=False, help='Before granting new permissions, revoke first all previous table and column permissions')
@click.option('-v', '--verbose', count=True)
def permissions_apply(db_url: str, schema_url: str, profile_url: str, schema_filename: str, profile_filename: str, pg_schema: str, auto: bool, role: str, scope: str, execute: bool, create_roles: bool, set_read_permissions: bool, set_write_permissions: bool, revoke: bool, verbose: int) -> None:
    """Set permissions for a postgres role.

    This is based on a scope from Amsterdam Schema or Profiles.
    """
    dry_run = not execute
    if auto:
        role = 'AUTO'
        scope = 'ALL'
    engine = _get_engine(db_url)
    if schema_filename:
        dataset_schema = DatasetSchema.from_file(schema_filename)
        ams_schema = {dataset_schema.id: dataset_schema}
    else:
        ams_schema = dataset_schemas_from_url(schemas_url=schema_url)
    if profile_filename:
        profile = _schema_fetch_url_file(profile_filename)
        profiles = {profile['name']: profile}
    else:
        profiles = None
    if auto or (role and scope):
        apply_schema_and_profile_permissions(engine, pg_schema, ams_schema, profiles, role, scope, set_read_permissions, set_write_permissions, dry_run, create_roles, revoke, verbose=verbose)
    else:
        click.echo('Choose --auto or specify both a --role and a --scope to be able to grant permissions')

def _schema_fetch_url_file(schema_url_file: URL | str) -> dict[str, Any]:
    """Return schemadata from URL or File."""
    if not schema_url_file.startswith('http'):
        with open(schema_url_file) as f:
            schema_data = json.load(f)
    else:
        response = requests.get(schema_url_file)
        response.raise_for_status()
        schema_data = response.json()
    return cast(Dict[str, Any], schema_data)

@schema.group()
def introspect() -> None:
    """Subcommand to generate a schema."""
    pass

@schema.group()
def create() -> None:
    """Subcommand to create a DB object."""
    pass

@schema.group()
def diff() -> None:
    """Subcommand to show schema diffs."""
    pass

def _fetch_json(location: str) -> dict[str, Any]:
    """Fetch JSON from file or URL.

    Args:
        location: a file name or an URL

    Returns:
        JSON data as a dictionary.
    """
    if not location.startswith('http'):
        with open(location) as f:
            json_obj = json.load(f)
    else:
        response = requests.get(location)
        response.raise_for_status()
        json_obj = response.json()
    return json_obj

@schema.command()
@option_schema_url
@argument_dataset_id
@click.option('--additional-schemas', '-a', multiple=True, help='Id of a dataset schema that will be preloaded. To be used mainly for schemas that are related to the schema that is being validated.')
@click.argument('meta_schema_url')
def validate(schema_url: str, dataset_id: str, additional_schemas: list[str], meta_schema_url: str) -> None:
    """Validate a schema against the Amsterdam Schema meta schema.

    Args:

    \x08
        DATASET_ID: id of the dataset.
        META_SCHEMA_URL: URL where the meta schema for Amsterdam Schema definitions can be found.
    """
    meta_schema = _fetch_json(meta_schema_url)
    dataset = _get_dataset_schema(dataset_id, schema_url, prefetch_related=True)
    for schema in additional_schemas:
        _get_dataset_schema(schema, schema_url)
    structural_errors = False
    try:
        jsonschema.validate(instance=dataset.json_data(), schema=meta_schema, format_checker=draft7_format_checker)
    except (jsonschema.ValidationError, jsonschema.SchemaError) as e:
        click.echo('Structural validation: ', nl=False)
        structural_errors = True
        click.echo(f'\n{e!s}', err=True)
    semantic_errors = False
    for error in validation.run(dataset):
        if not semantic_errors:
            click.echo('Semantic validation: ', nl=False)
            semantic_errors = True
        click.echo(f'\n{error!s}', err=True)
    if structural_errors or semantic_errors:
        sys.exit(1)

@schema.command()
@click.argument('meta_schema_url')
@click.argument('schema_files', nargs=-1)
def batch_validate(meta_schema_url: str, schema_files: tuple[str]) -> None:
    """Batch validate schema's.

    This command was tailored so that it could be run from a pre-commit hook. As a result,
    the order and type of its arguments differ from other `schema` sub-commands.

    It will perform both structural and semantic validation of the schema's.

    Args:

    \x08
        META_SCHEMA_URL: the URL to the Amsterdam meta schema
        SCHEMA_FILES: one or more schema files to be validated
    """
    meta_schema = _fetch_json(meta_schema_url)
    errors: DefaultDict[str, list[str]] = defaultdict(list)
    for schema in schema_files:
        try:
            dataset = dataset_schema_from_path(schema)
        except ValueError as ve:
            errors[schema].append(str(ve))
            break
        try:
            jsonschema.validate(instance=dataset.json_data(), schema=meta_schema, format_checker=draft7_format_checker)
        except (jsonschema.ValidationError, jsonschema.SchemaError) as struct_error:
            errors[schema].append(f"{struct_error.message}: ({', '.join(struct_error.path)})")
        for sem_error in validation.run(dataset):
            errors[schema].append(str(sem_error))
    if errors:
        width = len(max(errors.keys()))
        for schema, error_messages in errors.items():
            for err_msg in error_messages:
                click.echo(f'{schema:>{width}}: {err_msg}')
        sys.exit(1)

@show.command('provenance')
@click.argument('dataset_id')
def show_provenance(dataset_id: str) -> None:
    """Retrieve the key-values pairs of the source column.

    (specified as a 'provenance' property of an attribute)
    and its translated name (the attribute name itself)
    """
    dataset = _get_dataset_schema(dataset_id, prefetch_related=True)
    try:
        instance = ProvenanceIteration(dataset)
        click.echo(instance.final_dic)
    except (jsonschema.ValidationError, jsonschema.SchemaError, KeyError) as e:
        click.echo(str(e), err=True)
        exit(1)

@show.command('tablenames')
@option_db_url
def show_tablenames(db_url: str) -> None:
    """Retrieve tablenames from a database."""
    engine = _get_engine(db_url)
    names = inspect(engine).get_table_names()
    click.echo('\n'.join(names))

@show.command('mapfile')
@click.option('--schema-url', envvar='SCHEMA_URL', default=DEFAULT_SCHEMA_URL, show_default=True, required=True, help='Url where valid amsterdam schema files are found. SCHEMA_URL can also be provided as environment variable.')
@click.argument('dataset_id')
def show_mapfile(schema_url: str, dataset_id: str) -> None:
    """Generate a mapfile based on a dataset schema."""
    try:
        dataset_schema = dataset_schema_from_url(schema_url, dataset_id)
    except KeyError:
        raise click.BadParameter(f'Schema {dataset_id} not found.') from None
    click.echo(create_mapfile(dataset_schema))

@introspect.command('db')
@click.option('--db-schema', '-s', help="Tables are in a different postgres schema (not 'public')")
@click.option('--prefix', '-p', help='Tables have prefix that needs to be stripped')
@option_db_url
@click.argument('dataset_id')
@click.argument('tables', nargs=-1)
def introspect_db(db_schema: str, prefix: str, db_url: str, dataset_id: str, tables: Iterable[str]) -> None:
    """Generate a schema for the tables in a database."""
    engine = _get_engine(db_url)
    aschema = introspect_db_schema(engine, dataset_id, tables, db_schema, prefix)
    click.echo(json.dumps(aschema, indent=2))

@introspect.command('geojson')
@click.argument('dataset_id')
@click.argument('files', nargs=-1, required=True)
def introspect_geojson(dataset_id: str, files: Iterable[str]) -> None:
    """Generate a schema from a GeoJSON file."""
    aschema = introspect_geojson_files(dataset_id, files)
    click.echo(json.dumps(aschema, indent=2))

@import_.command('ndjson')
@option_db_url
@option_schema_url
@argument_dataset_id
@click.argument('table_name')
@click.argument('ndjson_path')
@click.option('--truncate-table', is_flag=True)
def import_ndjson(db_url: str, schema_url: str, dataset_id: str, table_name: str, ndjson_path: str, truncate_table: bool) -> None:
    """Import a NDJSON file into a table."""
    engine = _get_engine(db_url)
    dataset_schema = _get_dataset_schema(dataset_id, schema_url)
    importer = NDJSONImporter(dataset_schema, engine)
    importer.load_file(ndjson_path, table_name, truncate=truncate_table)

@import_.command('geojson')
@option_db_url
@option_schema_url
@argument_dataset_id
@click.argument('table_name')
@click.argument('geojson_path')
@click.option('--truncate-table', is_flag=True)
def import_geojson(db_url: str, schema_url: str, dataset_id: str, table_name: str, geojson_path: str, truncate_table: bool) -> None:
    """Import a GeoJSON file into a table."""
    engine = _get_engine(db_url)
    dataset_schema = _get_dataset_schema(dataset_id, schema_url)
    importer = GeoJSONImporter(dataset_schema, engine)
    importer.load_file(geojson_path, table_name, truncate=truncate_table)

@import_.command('events')
@option_db_url
@option_schema_url
@argument_dataset_id
@click.option('--additional-schemas', '-a', multiple=True)
@click.argument('events_path')
@click.option('-t', '--truncate-table', default=False, is_flag=True)
def import_events(db_url: str, schema_url: str, dataset_id: str, additional_schemas: str, events_path: str, truncate_table: bool) -> None:
    """Import an events file into a table."""
    engine = _get_engine(db_url)
    dataset_schemas = [_get_dataset_schema(dataset_id, schema_url)]
    for schema in additional_schemas:
        dataset_schemas.append(_get_dataset_schema(schema, schema_url))
    srid = dataset_schemas[0]['crs'].split(':')[-1]
    with engine.connect() as connection:
        importer = EventsProcessor(dataset_schemas, srid, connection, truncate=truncate_table)
        importer.load_events_from_file(events_path)

def _get_dataset_schema(dataset_id: str, schema_url: str, prefetch_related: bool=False) -> DatasetSchema:
    """Find the dataset schema for the given dataset.

    Args:
        dataset_id: id of the dataset.
        schema_url: url of the location where the collection of amsterdam schemas is found.
        prefetch_related: related schemas should be prefetched.
    """
    set_schema_loader(schema_url)
    dataset_collection = DatasetCollection()
    try:
        return dataset_collection.get_dataset(dataset_id, prefetch_related=prefetch_related)
    except DatasetNotFound as e:
        raise click.ClickException(e)

def _get_all_dataset_schemas(schema_url: str) -> dict[str, DatasetSchema]:
    """Find all the dataset schemas for the given schema_url.

    Args:
        schema_url: url of the location where the collection of amsterdam schemas is found.
    """
    set_schema_loader(schema_url)
    dataset_collection = DatasetCollection()
    return dataset_collection.get_all_datasets()

@create.command('extra_index')
@option_db_url
@option_schema_url
@argument_dataset_id
def create_identifier_index(db_url: str, schema_url: str, dataset_id: str) -> None:
    """Execute SQLalchemy Index based on Identifier in the JSON schema data definition."""
    engine = _get_engine(db_url)
    dataset_schema = _get_dataset_schema(dataset_id, schema_url)
    importer = BaseImporter(dataset_schema, engine)
    for table in dataset_schema.get_tables():
        importer.generate_db_objects(table.id, ind_tables=False, ind_extra_index=True, is_versioned_dataset=importer.is_versioned_dataset)

@create.command('tables')
@option_db_url
@option_schema_url
@argument_dataset_id
def create_tables(db_url: str, schema_url: str, dataset_id: str) -> None:
    """Execute SQLalchemy Table objects."""
    engine = _get_engine(db_url)
    dataset_schema = _get_dataset_schema(dataset_id, schema_url, prefetch_related=True)
    importer = BaseImporter(dataset_schema, engine)
    for table in dataset_schema.get_tables():
        importer.generate_db_objects(table.id, ind_extra_index=False, ind_tables=True, is_versioned_dataset=importer.is_versioned_dataset)

@create.command('sql')
@click.option('--versioned/--no-versioned', default=True)
@option_db_url
@click.argument('schema_path')
def create_sql(versioned: bool, db_url: str, schema_path: str) -> None:
    """Generate SQL Create from amsterdam schema definition."""
    engine = _get_engine(db_url)
    dataset_schema = dataset_schema_from_path(schema_path)
    tables = tables_factory(dataset_schema, is_versioned_dataset=versioned)
    for table in tables.values():
        table_sql = CreateTable(table).compile(engine)
        click.echo(str(table_sql))

@create.command('all')
@option_db_url
@option_schema_url
@click.option('-x', '--exclude', multiple=True, type=str, default=[], help='dataset_id to exclude. Can be repeated.')
@click.argument('dataset_id', required=False)
def create_all_objects(db_url: str, schema_url: str, exclude: list[str], dataset_id: str | None) -> None:
    """Execute SQLalchemy Index (Identifier fields) and Table objects.

    If no DATASET_ID is provide it will process all datasets!
    """
    if dataset_id is None:
        click.echo("No 'dataset_id' provided. Processing all datasets!")
        dataset_schemas = _get_all_dataset_schemas(schema_url)
    else:
        dataset_schemas = {dataset_id: _get_dataset_schema(dataset_id, schema_url, prefetch_related=True)}
    engine = _get_engine(db_url)
    for dataset_id, dataset_schema in dataset_schemas.items():
        if dataset_id in exclude:
            msg = f'Skipping dataset {dataset_id!r}'
            click.echo(msg)
            click.echo('=' * len(msg))
            continue
        msg = f'Processing dataset {dataset_id!r}'
        click.echo(msg)
        click.echo('-' * len(msg))
        importer = BaseImporter(dataset_schema, engine)
        for table in dataset_schema.get_tables():
            importer.generate_db_objects(table.id, is_versioned_dataset=importer.is_versioned_dataset)

@diff.command('all')
@option_schema_url
@click.argument('diff_schema_url')
def diff_schemas(schema_url: str, diff_schema_url: str) -> None:
    """Show diff for two sets of schemas.

    The left-side schemas location is
    defined in SCHEMA_URL (or via --schema-url), the right-side schemas location
    has to be on the command-line.

    This can be used to compare two sets of schemas, e.g. ACC and PRD schemas.

    For nicer output, pipe it through a json formatter.
    """
    schemas = dataset_schemas_from_url(schema_url)
    diff_schemas = dataset_schemas_from_url(diff_schema_url)
    click.echo(DeepDiff(schemas, diff_schemas, ignore_order=True).to_json())

@export.command('events')
@option_db_url
@option_schema_url
@argument_dataset_id
@click.option('--additional-schemas', '-a', multiple=True)
@click.argument('table_id')
def export_events_for(db_url: str, schema_url: str, dataset_id: str, additional_schemas: str, table_id: str) -> None:
    """Export events from postgres."""
    engine = _get_engine(db_url)
    dataset_schemas = [_get_dataset_schema(dataset_id, schema_url)]
    for schema in additional_schemas:
        dataset_schemas.append(_get_dataset_schema(schema, schema_url))
    with engine.begin() as connection:
        for event in export_events(dataset_schemas, dataset_id, table_id, connection):
            click.echo(event)

@kafka.command()
@option_db_url
@option_schema_url
@argument_dataset_id
@click.option('--additional-schemas', '-a', multiple=True)
@click.option('--topics', '-t', multiple=True)
@click.option('--truncate-table', default=False, is_flag=True)
def consume(db_url: str, schema_url: str, dataset_id: str, additional_schemas: str, topics: Iterable[str], truncate_table: bool) -> None:
    """Consume kafka events."""
    from schematools.events.consumer import consume_events
    engine = _get_engine(db_url)
    dataset_schemas = [_get_dataset_schema(dataset_id, schema_url)]
    for schema in additional_schemas:
        dataset_schemas.append(_get_dataset_schema(schema, schema_url))
    srid = dataset_schemas[0]['crs'].split(':')[-1]
    with engine.connect() as connection:
        consume_events(dataset_schemas, srid, connection, topics, truncate=truncate_table)
if __name__ == '__main__':
    main()