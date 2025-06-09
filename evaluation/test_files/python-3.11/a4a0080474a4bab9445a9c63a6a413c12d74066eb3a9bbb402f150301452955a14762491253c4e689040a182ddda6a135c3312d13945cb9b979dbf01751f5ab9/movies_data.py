""" A small subset of data from the `Open Movie Database`_.

License: `CC BY-NC 4.0`_

Sourced from http://www.omdbapi.com

This modules has an attribute ``movie_path``. This attribute contains the path
to a SQLite database with the data.

.. bokeh-sampledata-xref:: movies_data

.. _Open Movie Database: http://www.omdbapi.com
"""
from __future__ import annotations
import logging
log = logging.getLogger(__name__)
from ..util.sampledata import external_path
__all__ = ('movie_path',)
movie_path = external_path('movies.db')