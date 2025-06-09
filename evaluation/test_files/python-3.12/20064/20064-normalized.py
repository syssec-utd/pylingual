def run(locations, random, bikes, crime, nearby, json, update_bikes, api_server, cross_origin, host, port, db_path, verbose):
    """
    Runs the program. Takes a list of postcodes or coordinates and
    returns various information about them. If using the cli, make
    sure to update the bikes database with the -u command.

    Locations can be either a specific postcode, or a pair of coordinates.
    Coordinates are passed in the form "55.948824,-3.196425".

    :param locations: The list of postcodes or coordinates to search.
    :param random: The number of random postcodes to include.
    :param bikes: Includes a list of stolen bikes in that area.
    :param crime: Includes a list of committed crimes in that area.
    :param nearby: Includes a list of wikipedia articles in that area.
    :param json: Returns the data in json format.
    :param update_bikes: Whether to force update bikes.
    :param api_server: If given, the program will instead run a rest api.
    :param cross_origin:
    :param host:
    :param port: Defines the port to run the rest api on.
    :param db_path: The path to the sqlite db to use.
    :param verbose: The verbosity.
    """
    log_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    logging.basicConfig(level=log_levels[min(verbose, 2)])
    initialize_database(db_path)
    loop = get_event_loop()
    if update_bikes:
        logger.info('Force updating bikes.')
        loop.run_until_complete(util.update_bikes())
    if api_server:
        if cross_origin:
            enable_cross_origin(app)
        try:
            web.run_app(app, host=host, port=port)
        except CancelledError as e:
            if e.__context__ is not None:
                click.echo(Fore.RED + (f'Could not bind to address {host}:{port}' if e.__context__.errno == 48 else e.__context__))
                exit(1)
            else:
                click.echo('Goodbye!')
    elif len(locations) > 0 or random > 0:
        exit(loop.run_until_complete(cli(locations, random, bikes=bikes, crime=crime, nearby=nearby, as_json=json)))
    else:
        click.echo(Fore.RED + 'Either include a post code, or the --api-server flag.')