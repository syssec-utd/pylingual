def setup_cmd_parser(cls):
    """Returns the GitLab argument parser."""
    parser = BackendCommandArgumentParser(cls.BACKEND.CATEGORIES, from_date=True, token_auth=True, archive=True)
    group = parser.parser.add_argument_group('GitLab arguments')
    group.add_argument('--enterprise-url', dest='base_url', help='Base URL for GitLab Enterprise instance')
    group.add_argument('--sleep-for-rate', dest='sleep_for_rate', action='store_true', help='sleep for getting more rate')
    group.add_argument('--min-rate-to-sleep', dest='min_rate_to_sleep', default=MIN_RATE_LIMIT, type=int, help='sleep until reset when the rate limit                                reaches this value')
    group.add_argument('--blacklist-ids', dest='blacklist_ids', nargs='*', type=int, help='Ids of items that must not be retrieved.')
    group.add_argument('--max-retries', dest='max_retries', default=MAX_RETRIES, type=int, help='number of API call retries')
    group.add_argument('--sleep-time', dest='sleep_time', default=DEFAULT_SLEEP_TIME, type=int, help='sleeping time between API call retries')
    parser.parser.add_argument('owner', help='GitLab owner')
    parser.parser.add_argument('repository', help='GitLab repository')
    return parser