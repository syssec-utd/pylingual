def main():
    """
    Parse command line options and launch the interpreter
    """
    parser = optparse.OptionParser(usage='%prog [options] <model_path> [another_model_path..]', version=xtuml.version.complete_string, formatter=optparse.TitledHelpFormatter())
    parser.add_option('-v', '--verbosity', dest='verbosity', action='count', default=1, help='increase debug logging level')
    parser.add_option('-f', '--function', dest='function', action='store', help='invoke function named NAME', metavar='NAME')
    parser.add_option('-c', '--component', dest='component', action='store', help='look for the function in a component named NAME', metavar='NAME', default=None)
    opts, args = parser.parse_args()
    if len(args) == 0 or not opts.function:
        parser.print_help()
        sys.exit(1)
    levels = {0: logging.ERROR, 1: logging.WARNING, 2: logging.INFO, 3: logging.DEBUG}
    logging.basicConfig(level=levels.get(opts.verbosity, logging.DEBUG))
    from bridgepoint import ooaofooa
    mm = ooaofooa.load_metamodel(args)
    c_c = mm.select_any('C_C', where(Name=opts.component))
    domain = ooaofooa.mk_component(mm, c_c, derived_attributes=False)
    func = domain.find_symbol(opts.function)
    return func()