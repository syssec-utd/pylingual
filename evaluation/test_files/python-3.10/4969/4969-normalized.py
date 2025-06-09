def setup_cmd_parser(cls):
    """Returns the Gerrit argument parser."""
    parser = BackendCommandArgumentParser(cls.BACKEND.CATEGORIES, from_date=True, archive=True)
    group = parser.parser.add_argument_group('Gerrit arguments')
    group.add_argument('--user', dest='user', help='Gerrit ssh user')
    group.add_argument('--max-reviews', dest='max_reviews', type=int, default=MAX_REVIEWS, help='Max number of reviews per ssh query.')
    group.add_argument('--blacklist-reviews', dest='blacklist_reviews', nargs='*', help='Wrong reviews that must not be retrieved.')
    group.add_argument('--disable-host-key-check', dest='disable_host_key_check', action='store_true', help="Don't check remote host identity")
    group.add_argument('--ssh-port', dest='port', default=PORT, type=int, help='Set SSH port of the Gerrit server')
    parser.parser.add_argument('hostname', help='Hostname of the Gerrit server')
    return parser