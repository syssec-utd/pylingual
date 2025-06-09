def main():
    """
    Main Entry point for translator and argument parser
    """
    args = command_line()
    translate = partial(translator, args.source, args.dest, version=' '.join([__version__, __build__]))
    return source(spool(set_task(translate, translit=args.translit)), args.text)