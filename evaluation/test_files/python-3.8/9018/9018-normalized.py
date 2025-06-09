def _main(argv):
    """
    Handle arguments for the 'lumi-download' command.
    """
    parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-b', '--base-url', default=URL_BASE, help='API root url, default: %s' % URL_BASE)
    parser.add_argument('-e', '--expanded', help="Include Luminoso's analysis of each document, such as terms and document vectors", action='store_true')
    parser.add_argument('-t', '--token', help='API authentication token')
    parser.add_argument('-s', '--save-token', action='store_true', help='save --token for --base-url to ~/.luminoso/tokens.json')
    parser.add_argument('project_id', help='The ID of the project in the Daylight API')
    parser.add_argument('output_file', nargs='?', default=None, help='The JSON lines (.jsons) file to write to')
    args = parser.parse_args(argv)
    if args.save_token:
        if not args.token:
            raise ValueError('error: no token provided')
        LuminosoClient.save_token(args.token, domain=urlparse(args.base_url).netloc)
    client = LuminosoClient.connect(url=args.base_url, token=args.token)
    proj_client = client.client_for_path('projects/{}'.format(args.project_id))
    download_docs(proj_client, args.output_file, args.expanded)