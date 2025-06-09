import click

@click.command()
@click.argument('payoff', type=float)
def be(payoff):
    """comando be (break-even)."""
    breakeven = 100 / (payoff + 1)
    click.echo('%.1f payoff' % payoff)
    click.echo('%i%% taxa de acerto do break even' % breakeven)
    return 0
if __name__ == '__main__':
    be()