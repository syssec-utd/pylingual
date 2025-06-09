import json
import os
import re
import warnings
from typing import Any, List, Optional, Union
import ee
from ee_extra.Apps.utils import _get_apps

def apps(online: bool=False) -> dict:
    """Gets the dictionary of available Google Earth Engine Apps.

    Args:
        online : Whether to retrieve the most recent list of apps directly from the GitHub repository and not from the local copy.

    Returns:
        Dictionary of available apps.

    Examples:
        >>> import ee
        >>> from ee_extra.Apps.core import apps
        >>> ee.Initialize()
        >>> Apps = apps()
        >>> Apps["jstnbraaten"][0]
        "https://jstnbraaten.users.earthengine.app/view/conus-cover-vis"
    """
    return _get_apps(online)