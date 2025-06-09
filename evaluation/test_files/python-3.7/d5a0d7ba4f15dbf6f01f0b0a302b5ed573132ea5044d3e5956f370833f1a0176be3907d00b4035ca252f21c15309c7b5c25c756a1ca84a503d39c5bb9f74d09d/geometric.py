"""
Generators for some directed graphs, including growing network (GN) graphs and
scale-free graphs.

"""
import networkx.generators.geometric
from graphscope.framework.errors import UnimplementedError
from graphscope.nx.utils.compat import import_as_graphscope_nx
import_as_graphscope_nx(networkx.generators.geometric)

def navigable_small_world_graph(n, p=1, q=1, r=2, dim=2, seed=None):
    raise UnimplementedError('navigable_small_world_graph not support in graphscope.nx')