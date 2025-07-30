from pylingual.editable_bytecode import EditableBytecode
from pylingual.editable_bytecode.control_flow_graph import bytecode_to_control_flow_graph


import networkx as nx

from .cfg import CFG
from .cft import ControlFlowTemplate, get_template_runs, MetaTemplate


def iteration(cfg: CFG, runs: list[list[type[ControlFlowTemplate]]]):
    for cfg.run, run in enumerate(runs):
        for node in cfg.ordered_iter():
            for template in run:
                if template.try_match(cfg, node):
                    return True
    return False


def bc_to_cft(bc: EditableBytecode):
    return structure_control_flow(bytecode_to_control_flow_graph(bc), bc)


def structure_control_flow(cfg: nx.DiGraph, bytecode: EditableBytecode) -> ControlFlowTemplate:
    cfg = CFG.from_graph(cfg, bytecode)
    runs = get_template_runs(bytecode.version[:2])

    while len(cfg) > 1:
        if not iteration(cfg, runs):
            return MetaTemplate("\x1b[31mirreducible cflow\x1b[0m", bytecode.codeobj)

    return next(iter(cfg.nodes))
