def details(self, query, accept_language=None, content_type=None, user_agent=None, client_id=None, client_ip=None, location=None, crop_bottom=None, crop_left=None, crop_right=None, crop_top=None, crop_type=None, country_code=None, id=None, image_url=None, insights_token=None, modules=None, market=None, safe_search=None, set_lang=None, custom_headers=None, raw=False, **operation_config):
    """The Image Detail Search API lets you search on Bing and get back
        insights about an image, such as webpages that include the image. This
        section provides technical details about the query parameters and
        headers that you use to request insights of images and the JSON
        response objects that contain them. For examples that show how to make
        requests, see [Searching the Web for
        Images](https://docs.microsoft.com/azure/cognitive-services/bing-image-search/search-the-web).

        :param query: The user's search query term. The term cannot be empty.
         The term may contain [Bing Advanced
         Operators](http://msdn.microsoft.com/library/ff795620.aspx). For
         example, to limit images to a specific domain, use the
         [site:](http://msdn.microsoft.com/library/ff795613.aspx) operator. To
         help improve relevance of an insights query (see
         [insightsToken](https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-images-api-v7-reference#insightstoken)),
         you should always include the user's query term. Use this parameter
         only with the Image Search API.Do not specify this parameter when
         calling the Trending Images API.
        :type query: str
        :param accept_language: A comma-delimited list of one or more
         languages to use for user interface strings. The list is in decreasing
         order of preference. For additional information, including expected
         format, see
         [RFC2616](http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html).
         This header and the
         [setLang](https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-images-api-v7-reference#setlang)
         query parameter are mutually exclusive; do not specify both. If you
         set this header, you must also specify the
         [cc](https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-images-api-v7-reference#cc)
         query parameter. To determine the market to return results for, Bing
         uses the first supported language it finds from the list and combines
         it with the cc parameter value. If the list does not include a
         supported language, Bing finds the closest language and market that
         supports the request or it uses an aggregated or default market for
         the results. To determine the market that Bing used, see the
         BingAPIs-Market header. Use this header and the cc query parameter
         only if you specify multiple languages. Otherwise, use the
         [mkt](https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-images-api-v7-reference#mkt)
         and
         [setLang](https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-images-api-v7-reference#setlang)
         query parameters. A user interface string is a string that's used as a
         label in a user interface. There are few user interface strings in the
         JSON response objects. Any links to Bing.com properties in the
         response objects apply the specified language.
        :type accept_language: str
        :param content_type: Optional request header. If you set the
         [modules](https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-images-api-v7-reference#modulesrequested)
         query parameter to RecognizedEntities, you may specify the binary of
         an image in the body of a POST request. If you specify the image in
         the body of a POST request, you must specify this header and set its
         value to multipart/form-data. The maximum image size is 1 MB.
        :type content_type: str
        :param user_agent: The user agent originating the request. Bing uses
         the user agent to provide mobile users with an optimized experience.
         Although optional, you are encouraged to always specify this header.
         The user-agent should be the same string that any commonly used
         browser sends. For information about user agents, see [RFC
         2616](http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). The
         following are examples of user-agent strings. Windows Phone:
         Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0;
         IEMobile/10.0; ARM; Touch; NOKIA; Lumia 822). Android: Mozilla / 5.0
         (Linux; U; Android 2.3.5; en - us; SCH - I500 Build / GINGERBREAD)
         AppleWebKit / 533.1 (KHTML; like Gecko) Version / 4.0 Mobile Safari /
         533.1. iPhone: Mozilla / 5.0 (iPhone; CPU iPhone OS 6_1 like Mac OS X)
         AppleWebKit / 536.26 (KHTML; like Gecko) Mobile / 10B142 iPhone4; 1
         BingWeb / 3.03.1428.20120423. PC: Mozilla / 5.0 (Windows NT 6.3;
         WOW64; Trident / 7.0; Touch; rv:11.0) like Gecko. iPad: Mozilla / 5.0
         (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit / 537.51.1 (KHTML, like
         Gecko) Version / 7.0 Mobile / 11A465 Safari / 9537.53
        :type user_agent: str
        :param client_id: Bing uses this header to provide users with
         consistent behavior across Bing API calls. Bing often flights new
         features and improvements, and it uses the client ID as a key for
         assigning traffic on different flights. If you do not use the same
         client ID for a user across multiple requests, then Bing may assign
         the user to multiple conflicting flights. Being assigned to multiple
         conflicting flights can lead to an inconsistent user experience. For
         example, if the second request has a different flight assignment than
         the first, the experience may be unexpected. Also, Bing can use the
         client ID to tailor web results to that client ID’s search history,
         providing a richer experience for the user. Bing also uses this header
         to help improve result rankings by analyzing the activity generated by
         a client ID. The relevance improvements help with better quality of
         results delivered by Bing APIs and in turn enables higher
         click-through rates for the API consumer. IMPORTANT: Although
         optional, you should consider this header required. Persisting the
         client ID across multiple requests for the same end user and device
         combination enables 1) the API consumer to receive a consistent user
         experience, and 2) higher click-through rates via better quality of
         results from the Bing APIs. Each user that uses your application on
         the device must have a unique, Bing generated client ID. If you do not
         include this header in the request, Bing generates an ID and returns
         it in the X-MSEdge-ClientID response header. The only time that you
         should NOT include this header in a request is the first time the user
         uses your app on that device. Use the client ID for each Bing API
         request that your app makes for this user on the device. Persist the
         client ID. To persist the ID in a browser app, use a persistent HTTP
         cookie to ensure the ID is used across all sessions. Do not use a
         session cookie. For other apps such as mobile apps, use the device's
         persistent storage to persist the ID. The next time the user uses your
         app on that device, get the client ID that you persisted. Bing
         responses may or may not include this header. If the response includes
         this header, capture the client ID and use it for all subsequent Bing
         requests for the user on that device. If you include the
         X-MSEdge-ClientID, you must not include cookies in the request.
        :type client_id: str
        :param client_ip: The IPv4 or IPv6 address of the client device. The
         IP address is used to discover the user's location. Bing uses the
         location information to determine safe search behavior. Although
         optional, you are encouraged to always specify this header and the
         X-Search-Location header. Do not obfuscate the address (for example,
         by changing the last octet to 0). Obfuscating the address results in
         the location not being anywhere near the device's actual location,
         which may result in Bing serving erroneous results.
        :type client_ip: str
        :param location: A semicolon-delimited list of key/value pairs that
         describe the client's geographical location. Bing uses the location
         information to determine safe search behavior and to return relevant
         local content. Specify the key/value pair as <key>:<value>. The
         following are the keys that you use to specify the user's location.
         lat (required): The latitude of the client's location, in degrees. The
         latitude must be greater than or equal to -90.0 and less than or equal
         to +90.0. Negative values indicate southern latitudes and positive
         values indicate northern latitudes. long (required): The longitude of
         the client's location, in degrees. The longitude must be greater than
         or equal to -180.0 and less than or equal to +180.0. Negative values
         indicate western longitudes and positive values indicate eastern
         longitudes. re (required): The radius, in meters, which specifies the
         horizontal accuracy of the coordinates. Pass the value returned by the
         device's location service. Typical values might be 22m for GPS/Wi-Fi,
         380m for cell tower triangulation, and 18,000m for reverse IP lookup.
         ts (optional): The UTC UNIX timestamp of when the client was at the
         location. (The UNIX timestamp is the number of seconds since January
         1, 1970.) head (optional): The client's relative heading or direction
         of travel. Specify the direction of travel as degrees from 0 through
         360, counting clockwise relative to true north. Specify this key only
         if the sp key is nonzero. sp (optional): The horizontal velocity
         (speed), in meters per second, that the client device is traveling.
         alt (optional): The altitude of the client device, in meters. are
         (optional): The radius, in meters, that specifies the vertical
         accuracy of the coordinates. Specify this key only if you specify the
         alt key. Although many of the keys are optional, the more information
         that you provide, the more accurate the location results are. Although
         optional, you are encouraged to always specify the user's geographical
         location. Providing the location is especially important if the
         client's IP address does not accurately reflect the user's physical
         location (for example, if the client uses VPN). For optimal results,
         you should include this header and the X-MSEdge-ClientIP header, but
         at a minimum, you should include this header.
        :type location: str
        :param crop_bottom: The bottom coordinate of the region to crop. The
         coordinate is a fractional value of the original image's height and is
         measured from the top, left corner of the image. Specify the
         coordinate as a value from 0.0 through 1.0. Use this parameter only
         with the Insights API. Do not specify this parameter when calling the
         Images, Trending Images, or Web Search APIs.
        :type crop_bottom: float
        :param crop_left: The left coordinate of the region to crop. The
         coordinate is a fractional value of the original image's height and is
         measured from the top, left corner of the image. Specify the
         coordinate as a value from 0.0 through 1.0. Use this parameter only
         with the Insights API. Do not specify this parameter when calling the
         Images, Trending Images, or Web Search APIs.
        :type crop_left: float
        :param crop_right: The right coordinate of the region to crop. The
         coordinate is a fractional value of the original image's height and is
         measured from the top, left corner of the image. Specify the
         coordinate as a value from 0.0 through 1.0. Use this parameter only
         with the Insights API. Do not specify this parameter when calling the
         Images, Trending Images, or Web Search APIs.
        :type crop_right: float
        :param crop_top: The top coordinate of the region to crop. The
         coordinate is a fractional value of the original image's height and is
         measured from the top, left corner of the image. Specify the
         coordinate as a value from 0.0 through 1.0. Use this parameter only
         with the Insights API. Do not specify this parameter when calling the
         Images, Trending Images, or Web Search APIs.
        :type crop_top: float
        :param crop_type: The crop type to use when cropping the image based
         on the coordinates specified in the cal, cat, car, and cab parameters.
         The following are the possible values. 0: Rectangular (default). Use
         this parameter only with the Insights API. Do not specify this
         parameter when calling the Images, Trending Images, or Web Search
         APIs. Possible values include: 'Rectangular'
        :type crop_type: str or
         ~azure.cognitiveservices.search.imagesearch.models.ImageCropType
        :param country_code: A 2-character country code of the country where
         the results come from. For a list of possible values, see [Market
         Codes](https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-images-api-v7-reference#market-codes).
         If you set this parameter, you must also specify the
         [Accept-Language](https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-images-api-v7-reference#acceptlanguage)
         header. Bing uses the first supported language it finds from the
         languages list, and combine that language with the country code that
         you specify to determine the market to return results for. If the
         languages list does not include a supported language, Bing finds the
         closest language and market that supports the request, or it may use
         an aggregated or default market for the results instead of a specified
         one. You should use this query parameter and the Accept-Language query
         parameter only if you specify multiple languages; otherwise, you
         should use the mkt and setLang query parameters. This parameter and
         the
         [mkt](https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-images-api-v7-reference#mkt)
         query parameter are mutually exclusive—do not specify both.
        :type country_code: str
        :param id: An ID that uniquely identifies an image. Use this parameter
         to ensure that the specified image is the first image in the list of
         images that Bing returns. The
         [Image](https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-images-api-v7-reference#image)
         object's imageId field contains the ID that you set this parameter to.
        :type id: str
        :param image_url: The URL of an image that you want to get insights
         of. Use this parameter as an alternative to using the insightsToken
         parameter to specify the image. You may also specify the image by
         placing the binary of the image in the body of a POST request. If you
         use the binary option, see the
         [Content-Type](https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-images-api-v7-reference#contenttype)
         header. The maximum supported image size is 1 MB. Use this parameter
         only with the Insights API. Do not specify this parameter when calling
         the Images, Trending Images, or Web Search APIs.
        :type image_url: str
        :param insights_token: An image token. The
         [Image](https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-images-api-v7-reference#image)
         object's
         [imageInsightsToken](https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-images-api-v7-reference#image-imageinsightstoken)
         contains the token. Specify this parameter to get additional
         information about an image, such as a caption or shopping source. For
         a list of the additional information about an image that you can get,
         see the
         [modules](https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-images-api-v7-reference#modulesrequested)
         query parameter. Use this parameter only with the Insights API. Do not
         specify this parameter when calling the Images, Trending Images, or
         Web Search APIs.
        :type insights_token: str
        :param modules: A comma-delimited list of insights to request. The
         following are the possible case-insensitive values. All: Return all
         insights, if available, except RecognizedEntities. BRQ: Best
         representative query. The query term that best describes the image.
         Caption: A caption that provides information about the image. If the
         caption contains entities, the response may include links to images of
         those entities. Collections: A list of related images. Recipes: A list
         of recipes for cooking the food shown in the images. PagesIncluding: A
         list of webpages that include the image. RecognizedEntities: A list of
         entities (people) that were recognized in the image. NOTE: You may not
         specify this module with any other module. If you specify it with
         other modules, the response doesn't include recognized entities.
         RelatedSearches: A list of related searches made by others.
         ShoppingSources: A list of merchants where you can buy related
         offerings. SimilarImages: A list of images that are visually similar
         to the original image. SimilarProducts: A list of images that contain
         a product that is similar to a product found in the original image.
         Tags: Provides characteristics of the type of content found in the
         image. For example, if the image is of a person, the tags might
         indicate the person's gender and type of clothes they're wearing. If
         you specify a module and there is no data for the module, the response
         object doesn't include the related field. For example, if you specify
         Caption and it does not exist, the response doesn't include the
         imageCaption field. To include related searches, the request must
         include the original query string. Although the original query string
         is not required for similar images or products, you should always
         include it because it can help improve relevance and the results. Use
         this parameter only with the Insights API. Do not specify this
         parameter when calling the Images, Trending Images, or Web Search
         APIs.
        :type modules: list[str or
         ~azure.cognitiveservices.search.imagesearch.models.ImageInsightModule]
        :param market: The market where the results come from. Typically, mkt
         is the country where the user is making the request from. However, it
         could be a different country if the user is not located in a country
         where Bing delivers results. The market must be in the form <language
         code>-<country code>. For example, en-US. The string is case
         insensitive. For a list of possible market values, see [Market
         Codes](https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-images-api-v7-reference#market-codes).
         NOTE: If known, you are encouraged to always specify the market.
         Specifying the market helps Bing route the request and return an
         appropriate and optimal response. If you specify a market that is not
         listed in [Market
         Codes](https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-images-api-v7-reference#market-codes),
         Bing uses a best fit market code based on an internal mapping that is
         subject to change. This parameter and the
         [cc](https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-images-api-v7-reference#cc)
         query parameter are mutually exclusive—do not specify both.
        :type market: str
        :param safe_search: Filter images for adult content. The following are
         the possible filter values. Off: May return images with adult content.
         If the request is through the Image Search API, the response includes
         thumbnail images that are clear (non-fuzzy). However, if the request
         is through the Web Search API, the response includes thumbnail images
         that are pixelated (fuzzy). Moderate: If the request is through the
         Image Search API, the response doesn't include images with adult
         content. If the request is through the Web Search API, the response
         may include images with adult content (the thumbnail images are
         pixelated (fuzzy)). Strict: Do not return images with adult content.
         The default is Moderate. If the request comes from a market that
         Bing's adult policy requires that safeSearch is set to Strict, Bing
         ignores the safeSearch value and uses Strict. If you use the site:
         query operator, there is the chance that the response may contain
         adult content regardless of what the safeSearch query parameter is set
         to. Use site: only if you are aware of the content on the site and
         your scenario supports the possibility of adult content. Possible
         values include: 'Off', 'Moderate', 'Strict'
        :type safe_search: str or
         ~azure.cognitiveservices.search.imagesearch.models.SafeSearch
        :param set_lang: The language to use for user interface strings.
         Specify the language using the ISO 639-1 2-letter language code. For
         example, the language code for English is EN. The default is EN
         (English). Although optional, you should always specify the language.
         Typically, you set setLang to the same language specified by mkt
         unless the user wants the user interface strings displayed in a
         different language. This parameter and the
         [Accept-Language](https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-images-api-v7-reference#acceptlanguage)
         header are mutually exclusive; do not specify both. A user interface
         string is a string that's used as a label in a user interface. There
         are few user interface strings in the JSON response objects. Also, any
         links to Bing.com properties in the response objects apply the
         specified language.
        :type set_lang: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: ImageInsights or ClientRawResponse if raw=true
        :rtype:
         ~azure.cognitiveservices.search.imagesearch.models.ImageInsights or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<azure.cognitiveservices.search.imagesearch.models.ErrorResponseException>`
        """
    url = self.details.metadata['url']
    query_parameters = {}
    if crop_bottom is not None:
        query_parameters['cab'] = self._serialize.query('crop_bottom', crop_bottom, 'float')
    if crop_left is not None:
        query_parameters['cal'] = self._serialize.query('crop_left', crop_left, 'float')
    if crop_right is not None:
        query_parameters['car'] = self._serialize.query('crop_right', crop_right, 'float')
    if crop_top is not None:
        query_parameters['cat'] = self._serialize.query('crop_top', crop_top, 'float')
    if crop_type is not None:
        query_parameters['ct'] = self._serialize.query('crop_type', crop_type, 'str')
    if country_code is not None:
        query_parameters['cc'] = self._serialize.query('country_code', country_code, 'str')
    if id is not None:
        query_parameters['id'] = self._serialize.query('id', id, 'str')
    if image_url is not None:
        query_parameters['imgUrl'] = self._serialize.query('image_url', image_url, 'str')
    if insights_token is not None:
        query_parameters['insightsToken'] = self._serialize.query('insights_token', insights_token, 'str')
    if modules is not None:
        query_parameters['modules'] = self._serialize.query('modules', modules, '[str]', div=',')
    if market is not None:
        query_parameters['mkt'] = self._serialize.query('market', market, 'str')
    query_parameters['q'] = self._serialize.query('query', query, 'str')
    if safe_search is not None:
        query_parameters['safeSearch'] = self._serialize.query('safe_search', safe_search, 'str')
    if set_lang is not None:
        query_parameters['setLang'] = self._serialize.query('set_lang', set_lang, 'str')
    header_parameters = {}
    header_parameters['Content-Type'] = 'application/json; charset=utf-8'
    if custom_headers:
        header_parameters.update(custom_headers)
    header_parameters['X-BingApis-SDK'] = self._serialize.header('self.x_bing_apis_sdk', self.x_bing_apis_sdk, 'str')
    if accept_language is not None:
        header_parameters['Accept-Language'] = self._serialize.header('accept_language', accept_language, 'str')
    if content_type is not None:
        header_parameters['Content-Type'] = self._serialize.header('content_type', content_type, 'str')
    if user_agent is not None:
        header_parameters['User-Agent'] = self._serialize.header('user_agent', user_agent, 'str')
    if client_id is not None:
        header_parameters['X-MSEdge-ClientID'] = self._serialize.header('client_id', client_id, 'str')
    if client_ip is not None:
        header_parameters['X-MSEdge-ClientIP'] = self._serialize.header('client_ip', client_ip, 'str')
    if location is not None:
        header_parameters['X-Search-Location'] = self._serialize.header('location', location, 'str')
    request = self._client.get(url, query_parameters)
    response = self._client.send(request, header_parameters, stream=False, **operation_config)
    if response.status_code not in [200]:
        raise models.ErrorResponseException(self._deserialize, response)
    deserialized = None
    if response.status_code == 200:
        deserialized = self._deserialize('ImageInsights', response)
    if raw:
        client_raw_response = ClientRawResponse(deserialized, response)
        return client_raw_response
    return deserialized