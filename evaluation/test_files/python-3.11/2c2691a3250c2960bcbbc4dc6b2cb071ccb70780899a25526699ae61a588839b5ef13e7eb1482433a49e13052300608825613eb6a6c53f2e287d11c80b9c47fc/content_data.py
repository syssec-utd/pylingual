import os
from datetime import date, datetime
from dataclasses import dataclass, field
import re
from typing import Optional
from src.config import config
from src.lib.fs import basename
from slugify.slugify import slugify
TITLE_DELIMETER = ' - '
DEFAULT_DATE = datetime.fromtimestamp(0)

@dataclass
class ContentData:
    filename: str = ''
    placeholder: Optional[str] = None
    meta: dict = field(default_factory=dict)
    content: str = ''
    entities: list = field(default_factory=list)
    match: dict = field(default_factory=dict)

    @property
    def title(self):
        if 'title' in self.match and self.match['title'] is not None:
            return self.match['title']
        meta_title = self.meta.get('title')
        if isinstance(meta_title, str):
            return meta_title
        title, _ = os.path.splitext(basename(self.filename))
        if TITLE_DELIMETER in title:
            *_, title = title.split(TITLE_DELIMETER)
            return title
        return title

    @property
    def date(self):
        meta_date = self.meta.get('date')
        if isinstance(meta_date, date):
            return datetime.strptime(meta_date.strftime('%Y%m%d'), '%Y%m%d')
        return DEFAULT_DATE

    def __lt__(self, other):
        return self.date < other.date

    @property
    def slug(self):
        meta_slug = self.meta.get('slug')
        if isinstance(meta_slug, str):
            return f'{meta_slug}.html'
        file, _ = os.path.splitext(self.filename)
        if '.' not in file:
            slug = slugify(os.path.basename(file))
            return f'{slug}.html'
        return os.path.basename(file)

    @property
    def id(self):
        filename, _ = os.path.splitext(self.filename)
        return slugify(filename)

    @property
    def ext(self):
        print(self.filename)
        _, ext = os.path.splitext(self.filename)
        return ext

    @property
    def is_private(self):
        if config.drafts and self.meta.get('draft'):
            return False
        if self.meta.get('published'):
            return False
        return True

    @property
    def _placeholder_title(self):
        if not self.placeholder:
            return None
        [title] = re.findall('\\[\\[([\\d\\s\\w\\-&|]*)\\]\\]', self.placeholder or '')
        if not '|' in title:
            return None
        _, title = title.split('|')
        return title.strip()