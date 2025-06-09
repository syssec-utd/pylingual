"""Kat script command line interface."""
import click
from .. import __version__, PROGRAM
from ..cli import KatState, plot_graph, input_file_argument, graph_layout_argument, graphviz_option, verbose_option, quiet_option, debug_option, log_display_level_option, log_exclude_option
from .exceptions import KatScriptError
BOUND_WIDTH = 18

@click.group(help='Kat script interface.')
@click.version_option(version=__version__, prog_name=PROGRAM)
@click.pass_context
def kat_script(ctx):
    pass

@kat_script.command()
@input_file_argument
@click.option('--raw', is_flag=True, default=False, help='Show raw tokens.')
@verbose_option
@quiet_option
@debug_option
@log_display_level_option
@log_exclude_option
@click.pass_context
def tokenize(ctx, input_file, raw):
    """Tokenize a Finesse script."""
    from .tokenizer import KatTokenizer

    def print_tokens(tokens):
        for token in tokens:
            value = repr(token) if raw else str(token)
            state.print(f'{token.bounds!s:>{BOUND_WIDTH}} {value}')
    state = ctx.ensure_object(KatState)
    state.print_banner(input_file)
    tokenizer = KatTokenizer()
    try:
        tokens = list(tokenizer.tokenize_file(input_file))
    except KatScriptError as e:
        state.print_error(e)
    state.print('Tokens:')
    print_tokens(tokens)

@kat_script.command()
@input_file_argument
@click.option('--raw', is_flag=True, default=False, help='Show raw parsed productions.')
@verbose_option
@quiet_option
@debug_option
@log_display_level_option
@log_exclude_option
@click.pass_context
def parse(ctx, input_file, raw):
    """Parse a Finesse script and display items."""
    state = ctx.ensure_object(KatState)
    state.print_banner(input_file)
    from .parser import KatParser
    parser = KatParser()
    try:
        script = parser.parse_file(input_file)
    except KatScriptError as e:
        state.print_error(e)
    state.print('Script statements:')
    if script.arguments:
        for item in script.arguments:
            value = repr(item) if raw else str(item)
            state.print(f'{item.bounds!s:>{BOUND_WIDTH}} {value}')
    else:
        state.print('*none*')
    state.print()
    state.print('Script extra tokens:')
    if script.extra:
        for extra in script.extra:
            if raw:
                state.print(repr(extra))
            else:
                state.print(f'{extra.bounds!s:>{BOUND_WIDTH}} {extra}')
    else:
        state.print('*none*')

@kat_script.command()
@input_file_argument
@click.option('--resolve/--no-resolve', is_flag=True, default=True, help='Resolve model references.')
@click.option('--build/--no-build', is_flag=True, default=True, help='Build the model.')
@click.option('--graph', is_flag=True, default=False, help='Show graph.')
@click.option('--dump-graph', is_flag=True, default=False, help='Dump the graph to GML markup.')
@click.option('--build-order', is_flag=True, default=False, help='Show only the build graph.')
@click.option('--node-labels', is_flag=True, default=True, help='Show node labels.')
@click.option('--node-attr', multiple=True, help='Show node attribute. Can be specified multiple times. If not specified, all attributes are shown.')
@click.option('--edge-attr', multiple=True, help='Show edge attribute. Can be specified multiple times. If not specified, all attributes are shown.')
@graph_layout_argument
@graphviz_option
@verbose_option
@quiet_option
@debug_option
@log_display_level_option
@log_exclude_option
@click.pass_context
def compile(ctx, input_file, resolve, build, graph, dump_graph, build_order, node_labels, node_attr, edge_attr, layout, graphviz):
    """Compile a Finesse script and display the model."""
    from .compiler import KatCompiler
    state = ctx.ensure_object(KatState)
    state.print_banner(input_file)
    compiler = KatCompiler()
    model = compiler.compile_file(input_file, resolve=resolve, build=build)
    if model:
        state.print(model.info())
    if graph:
        view_graph = compiler.build_graph if build_order else compiler.graph
        if dump_graph:
            from finesse.utilities import stringify_graph_gml
            state.print(stringify_graph_gml(view_graph))
        if not node_attr:
            node_attr = True
        if not edge_attr:
            edge_attr = True
        kwargs = {}
        if not graphviz:
            kwargs = {**kwargs, 'node_color_key': lambda node, data: data['type'], 'edge_color_key': lambda edge, data: data['type'], 'node_labels': node_labels, 'node_attrs': node_attr, 'edge_attrs': edge_attr}
        plot_graph(state, view_graph, layout, graphviz=graphviz, **kwargs)

@kat_script.command()
@input_file_argument
@click.option('--graph', is_flag=True, default=False, help='Show graph.')
@click.option('--dump-graph', is_flag=True, default=False, help='Dump the graph to GML markup.')
@click.option('--node-labels', is_flag=True, default=True, help='Show node labels.')
@click.option('--node-attr', multiple=True, help='Show node attribute. Can be specified multiple times. If not specified, all attributes are shown.')
@click.option('--edge-attr', multiple=True, help='Show edge attribute. Can be specified multiple times. If not specified, all attributes are shown.')
@graph_layout_argument
@graphviz_option
@verbose_option
@quiet_option
@debug_option
@log_display_level_option
@log_exclude_option
@click.pass_context
def normalise(ctx, input_file, graph, dump_graph, node_labels, node_attr, edge_attr, layout, graphviz):
    """Compile a Finesse script and print normalised kat script."""
    from .compiler import KatCompiler
    from .generator import KatUnbuilder
    state = ctx.ensure_object(KatState)
    state.print_banner(input_file)
    compiler = KatCompiler()
    model = compiler.compile_file(input_file)
    unbuilder = KatUnbuilder()
    script = unbuilder.unbuild(model)
    state.print(script)
    if graph:
        view_graph = unbuilder.graph
        if dump_graph:
            from finesse.utilities import stringify_graph_gml
            state.print(stringify_graph_gml(view_graph))
        if not node_attr:
            node_attr = True
        if not edge_attr:
            edge_attr = True
        kwargs = {}
        if not graphviz:
            kwargs['node_color_key'] = lambda node, data: data['type']
        plot_graph(state, view_graph, layout, node_labels=node_labels, node_attrs=node_attr, edge_attrs=edge_attr, graphviz=graphviz, **kwargs)

@kat_script.command()
@verbose_option
@quiet_option
@debug_option
@click.pass_context
def shell(ctx):
    """Start an interactive Finesse shell."""
    from ..script.shell import KatShell
    repl = KatShell()
    repl.cmdloop()
if __name__ == '__main__':
    kat_script()