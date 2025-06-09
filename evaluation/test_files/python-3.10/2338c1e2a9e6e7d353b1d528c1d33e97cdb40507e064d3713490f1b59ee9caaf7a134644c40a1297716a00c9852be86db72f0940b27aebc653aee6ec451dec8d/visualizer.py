"""
    This file is part of PM4Py (More Info: https://pm4py.fit.fraunhofer.de).

    PM4Py is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    PM4Py is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with PM4Py.  If not, see <https://www.gnu.org/licenses/>.
"""
from enum import Enum
from typing import Optional, Dict, Any
from graphviz import Graph
from pm4py.objects.trie.obj import Trie
from pm4py.util import exec_utils
from pm4py.visualization.common import gview
from pm4py.visualization.common import save as gsave
from pm4py.visualization.trie.variants import classic

class Variants(Enum):
    CLASSIC = classic

def apply(trie: Trie, variant=Variants.CLASSIC, parameters: Optional[Dict[Any, Any]]=None) -> Graph:
    """
    Represents the trie

    Parameters
    -----------------
    trie
        Trie
    variant
        Variant of the visualization, possible values:
        - Variants.CLASSIC => graphviz visualization
    parameters
        Parameters, including:
        - Parameters.FORMAT: the format of the visualization

    Returns
    -----------------
    graph
        Representation of the trie
    """
    return exec_utils.get_variant(variant).apply(trie, parameters=parameters)

def save(gviz: Graph, output_file_path: str):
    """
    Save the diagram

    Parameters
    -----------
    gviz
        GraphViz diagram
    output_file_path
        Path where the GraphViz output should be saved
    """
    gsave.save(gviz, output_file_path)

def view(gviz: Graph):
    """
    View the diagram

    Parameters
    -----------
    gviz
        GraphViz diagram
    """
    return gview.view(gviz)

def matplotlib_view(gviz: Graph):
    """
    Views the diagram using Matplotlib

    Parameters
    ---------------
    gviz
        Graphviz
    """
    return gview.matplotlib_view(gviz)