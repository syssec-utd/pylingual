async def parse_search(self, stype, soup):
    """
        This is our parsing dispatcher

        :param stype: Search type category
        :param soup: The beautifulsoup object that contains the parsed html
        """
    if stype == 'v':
        return await parse_vn_results(soup)
    elif stype == 'r':
        return await parse_release_results(soup)
    elif stype == 'p':
        return await parse_prod_staff_results(soup)
    elif stype == 's':
        return await parse_prod_staff_results(soup)
    elif stype == 'c':
        return await parse_character_results(soup)
    elif stype == 'g':
        return await parse_tag_results(soup)
    elif stype == 'i':
        return await parse_tag_results(soup)
    elif stype == 'u':
        return await parse_user_results(soup)