import typer
from meutils.pipe import *
cli = typer.Typer(name='llm4gpt CLI')

@cli.command(help='help')
def clitest(name: str='TEST'):
    """

    @param name: name
    @return:
    """
    typer.echo(f'Hello {name}')
if __name__ == '__main__':
    cli()