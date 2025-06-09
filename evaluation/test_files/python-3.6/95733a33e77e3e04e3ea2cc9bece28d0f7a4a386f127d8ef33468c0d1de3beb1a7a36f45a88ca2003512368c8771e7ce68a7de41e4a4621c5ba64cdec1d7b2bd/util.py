from bq.util.mkdir import _mkdir
import posixpath
import urllib
import os

def fetch_file(filename, url, dir):
    """
        @param filename: name of the file fetching from the store
        @param url: url of the store
        @param dir: the directory the file will be placed in
        
        @return the local path to the file
    """
    _mkdir(url)
    _mkdir(dir)
    url = posixpath.join(url, filename)
    path = os.path.join(dir, filename)
    if not os.path.exists(path):
        urllib.urlretrieve(url, path)
    return path