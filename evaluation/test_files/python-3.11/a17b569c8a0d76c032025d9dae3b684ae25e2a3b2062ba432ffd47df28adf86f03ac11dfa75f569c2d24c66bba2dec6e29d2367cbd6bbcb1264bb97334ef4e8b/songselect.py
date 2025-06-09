"""
The :mod:`~openlp.plugins.songs.lib.songselect` module contains the SongSelect importer itself.
"""
import logging
import re
from html import unescape
from urllib.request import URLError
from PyQt5 import QtCore
from bs4 import BeautifulSoup, NavigableString
from openlp.plugins.songs.lib import VerseType, clean_song
from openlp.plugins.songs.lib.db import Song, Author, Topic
from openlp.plugins.songs.lib.openlyricsxml import SongXML
from openlp.core.common.utils import wait_for
BASE_URL = 'https://songselect.ccli.com'
LOGIN_PAGE = 'https://profile.ccli.com/account/signin?appContext=SongSelect&returnUrl=https%3a%2f%2fsongselect.ccli.com%2f'
LOGIN_URL = 'https://profile.ccli.com'
LOGOUT_URL = BASE_URL + '/account/logout'
SEARCH_URL = BASE_URL + '/search/results'
SONG_PAGE = BASE_URL + '/Songs/'
log = logging.getLogger(__name__)

class Pages(object):
    """
    Songselect web page types.
    """
    Login = 0
    Home = 1
    Search = 2
    Song = 3
    Other = 4

class SongSelectImport(object):
    """
    The :class:`~openlp.plugins.songs.lib.songselect.SongSelectImport` class contains all the code which interfaces
    with CCLI's SongSelect service and downloads the songs.
    """

    def __init__(self, db_manager, webview):
        """
        Set up the song select importer

        :param db_manager: The song database manager
        """
        self.db_manager = db_manager
        self.webview = webview

    def get_page_type(self):
        """
        Get the type of page the user is currently ono

        :return: The page the user is on
        """
        current_url_host = self.webview.page().url().host()
        current_url_path = self.webview.page().url().path()
        if current_url_host == QtCore.QUrl(LOGIN_URL).host() and current_url_path == QtCore.QUrl(LOGIN_PAGE).path():
            return Pages.Login
        elif current_url_host == QtCore.QUrl(BASE_URL).host():
            if current_url_path == '/' or current_url_path == '':
                return Pages.Home
            elif current_url_path == QtCore.QUrl(SEARCH_URL).path():
                return Pages.Search
            elif self.get_song_number_from_url(current_url_path) is not None:
                return Pages.Song
        return Pages.Other

    def _run_javascript(self, script):
        """
        Run a script and returns the result

        :param script: The javascript to be run
        :return: The evaluated result
        """
        self.web_stuff = ''
        self.got_web_stuff = False

        def handle_result(result):
            """
            Handle the result from the asynchronous call
            """
            self.got_web_stuff = True
            self.web_stuff = result
        self.webview.page().runJavaScript(script, handle_result)
        wait_for(lambda: self.got_web_stuff)
        return self.web_stuff

    def reset_webview(self):
        """
        Sets the webview back to the login page using the Qt setUrl method
        """
        url = QtCore.QUrl(LOGIN_PAGE)
        self.webview.setUrl(url)

    def set_home_page(self):
        """
        Sets the webview to the search page
        """
        self.set_page(BASE_URL)

    def set_page(self, url):
        """
        Sets the active page in the webview

        :param url: The new page location
        """
        script = 'document.location = "{}"'.format(url)
        self._run_javascript(script)

    def set_login_fields(self, username, password):
        script_set_login_fields = 'document.getElementById("EmailAddress").value = "{email}";document.getElementById("Password").value = "{password}";'.format(email=username, password=password)
        self._run_javascript(script_set_login_fields)

    def get_page(self, url):
        """
        Gets the html for the url through the active webview

        :return: String containing a html document
        """
        script_get_page = 'var openlp_page_data = null;fetch("{}").then(data => {{return data.text()}})           .then(data => {{openlp_page_data = data}})'.format(url)
        self._run_javascript(script_get_page)
        wait_for(lambda: self._run_javascript('openlp_page_data != null'))
        return self._run_javascript('openlp_page_data')

    def get_song_number_from_url(self, url):
        """
        Gets the ccli song number for a song from the url

        :return: String containg ccli song number, None is returned if not found
        """
        ccli_number_regex = re.compile('.*?Songs\\/([0-9]+).*', re.IGNORECASE)
        regex_matches = ccli_number_regex.match(url)
        if regex_matches:
            return regex_matches.group(1)
        return None

    def get_song(self, callback=None):
        """
        Get the full song from SongSelect

        :param song: The song page url
        :param callback: A callback which can be used to indicate progress
        :return: Dictionary containing the song info
        """
        song = {}
        current_url = self.webview.url().path()
        ccli_number = self.get_song_number_from_url(current_url)
        if callback:
            callback()
        try:
            song_page = BeautifulSoup(self.get_page(SONG_PAGE + ccli_number), 'lxml')
        except (TypeError, URLError) as error:
            log.exception('Could not get song from SongSelect, {error}'.format(error=error))
            return None
        try:
            lyrics_link = song_page.find('section', 'page-section').find('a')['href']
        except KeyError:
            return None
        if callback:
            callback()
        try:
            lyrics_page = BeautifulSoup(self.get_page(BASE_URL + lyrics_link), 'lxml')
        except (TypeError, URLError):
            log.exception('Could not get lyrics from SongSelect')
            return None
        if callback:
            callback()
        theme_elements = []
        themes_regex = re.compile('\\bThemes\\b')
        for ul in song_page.find_all('ul', 'song-meta-list'):
            if ul.find('li', string=themes_regex):
                theme_elements.extend(ul.find_all('li')[1:])
        copyright_elements = lyrics_page.find('ul', 'copyright').find_all('li')
        author_elements = song_page.find('div', 'content-title').find('ul', 'authors').find_all('li')
        song['title'] = unescape(song_page.find('div', 'content-title').find('h1').string.strip())
        song['authors'] = [unescape(li.find('a').string).strip() for li in author_elements]
        song['copyright'] = '/'.join([unescape(li.string).strip() for li in copyright_elements])
        song['topics'] = [unescape(li.string).strip() for li in theme_elements]
        song['ccli_number'] = song_page.find('div', 'song-content-data').find('ul').find('li').find('strong').string.strip()
        song['verses'] = []
        verses = lyrics_page.find('div', 'song-viewer lyrics').find_all('p')
        verse_labels = lyrics_page.find('div', 'song-viewer lyrics').find_all('h3')
        for verse, label in zip(verses, verse_labels):
            song_verse = {'label': unescape(label.string).strip(), 'lyrics': ''}
            for v in verse.contents:
                if isinstance(v, NavigableString):
                    song_verse['lyrics'] += unescape(v.string).strip()
                else:
                    song_verse['lyrics'] += '\n'
            song_verse['lyrics'] = song_verse['lyrics'].strip(' \n\r\t')
            song['verses'].append(song_verse)
        for counter, author in enumerate(song['authors']):
            song['authors'][counter] = unescape(author)
        return song

    def save_song(self, song):
        """
        Save a song to the database, using the db_manager

        :param song: Dictionary of the song to save
        :return:
        """
        db_song = Song.populate(title=song['title'], copyright=song['copyright'], ccli_number=song['ccli_number'])
        song_xml = SongXML()
        verse_order = []
        for verse in song['verses']:
            if ' ' in verse['label']:
                verse_type, verse_number = verse['label'].split(' ', 1)
            else:
                verse_type = verse['label']
                verse_number = 1
            verse_type = VerseType.from_loose_input(verse_type)
            try:
                verse_number = int(verse_number)
            except ValueError:
                verse_number = 1
            song_xml.add_verse_to_lyrics(VerseType.tags[verse_type], verse_number, verse['lyrics'])
            verse_order.append('{tag}{number}'.format(tag=VerseType.tags[verse_type], number=verse_number))
        db_song.verse_order = ' '.join(verse_order)
        db_song.lyrics = song_xml.extract_xml()
        clean_song(self.db_manager, db_song)
        self.db_manager.save_object(db_song)
        db_song.authors_songs = []
        for author_name in song['authors']:
            author = self.db_manager.get_object_filtered(Author, Author.display_name == author_name)
            if not author:
                name_parts = author_name.rsplit(' ', 1)
                first_name = name_parts[0]
                if len(name_parts) == 1:
                    last_name = ''
                else:
                    last_name = name_parts[1]
                author = Author.populate(first_name=first_name, last_name=last_name, display_name=author_name)
            db_song.add_author(author)
        for topic_name in song.get('topics', []):
            topic = self.db_manager.get_object_filtered(Topic, Topic.name == topic_name)
            if not topic:
                topic = Topic.populate(name=topic_name)
            db_song.topics.append(topic)
        self.db_manager.save_object(db_song)
        return db_song