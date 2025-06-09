import re
import logging
from urllib.parse import urljoin
from ..crawlerbase import CrawlerBase
logger = logging.getLogger(__name__)

class WnacgCrawler(CrawlerBase):
    SITE = 'wnacg'
    SITE_INDEX = 'http://www.wnacg.org/'
    SOURCE_NAME = '绅士漫画'
    LOGIN_URL = SITE_INDEX
    DEFAULT_COMICID = '123107'
    DEFAULT_SEARCH_NAME = '漢化'
    DEFAULT_TAG = '3'
    R18 = True
    COMICID_PATTERN = re.compile('/photos-index-aid-(\\d+)')
    SINGLE_CHAPTER = True

    @property
    def source_url(self):
        return self.get_source_url(self.comicid)

    def get_source_url(self, comicid):
        return urljoin(self.SITE_INDEX, '/photos-index-aid-{}.html'.format(comicid))

    def get_comicbook_item(self):
        soup = self.get_soup(self.source_url)
        name = soup.h2.text.strip()
        author = ''
        desc = soup.find('div', {'class': 'asTBcell uwconn'}).p.text
        img = soup.find('div', {'class': 'asTBcell uwthumb'}).img
        src = img.get('data-original') or img.get('src')
        cover_image_url = 'https:' + src if src else ''
        book = self.new_comicbook_item(name=name, desc=desc, cover_image_url=cover_image_url, author=author, source_url=self.source_url)
        chapter_number = 1
        url = urljoin(self.SITE_INDEX, '/photos-slide-aid-{}.html'.format(self.comicid))
        book.add_chapter(chapter_number=chapter_number, cid=self.comicid, source_url=url, title='')
        tag_list = [i.text for i in soup.find('div', {'class': 'addtags'}).find_all('a', {'class': 'tagshow'})]
        for tag_name in tag_list:
            tag_id = self.get_tag_id_by_name(tag_name)
            book.add_tag(name=tag_name, tag=tag_id)
        return book

    def get_chapter_image_urls(self, citem):
        api_url = urljoin(self.SITE_INDEX, '/photos-gallery-aid-{}.html'.format(citem.cid))
        html = self.get_html(api_url)
        img_list = re.findall('url: fast_img_host\\+\\\\"(.*?)\\\\".*?}', html)
        image_urls = []
        for url in img_list:
            if url.startswith('//'):
                image_urls.append('http:' + url)
            elif url.startswith('/'):
                urljoin(self.SITE_INDEX, url)
            else:
                image_urls.append(url)
        return image_urls

    def search(self, name, page=1, size=None):
        url = urljoin(self.SITE_INDEX, '/search/index.php?q={}&m=&f=_all&s=create_time_DESC&p={}'.format(name, page))
        soup = self.get_soup(url)
        result = self.new_search_result_item()
        for li in soup.find('ul', {'class': 'cc'}).find_all('li'):
            href = li.a.get('href')
            name = li.a.get('title')
            name = re.sub('<[^>]+>', '', name, re.S)
            comicid = href.rsplit('.', 1)[0].split('-')[-1]
            url = li.img.get('data-original') or li.img.get('src')
            cover_image_url = 'http:' + url
            source_url = self.get_source_url(comicid)
            result.add_result(comicid=comicid, name=name, cover_image_url=cover_image_url, source_url=source_url)
        return result

    def latest(self, page=1):
        url = urljoin(self.SITE_INDEX, '/albums-index-page-%s.html' % page)
        soup = self.get_soup(url)
        result = self.new_search_result_item()
        for li in soup.find('ul', {'class': 'cc'}).find_all('li'):
            href = li.a.get('href')
            name = li.a.get('title')
            name = re.sub('<[^>]+>', '', name, re.S)
            comicid = href.rsplit('.', 1)[0].split('-')[-1]
            cover_image_url = 'http:' + li.img.get('data-original')
            source_url = self.get_source_url(comicid)
            result.add_result(comicid=comicid, name=name, cover_image_url=cover_image_url, source_url=source_url)
        return result
    TAGS = [dict(name='同人志-全部', tag_id='5'), dict(name='同人志-汉化', tag_id='1'), dict(name='同人志-日语', tag_id='12'), dict(name='同人志-CG畫集', tag_id='2'), dict(name='同人志-Cosplay', tag_id='3'), dict(name='单行本-全部', tag_id='6'), dict(name='单行本-汉化', tag_id='9'), dict(name='单行本-日語', tag_id='13')]

    def get_tags(self):
        tags = self.new_tags_item()
        for i in self.TAGS:
            (category, name) = i['name'].split('-', 1)
            tag_id = i['tag_id']
            tags.add_tag(category=category, name=name, tag=tag_id)
        return tags

    def get_tag_result(self, tag, page=1):
        if tag:
            try:
                url = urljoin(self.SITE_INDEX, '/albums-index-page-%s-cate-%s.html' % (page, int(tag)))
            except Exception:
                url = urljoin(self.SITE_INDEX, '/albums-index-page-%s-tag-%s.html' % (page, tag))
        else:
            url = urljoin(self.SITE_INDEX, '/albums.html')
        soup = self.get_soup(url)
        result = self.new_search_result_item()
        for li in soup.find('ul', {'class': 'cc'}).find_all('li'):
            href = li.a.get('href')
            name = li.a.get('title')
            name = re.sub('<[^>]+>', '', name, re.S)
            comicid = href.rsplit('.', 1)[0].split('-')[-1]
            src = li.img.get('data-original') or li.img.get('src')
            cover_image_url = 'https:' + src if src else ''
            source_url = self.get_source_url(comicid)
            result.add_result(comicid=comicid, name=name, cover_image_url=cover_image_url, source_url=source_url)
        return result

    def login(self):
        self.selenium_login(login_url=self.LOGIN_URL, check_login_status_func=self.check_login_status)

    def check_login_status(self):
        session = self.get_session()
        if session.cookies.get('remember', domain='.18comic.org'):
            return True