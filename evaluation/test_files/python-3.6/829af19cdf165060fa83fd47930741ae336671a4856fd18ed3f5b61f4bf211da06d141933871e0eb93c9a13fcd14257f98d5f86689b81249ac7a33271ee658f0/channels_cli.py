from __future__ import print_function
import click
import oci
import six
import sys
from oci_cli import cli_constants
from oci_cli import cli_util
from oci_cli import json_skeleton_utils
from oci_cli import custom_types
from oci_cli.aliasing import CommandGroupWithAlias
from services.mysql.src.oci_cli_mysql.generated import mysql_service_cli

@click.command(cli_util.override('channels.channels_root_group.command_name', 'channels'), cls=CommandGroupWithAlias, help=cli_util.override('channels.channels_root_group.help', 'The API for the MySQL Database Service'), short_help=cli_util.override('channels.channels_root_group.short_help', 'MySQL Database Service API'))
@cli_util.help_option_group
def channels_root_group():
    pass

@click.command(cli_util.override('channels.channel_group.command_name', 'channel'), cls=CommandGroupWithAlias, help='A Channel connecting a DB System to an external entity.')
@cli_util.help_option_group
def channel_group():
    pass
mysql_service_cli.mysql_service_group.add_command(channels_root_group)
channels_root_group.add_command(channel_group)

@channel_group.command(name=cli_util.override('channels.create_channel.command_name', 'create'), help=u'Creates a Channel to establish replication from a source to a target. \n[Command Reference](createChannel)')
@cli_util.option('--source', required=True, type=custom_types.CLI_COMPLEX_TYPE, help=u'' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--target', required=True, type=custom_types.CLI_COMPLEX_TYPE, help=u'' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--compartment-id', help=u'The OCID of the compartment.')
@cli_util.option('--display-name', help=u'The user-friendly name for the Channel. It does not have to be unique.')
@cli_util.option('--is-enabled', type=click.BOOL, help=u'Whether the Channel should be enabled upon creation. If set to true, the Channel will be asynchronously started as a result of the create Channel operation.')
@cli_util.option('--description', help=u'User provided information about the Channel.')
@cli_util.option('--freeform-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u'Simple key-value pair applied without any predefined name, type or scope. Exists for cross-compatibility only. Example: `{"bar-key": "value"}`' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--defined-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u'Usage of predefined tag keys. These predefined keys are scoped to namespaces. Example: `{"foo-namespace": {"bar-key": "value"}}`' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(['ACCEPTED', 'IN_PROGRESS', 'FAILED', 'SUCCEEDED', 'CANCELING', 'CANCELED']), multiple=True, help='This operation asynchronously creates, modifies or deletes a resource and uses a work request to track the progress of the operation. Specify this option to perform the action and then wait until the work request reaches a certain state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.')
@cli_util.option('--max-wait-seconds', type=click.INT, help='The maximum time to wait for the work request to reach the state defined by --wait-for-state. Defaults to 1200 seconds.')
@cli_util.option('--wait-interval-seconds', type=click.INT, help='Check every --wait-interval-seconds to see whether the work request has reached the state defined by --wait-for-state. Defaults to 30 seconds.')
@json_skeleton_utils.get_cli_json_input_option({'source': {'module': 'mysql', 'class': 'CreateChannelSourceDetails'}, 'target': {'module': 'mysql', 'class': 'CreateChannelTargetDetails'}, 'freeform-tags': {'module': 'mysql', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'mysql', 'class': 'dict(str, dict(str, object))'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'source': {'module': 'mysql', 'class': 'CreateChannelSourceDetails'}, 'target': {'module': 'mysql', 'class': 'CreateChannelTargetDetails'}, 'freeform-tags': {'module': 'mysql', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'mysql', 'class': 'dict(str, dict(str, object))'}}, output_type={'module': 'mysql', 'class': 'Channel'})
@cli_util.wrap_exceptions
def create_channel(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, source, target, compartment_id, display_name, is_enabled, description, freeform_tags, defined_tags):
    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    _details = {}
    _details['source'] = cli_util.parse_json_parameter('source', source)
    _details['target'] = cli_util.parse_json_parameter('target', target)
    if compartment_id is not None:
        _details['compartmentId'] = compartment_id
    if display_name is not None:
        _details['displayName'] = display_name
    if is_enabled is not None:
        _details['isEnabled'] = is_enabled
    if description is not None:
        _details['description'] = description
    if freeform_tags is not None:
        _details['freeformTags'] = cli_util.parse_json_parameter('freeform_tags', freeform_tags)
    if defined_tags is not None:
        _details['definedTags'] = cli_util.parse_json_parameter('defined_tags', defined_tags)
    client = cli_util.build_client('mysql', 'channels', ctx)
    result = client.create_channel(create_channel_details=_details, **kwargs)
    if wait_for_state:
        client = cli_util.build_client('mysql', 'work_requests', ctx)
        if hasattr(client, 'get_work_request') and callable(getattr(client, 'get_work_request')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds
                click.echo('Action completed. Waiting until the work request has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_work_request(result.headers['opc-work-request-id']), 'status', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                click.echo('Failed to wait until the work request entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for work request to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the work request to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)

@channel_group.command(name=cli_util.override('channels.create_channel_create_channel_source_from_mysql_details.command_name', 'create-channel-create-channel-source-from-mysql-details'), help=u'Creates a Channel to establish replication from a source to a target. \n[Command Reference](createChannel)')
@cli_util.option('--target', required=True, type=custom_types.CLI_COMPLEX_TYPE, help=u'' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--source-hostname', required=True, help=u'The network address of the MySQL instance.')
@cli_util.option('--source-username', required=True, help=u'The name of the replication user on the source MySQL instance. The username has a maximum length of 96 characters. For more information, please see the [MySQL documentation]')
@cli_util.option('--source-password', required=True, help=u'The password for the replication user. The password must be between 8 and 32 characters long, and must contain at least 1 numeric character, 1 lowercase character, 1 uppercase character, and 1 special (nonalphanumeric) character.')
@cli_util.option('--source-ssl-mode', required=True, help=u'The SSL mode of the Channel.')
@cli_util.option('--compartment-id', help=u'The OCID of the compartment.')
@cli_util.option('--display-name', help=u'The user-friendly name for the Channel. It does not have to be unique.')
@cli_util.option('--is-enabled', type=click.BOOL, help=u'Whether the Channel should be enabled upon creation. If set to true, the Channel will be asynchronously started as a result of the create Channel operation.')
@cli_util.option('--description', help=u'User provided information about the Channel.')
@cli_util.option('--freeform-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u'Simple key-value pair applied without any predefined name, type or scope. Exists for cross-compatibility only. Example: `{"bar-key": "value"}`' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--defined-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u'Usage of predefined tag keys. These predefined keys are scoped to namespaces. Example: `{"foo-namespace": {"bar-key": "value"}}`' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--source-port', type=click.INT, help=u'The port the source MySQL instance listens on.')
@cli_util.option('--source-ssl-ca-certificate', type=custom_types.CLI_COMPLEX_TYPE, help=u'' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--source-anonymous-transactions-handling', type=custom_types.CLI_COMPLEX_TYPE, help=u'' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(['ACCEPTED', 'IN_PROGRESS', 'FAILED', 'SUCCEEDED', 'CANCELING', 'CANCELED']), multiple=True, help='This operation asynchronously creates, modifies or deletes a resource and uses a work request to track the progress of the operation. Specify this option to perform the action and then wait until the work request reaches a certain state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.')
@cli_util.option('--max-wait-seconds', type=click.INT, help='The maximum time to wait for the work request to reach the state defined by --wait-for-state. Defaults to 1200 seconds.')
@cli_util.option('--wait-interval-seconds', type=click.INT, help='Check every --wait-interval-seconds to see whether the work request has reached the state defined by --wait-for-state. Defaults to 30 seconds.')
@json_skeleton_utils.get_cli_json_input_option({'target': {'module': 'mysql', 'class': 'CreateChannelTargetDetails'}, 'freeform-tags': {'module': 'mysql', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'mysql', 'class': 'dict(str, dict(str, object))'}, 'source-ssl-ca-certificate': {'module': 'mysql', 'class': 'CaCertificate'}, 'source-anonymous-transactions-handling': {'module': 'mysql', 'class': 'AnonymousTransactionsHandling'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'target': {'module': 'mysql', 'class': 'CreateChannelTargetDetails'}, 'freeform-tags': {'module': 'mysql', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'mysql', 'class': 'dict(str, dict(str, object))'}, 'source-ssl-ca-certificate': {'module': 'mysql', 'class': 'CaCertificate'}, 'source-anonymous-transactions-handling': {'module': 'mysql', 'class': 'AnonymousTransactionsHandling'}}, output_type={'module': 'mysql', 'class': 'Channel'})
@cli_util.wrap_exceptions
def create_channel_create_channel_source_from_mysql_details(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, target, source_hostname, source_username, source_password, source_ssl_mode, compartment_id, display_name, is_enabled, description, freeform_tags, defined_tags, source_port, source_ssl_ca_certificate, source_anonymous_transactions_handling):
    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    _details = {}
    _details['source'] = {}
    _details['target'] = cli_util.parse_json_parameter('target', target)
    _details['source']['hostname'] = source_hostname
    _details['source']['username'] = source_username
    _details['source']['password'] = source_password
    _details['source']['sslMode'] = source_ssl_mode
    if compartment_id is not None:
        _details['compartmentId'] = compartment_id
    if display_name is not None:
        _details['displayName'] = display_name
    if is_enabled is not None:
        _details['isEnabled'] = is_enabled
    if description is not None:
        _details['description'] = description
    if freeform_tags is not None:
        _details['freeformTags'] = cli_util.parse_json_parameter('freeform_tags', freeform_tags)
    if defined_tags is not None:
        _details['definedTags'] = cli_util.parse_json_parameter('defined_tags', defined_tags)
    if source_port is not None:
        _details['source']['port'] = source_port
    if source_ssl_ca_certificate is not None:
        _details['source']['sslCaCertificate'] = cli_util.parse_json_parameter('source_ssl_ca_certificate', source_ssl_ca_certificate)
    if source_anonymous_transactions_handling is not None:
        _details['source']['anonymousTransactionsHandling'] = cli_util.parse_json_parameter('source_anonymous_transactions_handling', source_anonymous_transactions_handling)
    _details['source']['sourceType'] = 'MYSQL'
    client = cli_util.build_client('mysql', 'channels', ctx)
    result = client.create_channel(create_channel_details=_details, **kwargs)
    if wait_for_state:
        client = cli_util.build_client('mysql', 'work_requests', ctx)
        if hasattr(client, 'get_work_request') and callable(getattr(client, 'get_work_request')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds
                click.echo('Action completed. Waiting until the work request has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_work_request(result.headers['opc-work-request-id']), 'status', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                click.echo('Failed to wait until the work request entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for work request to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the work request to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)

@channel_group.command(name=cli_util.override('channels.create_channel_create_channel_target_from_db_system_details.command_name', 'create-channel-create-channel-target-from-db-system-details'), help=u'Creates a Channel to establish replication from a source to a target. \n[Command Reference](createChannel)')
@cli_util.option('--source', required=True, type=custom_types.CLI_COMPLEX_TYPE, help=u'' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--target-db-system-id', required=True, help=u'The OCID of the target DB System.')
@cli_util.option('--compartment-id', help=u'The OCID of the compartment.')
@cli_util.option('--display-name', help=u'The user-friendly name for the Channel. It does not have to be unique.')
@cli_util.option('--is-enabled', type=click.BOOL, help=u'Whether the Channel should be enabled upon creation. If set to true, the Channel will be asynchronously started as a result of the create Channel operation.')
@cli_util.option('--description', help=u'User provided information about the Channel.')
@cli_util.option('--freeform-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u'Simple key-value pair applied without any predefined name, type or scope. Exists for cross-compatibility only. Example: `{"bar-key": "value"}`' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--defined-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u'Usage of predefined tag keys. These predefined keys are scoped to namespaces. Example: `{"foo-namespace": {"bar-key": "value"}}`' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--target-channel-name', help=u'The case-insensitive name that identifies the replication channel. Channel names must follow the rules defined for [MySQL identifiers]. The names of non-Deleted Channels must be unique for each DB System.')
@cli_util.option('--target-applier-username', help=u'The username for the replication applier of the target MySQL DB System.')
@cli_util.option('--target-filters', type=custom_types.CLI_COMPLEX_TYPE, help=u'Replication filter rules to be applied at the DB System Channel target.\n\nThis option is a JSON list with items of type ChannelFilter.  For documentation on ChannelFilter please see our API reference: https://docs.cloud.oracle.com/api/#/en/channels/20190415/datatypes/ChannelFilter.' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(['ACCEPTED', 'IN_PROGRESS', 'FAILED', 'SUCCEEDED', 'CANCELING', 'CANCELED']), multiple=True, help='This operation asynchronously creates, modifies or deletes a resource and uses a work request to track the progress of the operation. Specify this option to perform the action and then wait until the work request reaches a certain state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.')
@cli_util.option('--max-wait-seconds', type=click.INT, help='The maximum time to wait for the work request to reach the state defined by --wait-for-state. Defaults to 1200 seconds.')
@cli_util.option('--wait-interval-seconds', type=click.INT, help='Check every --wait-interval-seconds to see whether the work request has reached the state defined by --wait-for-state. Defaults to 30 seconds.')
@json_skeleton_utils.get_cli_json_input_option({'source': {'module': 'mysql', 'class': 'CreateChannelSourceDetails'}, 'freeform-tags': {'module': 'mysql', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'mysql', 'class': 'dict(str, dict(str, object))'}, 'target-filters': {'module': 'mysql', 'class': 'list[ChannelFilter]'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'source': {'module': 'mysql', 'class': 'CreateChannelSourceDetails'}, 'freeform-tags': {'module': 'mysql', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'mysql', 'class': 'dict(str, dict(str, object))'}, 'target-filters': {'module': 'mysql', 'class': 'list[ChannelFilter]'}}, output_type={'module': 'mysql', 'class': 'Channel'})
@cli_util.wrap_exceptions
def create_channel_create_channel_target_from_db_system_details(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, source, target_db_system_id, compartment_id, display_name, is_enabled, description, freeform_tags, defined_tags, target_channel_name, target_applier_username, target_filters):
    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    _details = {}
    _details['target'] = {}
    _details['source'] = cli_util.parse_json_parameter('source', source)
    _details['target']['dbSystemId'] = target_db_system_id
    if compartment_id is not None:
        _details['compartmentId'] = compartment_id
    if display_name is not None:
        _details['displayName'] = display_name
    if is_enabled is not None:
        _details['isEnabled'] = is_enabled
    if description is not None:
        _details['description'] = description
    if freeform_tags is not None:
        _details['freeformTags'] = cli_util.parse_json_parameter('freeform_tags', freeform_tags)
    if defined_tags is not None:
        _details['definedTags'] = cli_util.parse_json_parameter('defined_tags', defined_tags)
    if target_channel_name is not None:
        _details['target']['channelName'] = target_channel_name
    if target_applier_username is not None:
        _details['target']['applierUsername'] = target_applier_username
    if target_filters is not None:
        _details['target']['filters'] = cli_util.parse_json_parameter('target_filters', target_filters)
    _details['target']['targetType'] = 'DBSYSTEM'
    client = cli_util.build_client('mysql', 'channels', ctx)
    result = client.create_channel(create_channel_details=_details, **kwargs)
    if wait_for_state:
        client = cli_util.build_client('mysql', 'work_requests', ctx)
        if hasattr(client, 'get_work_request') and callable(getattr(client, 'get_work_request')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds
                click.echo('Action completed. Waiting until the work request has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_work_request(result.headers['opc-work-request-id']), 'status', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                click.echo('Failed to wait until the work request entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for work request to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the work request to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)

@channel_group.command(name=cli_util.override('channels.delete_channel.command_name', 'delete'), help=u'Deletes the specified Channel. \n[Command Reference](deleteChannel)')
@cli_util.option('--channel-id', required=True, help=u'The Channel [OCID].')
@cli_util.option('--if-match', help=u"For optimistic concurrency control. In the PUT or DELETE call for a resource, set the `If-Match` header to the value of the etag from a previous GET or POST response for that resource. The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.")
@cli_util.confirm_delete_option
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(['ACCEPTED', 'IN_PROGRESS', 'FAILED', 'SUCCEEDED', 'CANCELING', 'CANCELED']), multiple=True, help='This operation asynchronously creates, modifies or deletes a resource and uses a work request to track the progress of the operation. Specify this option to perform the action and then wait until the work request reaches a certain state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.')
@cli_util.option('--max-wait-seconds', type=click.INT, help='The maximum time to wait for the work request to reach the state defined by --wait-for-state. Defaults to 1200 seconds.')
@cli_util.option('--wait-interval-seconds', type=click.INT, help='Check every --wait-interval-seconds to see whether the work request has reached the state defined by --wait-for-state. Defaults to 30 seconds.')
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def delete_channel(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, channel_id, if_match):
    if isinstance(channel_id, six.string_types) and len(channel_id.strip()) == 0:
        raise click.UsageError('Parameter --channel-id cannot be whitespace or empty string')
    kwargs = {}
    if if_match is not None:
        kwargs['if_match'] = if_match
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('mysql', 'channels', ctx)
    result = client.delete_channel(channel_id=channel_id, **kwargs)
    if wait_for_state:
        client = cli_util.build_client('mysql', 'work_requests', ctx)
        if hasattr(client, 'get_work_request') and callable(getattr(client, 'get_work_request')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds
                click.echo('Action completed. Waiting until the work request has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_work_request(result.headers['opc-work-request-id']), 'status', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                click.echo('Failed to wait until the work request entered the specified state. Please retrieve the work request to find its current state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for work request to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the work request to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)

@channel_group.command(name=cli_util.override('channels.get_channel.command_name', 'get'), help=u'Gets the full details of the specified Channel, including the user-specified configuration parameters (passwords are omitted), as well as information about the state of the Channel, its sources and targets. \n[Command Reference](getChannel)')
@cli_util.option('--channel-id', required=True, help=u'The Channel [OCID].')
@cli_util.option('--if-none-match', help=u'For conditional requests. In the GET call for a resource, set the `If-None-Match` header to the value of the ETag from a previous GET (or POST or PUT) response for that resource. The server will return with either a 304 Not Modified response if the resource has not changed, or a 200 OK response with the updated representation.')
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'mysql', 'class': 'Channel'})
@cli_util.wrap_exceptions
def get_channel(ctx, from_json, channel_id, if_none_match):
    if isinstance(channel_id, six.string_types) and len(channel_id.strip()) == 0:
        raise click.UsageError('Parameter --channel-id cannot be whitespace or empty string')
    kwargs = {}
    if if_none_match is not None:
        kwargs['if_none_match'] = if_none_match
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('mysql', 'channels', ctx)
    result = client.get_channel(channel_id=channel_id, **kwargs)
    cli_util.render_response(result, ctx)

@channel_group.command(name=cli_util.override('channels.list_channels.command_name', 'list'), help=u'Lists all the Channels that match the specified filters. \n[Command Reference](listChannels)')
@cli_util.option('--compartment-id', required=True, help=u'The compartment [OCID].')
@cli_util.option('--db-system-id', help=u'The DB System [OCID].')
@cli_util.option('--channel-id', help=u'The OCID of the Channel.')
@cli_util.option('--display-name', help=u'A filter to return only the resource matching the given display name exactly.')
@cli_util.option('--lifecycle-state', type=custom_types.CliCaseInsensitiveChoice(['CREATING', 'ACTIVE', 'NEEDS_ATTENTION', 'INACTIVE', 'UPDATING', 'DELETING', 'DELETED', 'FAILED']), help=u'The LifecycleState of the Channel.')
@cli_util.option('--is-enabled', type=click.BOOL, help=u'If true, returns only Channels that are enabled. If false, returns only Channels that are disabled.')
@cli_util.option('--sort-by', type=custom_types.CliCaseInsensitiveChoice(['displayName', 'timeCreated']), help=u'The field to sort by. Only one sort order may be provided. Time fields are default ordered as descending. Display name is default ordered as ascending.')
@cli_util.option('--sort-order', type=custom_types.CliCaseInsensitiveChoice(['ASC', 'DESC']), help=u'The sort order to use (ASC or DESC).')
@cli_util.option('--limit', type=click.INT, help=u'The maximum number of items to return in a paginated list call. For information about pagination, see [List Pagination].')
@cli_util.option('--page', help=u'The value of the `opc-next-page` or `opc-prev-page` response header from the previous list call. For information about pagination, see [List Pagination].')
@cli_util.option('--all', 'all_pages', is_flag=True, help='Fetches all pages of results. If you provide this option, then you cannot provide the --limit option.')
@cli_util.option('--page-size', type=click.INT, help='When fetching results, the number of results to fetch per call. Only valid when used with --all or --limit, and ignored otherwise.')
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'mysql', 'class': 'list[ChannelSummary]'})
@cli_util.wrap_exceptions
def list_channels(ctx, from_json, all_pages, page_size, compartment_id, db_system_id, channel_id, display_name, lifecycle_state, is_enabled, sort_by, sort_order, limit, page):
    if all_pages and limit:
        raise click.UsageError('If you provide the --all option you cannot provide the --limit option')
    kwargs = {}
    if db_system_id is not None:
        kwargs['db_system_id'] = db_system_id
    if channel_id is not None:
        kwargs['channel_id'] = channel_id
    if display_name is not None:
        kwargs['display_name'] = display_name
    if lifecycle_state is not None:
        kwargs['lifecycle_state'] = lifecycle_state
    if is_enabled is not None:
        kwargs['is_enabled'] = is_enabled
    if sort_by is not None:
        kwargs['sort_by'] = sort_by
    if sort_order is not None:
        kwargs['sort_order'] = sort_order
    if limit is not None:
        kwargs['limit'] = limit
    if page is not None:
        kwargs['page'] = page
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('mysql', 'channels', ctx)
    if all_pages:
        if page_size:
            kwargs['limit'] = page_size
        result = cli_util.list_call_get_all_results(client.list_channels, compartment_id=compartment_id, **kwargs)
    elif limit is not None:
        result = cli_util.list_call_get_up_to_limit(client.list_channels, limit, page_size, compartment_id=compartment_id, **kwargs)
    else:
        result = client.list_channels(compartment_id=compartment_id, **kwargs)
    cli_util.render_response(result, ctx)

@channel_group.command(name=cli_util.override('channels.reset_channel.command_name', 'reset'), help=u'Resets the specified Channel by purging its cached information, leaving the Channel as if it had just been created. This operation is only accepted in Inactive Channels. \n[Command Reference](resetChannel)')
@cli_util.option('--channel-id', required=True, help=u'The Channel [OCID].')
@cli_util.option('--if-match', help=u"For optimistic concurrency control. In the PUT or DELETE call for a resource, set the `If-Match` header to the value of the etag from a previous GET or POST response for that resource. The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.")
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(['ACCEPTED', 'IN_PROGRESS', 'FAILED', 'SUCCEEDED', 'CANCELING', 'CANCELED']), multiple=True, help='This operation asynchronously creates, modifies or deletes a resource and uses a work request to track the progress of the operation. Specify this option to perform the action and then wait until the work request reaches a certain state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.')
@cli_util.option('--max-wait-seconds', type=click.INT, help='The maximum time to wait for the work request to reach the state defined by --wait-for-state. Defaults to 1200 seconds.')
@cli_util.option('--wait-interval-seconds', type=click.INT, help='Check every --wait-interval-seconds to see whether the work request has reached the state defined by --wait-for-state. Defaults to 30 seconds.')
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def reset_channel(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, channel_id, if_match):
    if isinstance(channel_id, six.string_types) and len(channel_id.strip()) == 0:
        raise click.UsageError('Parameter --channel-id cannot be whitespace or empty string')
    kwargs = {}
    if if_match is not None:
        kwargs['if_match'] = if_match
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('mysql', 'channels', ctx)
    result = client.reset_channel(channel_id=channel_id, **kwargs)
    if wait_for_state:
        client = cli_util.build_client('mysql', 'work_requests', ctx)
        if hasattr(client, 'get_work_request') and callable(getattr(client, 'get_work_request')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds
                click.echo('Action completed. Waiting until the work request has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_work_request(result.headers['opc-work-request-id']), 'status', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                click.echo('Failed to wait until the work request entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for work request to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the work request to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)

@channel_group.command(name=cli_util.override('channels.resume_channel.command_name', 'resume'), help=u'Resumes an enabled Channel that has become Inactive due to an error. The resume operation requires that the error that cause the Channel to become Inactive has already been fixed, otherwise the operation may fail. \n[Command Reference](resumeChannel)')
@cli_util.option('--channel-id', required=True, help=u'The Channel [OCID].')
@cli_util.option('--if-match', help=u"For optimistic concurrency control. In the PUT or DELETE call for a resource, set the `If-Match` header to the value of the etag from a previous GET or POST response for that resource. The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.")
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(['ACCEPTED', 'IN_PROGRESS', 'FAILED', 'SUCCEEDED', 'CANCELING', 'CANCELED']), multiple=True, help='This operation asynchronously creates, modifies or deletes a resource and uses a work request to track the progress of the operation. Specify this option to perform the action and then wait until the work request reaches a certain state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.')
@cli_util.option('--max-wait-seconds', type=click.INT, help='The maximum time to wait for the work request to reach the state defined by --wait-for-state. Defaults to 1200 seconds.')
@cli_util.option('--wait-interval-seconds', type=click.INT, help='Check every --wait-interval-seconds to see whether the work request has reached the state defined by --wait-for-state. Defaults to 30 seconds.')
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def resume_channel(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, channel_id, if_match):
    if isinstance(channel_id, six.string_types) and len(channel_id.strip()) == 0:
        raise click.UsageError('Parameter --channel-id cannot be whitespace or empty string')
    kwargs = {}
    if if_match is not None:
        kwargs['if_match'] = if_match
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('mysql', 'channels', ctx)
    result = client.resume_channel(channel_id=channel_id, **kwargs)
    if wait_for_state:
        client = cli_util.build_client('mysql', 'work_requests', ctx)
        if hasattr(client, 'get_work_request') and callable(getattr(client, 'get_work_request')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds
                click.echo('Action completed. Waiting until the work request has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_work_request(result.headers['opc-work-request-id']), 'status', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                click.echo('Failed to wait until the work request entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for work request to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the work request to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)

@channel_group.command(name=cli_util.override('channels.update_channel.command_name', 'update'), help=u'Updates the properties of the specified Channel. If the Channel is Active the Update operation will asynchronously apply the new configuration parameters to the Channel and the Channel may become temporarily unavailable. Otherwise, the new configuration will be applied the next time the Channel becomes Active. \n[Command Reference](updateChannel)')
@cli_util.option('--channel-id', required=True, help=u'The Channel [OCID].')
@cli_util.option('--source', type=custom_types.CLI_COMPLEX_TYPE, help=u'' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--target', type=custom_types.CLI_COMPLEX_TYPE, help=u'' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--display-name', help=u'The user-friendly name for the Channel. It does not have to be unique.')
@cli_util.option('--is-enabled', type=click.BOOL, help=u'Whether the Channel should be enabled or disabled. Enabling a previously disabled Channel will cause the Channel to be started. Conversely, disabling a previously enabled Channel will stop the Channel. Both operations are executed asynchronously.')
@cli_util.option('--description', help=u'User provided description of the Channel.')
@cli_util.option('--freeform-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u'Simple key-value pair applied without any predefined name, type or scope. Exists for cross-compatibility only. Example: `{"bar-key": "value"}`' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--defined-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u'Usage of predefined tag keys. These predefined keys are scoped to namespaces. Example: `{"foo-namespace": {"bar-key": "value"}}`' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--if-match', help=u"For optimistic concurrency control. In the PUT or DELETE call for a resource, set the `If-Match` header to the value of the etag from a previous GET or POST response for that resource. The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.")
@cli_util.option('--force', help='Perform update without prompting for confirmation.', is_flag=True)
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(['ACCEPTED', 'IN_PROGRESS', 'FAILED', 'SUCCEEDED', 'CANCELING', 'CANCELED']), multiple=True, help='This operation asynchronously creates, modifies or deletes a resource and uses a work request to track the progress of the operation. Specify this option to perform the action and then wait until the work request reaches a certain state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.')
@cli_util.option('--max-wait-seconds', type=click.INT, help='The maximum time to wait for the work request to reach the state defined by --wait-for-state. Defaults to 1200 seconds.')
@cli_util.option('--wait-interval-seconds', type=click.INT, help='Check every --wait-interval-seconds to see whether the work request has reached the state defined by --wait-for-state. Defaults to 30 seconds.')
@json_skeleton_utils.get_cli_json_input_option({'source': {'module': 'mysql', 'class': 'UpdateChannelSourceDetails'}, 'target': {'module': 'mysql', 'class': 'UpdateChannelTargetDetails'}, 'freeform-tags': {'module': 'mysql', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'mysql', 'class': 'dict(str, dict(str, object))'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'source': {'module': 'mysql', 'class': 'UpdateChannelSourceDetails'}, 'target': {'module': 'mysql', 'class': 'UpdateChannelTargetDetails'}, 'freeform-tags': {'module': 'mysql', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'mysql', 'class': 'dict(str, dict(str, object))'}})
@cli_util.wrap_exceptions
def update_channel(ctx, from_json, force, wait_for_state, max_wait_seconds, wait_interval_seconds, channel_id, source, target, display_name, is_enabled, description, freeform_tags, defined_tags, if_match):
    if isinstance(channel_id, six.string_types) and len(channel_id.strip()) == 0:
        raise click.UsageError('Parameter --channel-id cannot be whitespace or empty string')
    if not force:
        if source or target or freeform_tags or defined_tags:
            if not click.confirm('WARNING: Updates to source and target and freeform-tags and defined-tags will replace any existing values. Are you sure you want to continue?'):
                ctx.abort()
    kwargs = {}
    if if_match is not None:
        kwargs['if_match'] = if_match
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    _details = {}
    if source is not None:
        _details['source'] = cli_util.parse_json_parameter('source', source)
    if target is not None:
        _details['target'] = cli_util.parse_json_parameter('target', target)
    if display_name is not None:
        _details['displayName'] = display_name
    if is_enabled is not None:
        _details['isEnabled'] = is_enabled
    if description is not None:
        _details['description'] = description
    if freeform_tags is not None:
        _details['freeformTags'] = cli_util.parse_json_parameter('freeform_tags', freeform_tags)
    if defined_tags is not None:
        _details['definedTags'] = cli_util.parse_json_parameter('defined_tags', defined_tags)
    client = cli_util.build_client('mysql', 'channels', ctx)
    result = client.update_channel(channel_id=channel_id, update_channel_details=_details, **kwargs)
    if wait_for_state:
        client = cli_util.build_client('mysql', 'work_requests', ctx)
        if hasattr(client, 'get_work_request') and callable(getattr(client, 'get_work_request')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds
                click.echo('Action completed. Waiting until the work request has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_work_request(result.headers['opc-work-request-id']), 'status', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                click.echo('Failed to wait until the work request entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for work request to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the work request to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)

@channel_group.command(name=cli_util.override('channels.update_channel_update_channel_source_from_mysql_details.command_name', 'update-channel-update-channel-source-from-mysql-details'), help=u'Updates the properties of the specified Channel. If the Channel is Active the Update operation will asynchronously apply the new configuration parameters to the Channel and the Channel may become temporarily unavailable. Otherwise, the new configuration will be applied the next time the Channel becomes Active. \n[Command Reference](updateChannel)')
@cli_util.option('--channel-id', required=True, help=u'The Channel [OCID].')
@cli_util.option('--target', type=custom_types.CLI_COMPLEX_TYPE, help=u'' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--display-name', help=u'The user-friendly name for the Channel. It does not have to be unique.')
@cli_util.option('--is-enabled', type=click.BOOL, help=u'Whether the Channel should be enabled or disabled. Enabling a previously disabled Channel will cause the Channel to be started. Conversely, disabling a previously enabled Channel will stop the Channel. Both operations are executed asynchronously.')
@cli_util.option('--description', help=u'User provided description of the Channel.')
@cli_util.option('--freeform-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u'Simple key-value pair applied without any predefined name, type or scope. Exists for cross-compatibility only. Example: `{"bar-key": "value"}`' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--defined-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u'Usage of predefined tag keys. These predefined keys are scoped to namespaces. Example: `{"foo-namespace": {"bar-key": "value"}}`' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--if-match', help=u"For optimistic concurrency control. In the PUT or DELETE call for a resource, set the `If-Match` header to the value of the etag from a previous GET or POST response for that resource. The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.")
@cli_util.option('--source-hostname', help=u'The network address of the MySQL instance.')
@cli_util.option('--source-port', type=click.INT, help=u'The port the source MySQL instance listens on.')
@cli_util.option('--source-username', help=u'The name of the replication user on the source MySQL instance. The username has a maximum length of 96 characters. For more information, please see the [MySQL documentation]')
@cli_util.option('--source-password', help=u'The password for the replication user. The password must be between 8 and 32 characters long, and must contain at least 1 numeric character, 1 lowercase character, 1 uppercase character, and 1 special (nonalphanumeric) character.')
@cli_util.option('--source-ssl-mode', help=u'The SSL mode of the Channel.')
@cli_util.option('--source-ssl-ca-certificate', type=custom_types.CLI_COMPLEX_TYPE, help=u'' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--source-anonymous-transactions-handling', type=custom_types.CLI_COMPLEX_TYPE, help=u'' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--force', help='Perform update without prompting for confirmation.', is_flag=True)
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(['ACCEPTED', 'IN_PROGRESS', 'FAILED', 'SUCCEEDED', 'CANCELING', 'CANCELED']), multiple=True, help='This operation asynchronously creates, modifies or deletes a resource and uses a work request to track the progress of the operation. Specify this option to perform the action and then wait until the work request reaches a certain state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.')
@cli_util.option('--max-wait-seconds', type=click.INT, help='The maximum time to wait for the work request to reach the state defined by --wait-for-state. Defaults to 1200 seconds.')
@cli_util.option('--wait-interval-seconds', type=click.INT, help='Check every --wait-interval-seconds to see whether the work request has reached the state defined by --wait-for-state. Defaults to 30 seconds.')
@json_skeleton_utils.get_cli_json_input_option({'target': {'module': 'mysql', 'class': 'UpdateChannelTargetDetails'}, 'freeform-tags': {'module': 'mysql', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'mysql', 'class': 'dict(str, dict(str, object))'}, 'source-ssl-ca-certificate': {'module': 'mysql', 'class': 'CaCertificate'}, 'source-anonymous-transactions-handling': {'module': 'mysql', 'class': 'AnonymousTransactionsHandling'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'target': {'module': 'mysql', 'class': 'UpdateChannelTargetDetails'}, 'freeform-tags': {'module': 'mysql', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'mysql', 'class': 'dict(str, dict(str, object))'}, 'source-ssl-ca-certificate': {'module': 'mysql', 'class': 'CaCertificate'}, 'source-anonymous-transactions-handling': {'module': 'mysql', 'class': 'AnonymousTransactionsHandling'}})
@cli_util.wrap_exceptions
def update_channel_update_channel_source_from_mysql_details(ctx, from_json, force, wait_for_state, max_wait_seconds, wait_interval_seconds, channel_id, target, display_name, is_enabled, description, freeform_tags, defined_tags, if_match, source_hostname, source_port, source_username, source_password, source_ssl_mode, source_ssl_ca_certificate, source_anonymous_transactions_handling):
    if isinstance(channel_id, six.string_types) and len(channel_id.strip()) == 0:
        raise click.UsageError('Parameter --channel-id cannot be whitespace or empty string')
    if not force:
        if target or freeform_tags or defined_tags:
            if not click.confirm('WARNING: Updates to target and freeform-tags and defined-tags will replace any existing values. Are you sure you want to continue?'):
                ctx.abort()
    kwargs = {}
    if if_match is not None:
        kwargs['if_match'] = if_match
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    _details = {}
    _details['source'] = {}
    if target is not None:
        _details['target'] = cli_util.parse_json_parameter('target', target)
    if display_name is not None:
        _details['displayName'] = display_name
    if is_enabled is not None:
        _details['isEnabled'] = is_enabled
    if description is not None:
        _details['description'] = description
    if freeform_tags is not None:
        _details['freeformTags'] = cli_util.parse_json_parameter('freeform_tags', freeform_tags)
    if defined_tags is not None:
        _details['definedTags'] = cli_util.parse_json_parameter('defined_tags', defined_tags)
    if source_hostname is not None:
        _details['source']['hostname'] = source_hostname
    if source_port is not None:
        _details['source']['port'] = source_port
    if source_username is not None:
        _details['source']['username'] = source_username
    if source_password is not None:
        _details['source']['password'] = source_password
    if source_ssl_mode is not None:
        _details['source']['sslMode'] = source_ssl_mode
    if source_ssl_ca_certificate is not None:
        _details['source']['sslCaCertificate'] = cli_util.parse_json_parameter('source_ssl_ca_certificate', source_ssl_ca_certificate)
    if source_anonymous_transactions_handling is not None:
        _details['source']['anonymousTransactionsHandling'] = cli_util.parse_json_parameter('source_anonymous_transactions_handling', source_anonymous_transactions_handling)
    _details['source']['sourceType'] = 'MYSQL'
    client = cli_util.build_client('mysql', 'channels', ctx)
    result = client.update_channel(channel_id=channel_id, update_channel_details=_details, **kwargs)
    if wait_for_state:
        client = cli_util.build_client('mysql', 'work_requests', ctx)
        if hasattr(client, 'get_work_request') and callable(getattr(client, 'get_work_request')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds
                click.echo('Action completed. Waiting until the work request has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_work_request(result.headers['opc-work-request-id']), 'status', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                click.echo('Failed to wait until the work request entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for work request to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the work request to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)

@channel_group.command(name=cli_util.override('channels.update_channel_update_channel_target_from_db_system_details.command_name', 'update-channel-update-channel-target-from-db-system-details'), help=u'Updates the properties of the specified Channel. If the Channel is Active the Update operation will asynchronously apply the new configuration parameters to the Channel and the Channel may become temporarily unavailable. Otherwise, the new configuration will be applied the next time the Channel becomes Active. \n[Command Reference](updateChannel)')
@cli_util.option('--channel-id', required=True, help=u'The Channel [OCID].')
@cli_util.option('--source', type=custom_types.CLI_COMPLEX_TYPE, help=u'' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--display-name', help=u'The user-friendly name for the Channel. It does not have to be unique.')
@cli_util.option('--is-enabled', type=click.BOOL, help=u'Whether the Channel should be enabled or disabled. Enabling a previously disabled Channel will cause the Channel to be started. Conversely, disabling a previously enabled Channel will stop the Channel. Both operations are executed asynchronously.')
@cli_util.option('--description', help=u'User provided description of the Channel.')
@cli_util.option('--freeform-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u'Simple key-value pair applied without any predefined name, type or scope. Exists for cross-compatibility only. Example: `{"bar-key": "value"}`' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--defined-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u'Usage of predefined tag keys. These predefined keys are scoped to namespaces. Example: `{"foo-namespace": {"bar-key": "value"}}`' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--if-match', help=u"For optimistic concurrency control. In the PUT or DELETE call for a resource, set the `If-Match` header to the value of the etag from a previous GET or POST response for that resource. The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.")
@cli_util.option('--target-channel-name', help=u'The case-insensitive name that identifies the replication channel. Channel names must follow the rules defined for [MySQL identifiers]. The names of non-Deleted Channels must be unique for each DB System.')
@cli_util.option('--target-applier-username', help=u'The username for the replication applier of the target MySQL DB System.')
@cli_util.option('--target-filters', type=custom_types.CLI_COMPLEX_TYPE, help=u'Replication filter rules to be applied at the DB System Channel target.\n\nThis option is a JSON list with items of type ChannelFilter.  For documentation on ChannelFilter please see our API reference: https://docs.cloud.oracle.com/api/#/en/channels/20190415/datatypes/ChannelFilter.' + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--force', help='Perform update without prompting for confirmation.', is_flag=True)
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(['ACCEPTED', 'IN_PROGRESS', 'FAILED', 'SUCCEEDED', 'CANCELING', 'CANCELED']), multiple=True, help='This operation asynchronously creates, modifies or deletes a resource and uses a work request to track the progress of the operation. Specify this option to perform the action and then wait until the work request reaches a certain state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.')
@cli_util.option('--max-wait-seconds', type=click.INT, help='The maximum time to wait for the work request to reach the state defined by --wait-for-state. Defaults to 1200 seconds.')
@cli_util.option('--wait-interval-seconds', type=click.INT, help='Check every --wait-interval-seconds to see whether the work request has reached the state defined by --wait-for-state. Defaults to 30 seconds.')
@json_skeleton_utils.get_cli_json_input_option({'source': {'module': 'mysql', 'class': 'UpdateChannelSourceDetails'}, 'freeform-tags': {'module': 'mysql', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'mysql', 'class': 'dict(str, dict(str, object))'}, 'target-filters': {'module': 'mysql', 'class': 'list[ChannelFilter]'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'source': {'module': 'mysql', 'class': 'UpdateChannelSourceDetails'}, 'freeform-tags': {'module': 'mysql', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'mysql', 'class': 'dict(str, dict(str, object))'}, 'target-filters': {'module': 'mysql', 'class': 'list[ChannelFilter]'}})
@cli_util.wrap_exceptions
def update_channel_update_channel_target_from_db_system_details(ctx, from_json, force, wait_for_state, max_wait_seconds, wait_interval_seconds, channel_id, source, display_name, is_enabled, description, freeform_tags, defined_tags, if_match, target_channel_name, target_applier_username, target_filters):
    if isinstance(channel_id, six.string_types) and len(channel_id.strip()) == 0:
        raise click.UsageError('Parameter --channel-id cannot be whitespace or empty string')
    if not force:
        if source or freeform_tags or defined_tags:
            if not click.confirm('WARNING: Updates to source and freeform-tags and defined-tags will replace any existing values. Are you sure you want to continue?'):
                ctx.abort()
    kwargs = {}
    if if_match is not None:
        kwargs['if_match'] = if_match
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    _details = {}
    _details['target'] = {}
    if source is not None:
        _details['source'] = cli_util.parse_json_parameter('source', source)
    if display_name is not None:
        _details['displayName'] = display_name
    if is_enabled is not None:
        _details['isEnabled'] = is_enabled
    if description is not None:
        _details['description'] = description
    if freeform_tags is not None:
        _details['freeformTags'] = cli_util.parse_json_parameter('freeform_tags', freeform_tags)
    if defined_tags is not None:
        _details['definedTags'] = cli_util.parse_json_parameter('defined_tags', defined_tags)
    if target_channel_name is not None:
        _details['target']['channelName'] = target_channel_name
    if target_applier_username is not None:
        _details['target']['applierUsername'] = target_applier_username
    if target_filters is not None:
        _details['target']['filters'] = cli_util.parse_json_parameter('target_filters', target_filters)
    _details['target']['targetType'] = 'DBSYSTEM'
    client = cli_util.build_client('mysql', 'channels', ctx)
    result = client.update_channel(channel_id=channel_id, update_channel_details=_details, **kwargs)
    if wait_for_state:
        client = cli_util.build_client('mysql', 'work_requests', ctx)
        if hasattr(client, 'get_work_request') and callable(getattr(client, 'get_work_request')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds
                click.echo('Action completed. Waiting until the work request has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_work_request(result.headers['opc-work-request-id']), 'status', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                click.echo('Failed to wait until the work request entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for work request to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the work request to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)