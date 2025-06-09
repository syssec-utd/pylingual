import sys
import time
from functools import partial
import anyio
import asyncclick as click
from moat.util import P, Path, attr_args, attrdict, process_args, yprint
from distkv.code import CodeRoot
from distkv.data import add_dates, data_get
from distkv.runner import AllRunnerRoot, AnyRunnerRoot, SingleRunnerRoot

@click.group()
@click.option('-n', '--node', help="node to run this code on. Empty: any one node, '-': all nodes")
@click.option('-g', '--group', help='group to run this code on. Empty: default')
@click.pass_context
async def cli(ctx, node, group):
    """Run code stored in DistKV.

    \x08
    The option '-n' is somewhat special:
    -n -     Jobs for all hosts
    -n XXX   Jobs for host XXX
    (no -n)  Jobs for any host

    The default group is 'default'.
    """
    obj = ctx.obj
    if group is None:
        group = 'default'
    if group == '-':
        if node is not None:
            raise click.UsageError("'-g -' doesn't make sense with '-n'")
        if ctx.invoked_subcommand != 'info':
            raise click.UsageError("'-g -' only makes sense with the 'info' command")
        obj.runner_root = SingleRunnerRoot
        subpath = (None,)
    elif not node:
        obj.runner_root = AnyRunnerRoot
        subpath = (group,)
    elif node == '-':
        obj.runner_root = AllRunnerRoot
        subpath = (group,)
    else:
        obj.runner_root = SingleRunnerRoot
        subpath = (node, group)
    obj.subpath = Path(obj.cfg['runner']['sub'][obj.runner_root.SUB]) + subpath
    obj.path = obj.cfg['runner']['prefix'] + obj.subpath
    obj.statepath = obj.cfg['runner']['state'] + obj.subpath

@cli.group('at', short_help='path of the job to operate on', invoke_without_command=True)
@click.argument('path', nargs=1, type=P)
@click.pass_context
async def at_cli(ctx, path):
    """
    Add, list, modify, delete jobs at/under this path.
    """
    obj = ctx.obj
    obj.jobpath = path
    if ctx.invoked_subcommand is None:
        res = await obj.client.get(obj.path + path, nchain=obj.meta)
        yprint(res, stream=obj.stdout)

@cli.command('info')
@click.pass_obj
async def info_(obj):
    """
    List available groups for the node in question.

    \x08
    Options (between 'job' and 'info')
    (none)    list groups with jobs for any host
    -n -      list groups with jobs for all hosts
    -g -      list hosts that have specific jobs
    -n XXX    list groups with jobs for a specific host
    """
    path = obj.path[:-1]
    async for r in obj.client.get_tree(path=path, min_depth=1, max_depth=1, empty=True):
        print(r.path[-1], file=obj.stdout)

@at_cli.command('--help', hidden=True)
@click.pass_context
def help_(ctx):
    print(at_cli.get_help(ctx))

@at_cli.command('path')
@click.pass_obj
async def path__(obj):
    """
    Emit the full path leading to the specified runner object.

    Useful for copying or for state monitoring.

    NEVER directly write to the state object. It's controlled by the
    runner. You'll confuse it if you do that.

    Updating the control object will cancel any running code.
    """
    path = obj.jobpath
    res = dict(command=obj.path + path, state=obj.statepath + path)
    yprint(res, stream=obj.stdout)

@cli.command('run')
@click.option('-n', '--nodes', type=int, default=0, help='Size of the group (not for single-node runners)')
@click.pass_obj
async def run(obj, nodes):
    """
    Run code that needs to run.

    This does not return.
    """
    from moat.util import as_service
    if obj.subpath[-1] == '-':
        raise click.UsageError("Group '-' can only be used for listing.")
    if nodes and obj.runner_root == SingleRunnerRoot:
        raise click.UsageError("A single-site runner doesn't have a size.")
    async with as_service(obj) as evt:
        c = obj.client
        cr = await CodeRoot.as_handler(c)
        await obj.runner_root.as_handler(c, subpath=obj.subpath, code=cr, **{'nodes': nodes} if nodes else {})
        evt.set()
        while True:
            await anyio.sleep(99999)

async def _state_fix(obj, state, state_only, path, r):
    try:
        val = r.value
    except AttributeError:
        return
    if state:
        rs = await obj.client._request(action='get_value', path=state + r.path, iter=False, nchain=obj.meta)
        if state_only:
            r.value = rs
        elif obj.meta:
            val['state'] = rs
        elif 'value' in rs:
            val['state'] = rs.value
        if 'value' in rs:
            add_dates(rs.value)
    if not state_only:
        if path:
            r.path = path + r.path
        add_dates(val)
    return r

@at_cli.command('list')
@click.option('-s', '--state', is_flag=True, help='Add state data')
@click.option('-S', '--state-only', is_flag=True, help='Only output state data')
@click.option('-t', '--table', is_flag=True, help='one-line output')
@click.option('-d', '--as-dict', default=None, help='Structure as dictionary. The argument is the key to use for values. Default: return as list')
@click.pass_obj
async def list_(obj, state, state_only, table, as_dict):
    """List run entries."""
    if table and state:
        click.UsageError("'--table' and '--state' are mutually exclusive")
    path = obj.jobpath
    if state or state_only or table:
        state = obj.statepath + path
    if table:
        from distkv.errors import ErrorRoot
        err = await ErrorRoot.as_handler(obj.client)
        async for r in obj.client.get_tree(obj.path + path):
            p = path + r.path
            s = await obj.client.get(state + r.path)
            if 'value' not in s:
                st = '-never-'
            elif s.value.started > s.value.stopped:
                st = s.value.node
            else:
                try:
                    e = await err.get_error_record('run', obj.path + p, create=False)
                except KeyError:
                    st = '-stopped-'
                else:
                    if e is None or e.resolved:
                        st = '-stopped-'
                    else:
                        st = ' | '.join(('%s %s' % (Path.build(e.subpath) if e._path[-2] == ee._path[-1] else Path.build(ee.subpath), getattr(ee, 'message', None) or getattr(ee, 'comment', None) or '-') for ee in e))
            print(p, r.value.code, st, file=obj.stdout)
    else:
        await data_get(obj, obj.path + path, as_dict=as_dict, item_mangle=partial(_state_fix, obj, state, state_only, None if as_dict else path))

@at_cli.command('state')
@click.option('-r', '--result', is_flag=True, help='Just print the actual result.')
@click.pass_obj
async def state_(obj, result):
    """Get the status of a runner entry."""
    path = obj.jobpath
    if obj.subpath[-1] == '-':
        raise click.UsageError("Group '-' can only be used for listing.")
    if result and obj.meta:
        raise click.UsageError("You can't use '-v' and '-r' at the same time.")
    if not len(path):
        raise click.UsageError('You need a non-empty path.')
    path = obj.statepath + obj.jobpath
    res = await obj.client.get(path, nchain=obj.meta)
    if 'value' not in res:
        if obj.debug:
            print('Not found (yet?)', file=sys.stderr)
        sys.exit(1)
    add_dates(res.value)
    if not obj.meta:
        res = res.value
    yprint(res, stream=obj.stdout)

@at_cli.command()
@click.option('-s', '--state', is_flag=True, help='Add state data')
@click.pass_obj
async def get(obj, state):
    """Read a runner entry"""
    path = obj.jobpath
    if obj.subpath[-1] == '-':
        raise click.UsageError("Group '-' can only be used for listing.")
    if not path:
        raise click.UsageError('You need a non-empty path.')
    res = await obj.client._request(action='get_value', path=obj.path + path, iter=False, nchain=obj.meta)
    if 'value' not in res:
        print('Not found.', file=sys.stderr)
        return
    res.path = path
    if state:
        state = obj.statepath
    await _state_fix(obj, state, False, path, res)
    if not obj.meta:
        res = res.value
    yprint(res, stream=obj.stdout)

@at_cli.command()
@click.option('-f', '--force', is_flag=True, help='Force deletion even if messy')
@click.pass_obj
async def delete(obj, force):
    """Remove a runner entry"""
    path = obj.jobpath
    if obj.subpath[-1] == '-':
        raise click.UsageError("Group '-' can only be used for listing.")
    if not path:
        raise click.UsageError('You need a non-empty path.')
    res = await obj.client.get(obj.path + path, nchain=3)
    if 'value' not in res:
        res.info = 'Does not exist.'
    else:
        val = res.value
        if 'target' not in val:
            val.target = None
        if val.target is not None:
            val.target = None
            res = await obj.client.set(obj.path + path, value=val, nchain=3, chain=res.chain)
            if not force:
                res.info = "'target' was set: cleared but not deleted."
        if force or val.target is None:
            sres = await obj.client.get(obj.statepath + path, nchain=3)
            if not force and 'value' in sres and (sres.value.stopped < sres.value.started):
                res.info = 'Still running, not deleted.'
            else:
                sres = await obj.client.delete(obj.statepath + path, chain=sres.chain)
                res = await obj.client.delete(obj.path + path, chain=res.chain)
                if 'value' in res and res.value.stopped < res.value.started:
                    res.info = 'Deleted (unclean!).'
                else:
                    res.info = 'Deleted.'
    if obj.meta:
        yprint(res, stream=obj.stdout)
    elif obj.debug:
        print(res.info)

@at_cli.command('set')
@click.option('-c', '--code', help='Path to the code that should run.')
@click.option('-C', '--copy', help='Use this entry as a template.')
@click.option('-t', '--time', 'tm', help="time the code should next run at. '-':not")
@click.option('-r', '--repeat', type=int, help='Seconds the code should re-run after')
@click.option('-k', '--ok', type=float, help='Code is OK if it ran this many seconds')
@click.option('-b', '--backoff', type=float, help='Back-off factor. Default: 1.4')
@click.option('-d', '--delay', type=int, help='Seconds the code should retry after (w/ backoff)')
@click.option('-i', '--info', help='Short human-readable information')
@attr_args
@click.pass_obj
async def set_(obj, code, tm, info, ok, repeat, delay, backoff, copy, vars_, eval_, path_):
    """Add or modify a runner.

    Code typically requires some input parameters.

    You should use '-v NAME VALUE' for string values, '-p NAME VALUE' for
    paths, and '-e NAME VALUE' for other data. '-e NAME -' deletes an item.
    """
    path = obj.jobpath
    if obj.subpath[-1] == '-':
        raise click.UsageError("Group '-' can only be used for listing.")
    if code is not None:
        code = P(code)
    if copy:
        copy = P(copy)
    path = obj.path + P(path)
    res = await obj.client._request(action='get_value', path=copy or path, iter=False, nchain=3)
    if 'value' not in res:
        if copy:
            raise click.UsageError('--copy: use the complete path to an existing entry')
        elif code is None:
            raise click.UsageError('New entry, need code')
        res = {}
        chain = None
    else:
        chain = None if copy else res['chain']
        res = res['value']
        if copy and 'code' not in res:
            raise click.UsageError("'--copy' needs a runner entry")
    vl = attrdict(**res.setdefault('data', {}))
    vl = process_args(vl, vars_, eval_, path_)
    res['data'] = vl
    if code is not None:
        res['code'] = code
    if ok is not None:
        res['ok_after'] = ok
    if info is not None:
        res['info'] = info
    if backoff is not None:
        res['backoff'] = backoff
    if delay is not None:
        res['delay'] = delay
    if repeat is not None:
        res['repeat'] = repeat
    if tm is not None:
        if tm == '-':
            res['target'] = None
        else:
            res['target'] = time.time() + float(tm)
    res = await obj.client.set(path, value=res, nchain=3, chain=chain)
    if obj.meta:
        yprint(res, stream=obj.stdout)

@cli.command(short_help="Show runners' keepalive messages")
@click.pass_obj
async def monitor(obj):
    """
    Runners periodically send a keepalive message. Show them.
    """
    if obj.subpath[-1] == '-':
        raise click.UsageError("Group '-' can only be used for listing.")
    async with obj.client.msg_monitor('run') as cl:
        async for msg in cl:
            yprint(msg, stream=obj.stdout)
            print('---', file=obj.stdout)