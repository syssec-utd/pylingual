async def parse_tag_results(soup):
    """
    Parse a page of tag or trait results. Same format.

    :param soup: BS4 Class Object
    :return: A list of tags, Nothing else really useful there
    """
    soup = soup.find_all('td', class_='tc3')
    tags = []
    for item in soup:
        tags.append(item.a.string)
    return tags