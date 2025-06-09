def search(self, **kwargs):
    """
        :param entity_id: location id
        :param entity_type: location type (city, subzone, zone, lanmark, metro , group)
        :param q: search keyword
        :param start: fetch results after offset
        :param count: max number of results to display
        :param lat: latitude
        :param lon: longitude
        :param radius: radius around (lat,lon); to define search area, defined in meters(M)
        :param cuisines: list of cuisine id's separated by comma
        :param establishment_type: estblishment id obtained from establishments call
        :param collection_id: collection id obtained from collections call
        :param category: category ids obtained from categories call
        :param sort: sort restaurants by (cost, rating, real_distance)
        :param order: used with 'sort' parameter to define ascending / descending
        :return: json response
        The location input can be specified using Zomato location ID or coordinates. Cuisine / Establishment /
        Collection IDs can be obtained from respective api calls.

        Partner Access is required to access photos and reviews.

        Examples:
        - To search for 'Italian' restaurants in 'Manhattan, New York City',
        set cuisines = 55, entity_id = 94741 and entity_type = zone
        - To search for 'cafes' in 'Manhattan, New York City',
        set establishment_type = 1, entity_type = zone and entity_id = 94741
        - Get list of all restaurants in 'Trending this Week' collection in 'New York City' by using
        entity_id = 280, entity_type = city and collection_id = 1
        """
    params = {}
    available_params = ['entity_id', 'entity_type', 'q', 'start', 'count', 'lat', 'lon', 'radius', 'cuisines', 'establishment_type', 'collection_id', 'category', 'sort', 'order']
    for key in available_params:
        if key in kwargs:
            params[key] = kwargs[key]
    results = self.api.get('/search', params)
    return results