from __future__ import annotations

from typing import TYPE_CHECKING, override

import networkx as nx

from ..cft import ControlFlowTemplate, register_template

if TYPE_CHECKING:
    from pylingual.control_flow_reconstruction.cfg import CFG


# it's better than nothing
@register_template(101, 0)
class CDG(ControlFlowTemplate):
    def __init__(self, cfg: CFG):
        self.cdg = cfg.cdg()
        self.start = cfg.start
        self.blame = cfg.start.blame
        self.header_lines = self.line("# irreducible cflow, using cdg fallback", meta=True)

    @override
    @classmethod
    def try_match(cls, cfg: CFG, node: ControlFlowTemplate) -> ControlFlowTemplate | None:
        cdg = CDG(cfg)

        if cfg.visualize == cfg._visualize:
            cfg.remove_edges_from(list(cfg.edges))
            cfg.add_edges_from(cdg.cdg.edges(data=True))
            cfg.remove_node(cfg.end)
            cfg.layout_nodes()
            cfg.visualize()

        cfg.clear()
        cfg.add_node(cdg)
        for p, n in nx.dfs_edges(cdg.cdg, cfg.start):
            cdg.cdg.nodes[n]["indent"] = cdg.cdg.nodes[p].get("indent", -1) + 1
        cdg.cdg.remove_node(cfg.start)
        return cdg

    @override
    def get_instructions(self):
        return []

    @override
    def to_indented_source(self, source):
        src = []
        for n in sorted(self.cdg.nodes, key=lambda x: x.offset):
            src.extend(source[n, self.cdg.nodes[n].get("indent", 0)])
        return src
