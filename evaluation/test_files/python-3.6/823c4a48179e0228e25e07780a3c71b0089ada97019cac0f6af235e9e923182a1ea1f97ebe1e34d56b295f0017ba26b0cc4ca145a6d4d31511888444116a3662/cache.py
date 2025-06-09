import click
from rich import print
from ..utils.cache import CACHE_DIR
from ..utils.remove import remove

@click.command(name='clean')
def cmd_cache_clean() -> None:
    remove(CACHE_DIR)

@click.command(name='prefix')
def cmd_cache_prefix() -> None:
    print(CACHE_DIR)

@click.group(name='cache', invoke_without_command=True)
@click.pass_context
def cmd_cache(ctx: click.Context) -> None:
    if not ctx.invoked_subcommand:
        ctx.invoke(cmd_cache_prefix)
cmd_cache.add_command(cmd=cmd_cache_clean)
cmd_cache.add_command(cmd=cmd_cache_prefix)