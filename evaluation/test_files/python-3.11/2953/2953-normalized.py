def fetch_streams(plugin):
    """Fetches streams using correct parameters."""
    return plugin.streams(stream_types=args.stream_types, sorting_excludes=args.stream_sorting_excludes)