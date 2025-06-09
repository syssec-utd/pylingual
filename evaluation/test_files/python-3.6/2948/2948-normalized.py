def output_stream_passthrough(plugin, stream):
    """Prepares a filename to be passed to the player."""
    global output
    title = create_title(plugin)
    filename = '"{0}"'.format(stream_to_url(stream))
    output = PlayerOutput(args.player, args=args.player_args, filename=filename, call=True, quiet=not args.verbose_player, title=title)
    try:
        log.info('Starting player: {0}', args.player)
        output.open()
    except OSError as err:
        console.exit('Failed to start player: {0} ({1})', args.player, err)
        return False
    return True