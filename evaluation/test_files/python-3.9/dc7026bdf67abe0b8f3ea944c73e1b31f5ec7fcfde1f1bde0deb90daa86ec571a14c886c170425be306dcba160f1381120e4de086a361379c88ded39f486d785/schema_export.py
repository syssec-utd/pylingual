"""Export the schema diagram."""
import click
from networkx.drawing.nx_agraph import to_agraph
from bioregistry.constants import SCHEMA_PDF_PATH, SCHEMA_SVG_PATH
from bioregistry.schema.constants import get_schema_nx

@click.command()
def schema_export():
    """Export the schema diagram."""
    agraph = to_agraph(get_schema_nx())
    agraph.layout(prog='dot')
    agraph.draw(SCHEMA_SVG_PATH)
    agraph.draw(SCHEMA_PDF_PATH)
if __name__ == '__main__':
    schema_export()