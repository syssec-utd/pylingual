import typer
from gtdblib import __version__, log
from gtdblib.cli.tree import app as tree_app
from gtdblib.exception import GtdbLibExit
app = typer.Typer(context_settings={'help_option_names': ['-h', '--help']}, rich_markup_mode='rich')

def version_callback(value: bool):
    if value:
        typer.echo(f'gtdblib: {__version__}')
        raise typer.Exit()

@app.callback()
def common(ctx: typer.Context, version: bool=typer.Option(None, '--version', '-v', callback=version_callback)):
    pass
app.add_typer(tree_app, name='tree', help='Commands for working with Newick trees.')

def main():
    """
    The main method that wraps all logic for the CLI.
    """
    try:
        app()
    except GtdbLibExit as e:
        log.error(e)
        typer.Exit(1)
if __name__ == '__main__':
    main()