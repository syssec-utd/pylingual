import logging
import requests
log = logging.getLogger(__name__)

def getip(url):
    """Get IP

    @param int level: logging level
    @return: IP address
    @rtype: str
    """
    log.info('getting my IP')
    res = requests.get(url)
    return res.json()['ip']