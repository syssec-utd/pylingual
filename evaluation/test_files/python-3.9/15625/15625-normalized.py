async def parse_user_results(soup):
    """
    Parse a page of user results

    :param soup: Bs4 Class object
    :return: A list of dictionaries containing a name and join date
    """
    soup = list(soup.find_all('table', class_='stripe')[0].children)[1:]
    users = []
    for item in soup:
        t_u = {'name': None, 'joined': None}
        t_u['name'] = list(item.children)[0].a.string
        t_u['joined'] = list(item.children)[1].string
        users.append(t_u)
        del t_u
    return users