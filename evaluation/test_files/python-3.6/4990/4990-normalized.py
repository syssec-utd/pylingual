def __fetch(self, url, payload):
    """Fetch requests from groupsio API"""
    r = requests.get(url, params=payload, auth=self.auth, verify=self.verify)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise e
    return r