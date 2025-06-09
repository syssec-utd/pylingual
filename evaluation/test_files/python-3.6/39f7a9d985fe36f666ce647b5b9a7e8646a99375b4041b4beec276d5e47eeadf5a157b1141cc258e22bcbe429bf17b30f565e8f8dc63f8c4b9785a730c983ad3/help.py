from ..automatoes import AutomatoesCliContext, pass_context
import click

@click.command(short_help='Show the list of commands')
@pass_context
def commands(ctx: AutomatoesCliContext):
    rv = []
    groups = []
    for source in ctx.context.loader.sources:
        for (key, item) in source.__dict__.items():
            if isinstance(item, click.Command):
                if isinstance(item, click.Group):
                    groups.append(item)
                rv.append(item.name)
    for group in groups:
        for (key, item) in group.commands.items():
            if item.name in rv:
                rv.remove(item.name)
    rv.sort()
    print(rv)
    print(groups)
    print('Test cli1 command')

@click.command(name='help', short_help='Show the help about a command')
def _help():
    print('Test cli1 command')