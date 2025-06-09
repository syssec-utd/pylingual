def parse_perfmetric(metric):
    """Return (sympy expressions, event names and symbols dict) from performance metric str."""
    perfcounters = re.findall('[A-Z0-9_]+:[A-Z0-9\\[\\]|\\-]+(?::[A-Za-z0-9\\-_=]+)*', metric)
    temp_metric = metric
    temp_pc_names = {'SYM{}'.format(re.sub('[\\[\\]\\-|=:]', '_', pc)): pc for (i, pc) in enumerate(perfcounters)}
    for (var_name, pc) in temp_pc_names.items():
        temp_metric = temp_metric.replace(pc, var_name)
    expr = parse_expr(temp_metric)
    for s in expr.free_symbols:
        if s.name in temp_pc_names:
            s.name = temp_pc_names[str(s)]
    events = {s: MachineModel.parse_perfctr_event(s.name) for s in expr.free_symbols if s.name in perfcounters}
    return (expr, events)