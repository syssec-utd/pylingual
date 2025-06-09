async def cli(location_strings: Tuple[str], random_postcodes_count: int, *, bikes: bool=False, crime: bool=False, nearby: bool=False, as_json: bool=False):
    """
    Runs the CLI app.
    Tries to execute as many steps as possible to give the user
    the best understanding of the errors (if there are any).

    :param location_strings: A list of desired postcodes or coordinates.
    :param random_postcodes_count: A number of random postcodes to fetch..
    :param bikes: A flag to include bikes.
    :param crime: A flag to include crime.
    :param nearby: A flag to include nearby.
    :param as_json: A flag to make json output.
    """

    def match_getter(location) -> Optional[PostcodeGetter]:
        for getter in getters:
            if getter.can_provide(location):
                return getter(location)
        else:
            return None

    async def handle_getter(exception_list, getter):
        try:
            return await getter.get_postcodes()
        except (CachingError, ApiError):
            exception_list.append(f'Could not get data for {getter}')

    async def handle_datas(exception_list, postcode):
        (postcode_data, new_exceptions) = await get_postcode_data(postcode, bikes, crime, nearby)
        exception_list += new_exceptions
        return postcode_data
    exception_list: List[Exception] = []
    handle_getter = partial(handle_getter, exception_list)
    handle_datas = partial(handle_datas, exception_list)
    postcode_getters = {location: match_getter(location) for location in set(location_strings) | ({random_postcodes_count} if random_postcodes_count > 0 else set())}
    (matched, unmatched) = partition(lambda k_v: k_v[1] is not None, postcode_getters.items())
    for (location, getter) in unmatched:
        echo(f'Invalid input for {location}')
    postcodes_collection = [await handle_getter(getter) for (location, getter) in matched]
    if len(exception_list) > 0:
        for f in exception_list:
            echo(str(f))
        return 1
    postcode_datas = [await handle_datas(postcode) for entry in postcodes_collection for postcode in entry]
    serializer = (PostcodeSerializerJSON if as_json else PostcodeSerializerHuman)(postcode_datas)
    echo(serializer.serialize())