from __future__ import annotations
import re
from typing import Optional
from jangle.patterns import RULES, match_rule
from jangle.utils import split_subtags

class Extension:
    singleton: str
    texts: list[str]

    def __init__(self, match: re.Match[str] | str) -> None:
        if isinstance(match, str):
            match = match_rule('extension', match)
        self.singleton = match.group('singleton')
        self.texts = split_subtags(match.group('ext_text'))

    def __str__(self) -> str:
        return '-'.join([self.singleton, *self.texts])

    def __repr__(self) -> str:
        return f"<Extension '{self}'>"

class LangTag:
    lang: str
    extlang: Optional[str]
    script: Optional[str]
    region: Optional[str]
    variants: list[str] = []
    extensions: list[Extension]
    private: Optional[str]

    def __init__(self, match: re.Match[str] | str) -> None:
        if isinstance(match, str):
            match = match_rule('langtag', match)
        groups = match.groupdict('')
        self.lang = groups['iso_639'].lower()
        self.extlang = groups['extlang'].lower() or None
        self.script = groups['script'].title() or None
        self.region = groups['region'].upper() or None
        self.private = groups['private_subtag'].lower().removeprefix('x-') or None
        if groups['variants']:
            self.variants = split_subtags(groups['variants'].lower())
        else:
            self.variants = []
        self.extensions = list(map(Extension, RULES['extension'].finditer(groups['extensions'].lower())))

    def __str__(self) -> str:
        subtags = [self.lang]
        subtags.extend(filter(None, [self.extlang, self.script, self.region]))
        subtags.extend(self.variants)
        subtags.extend(map(str, self.extensions))
        if self.private:
            subtags.extend(['x', self.private])
        return '-'.join(subtags)

    def __contains__(self, val: LangTag | re.Match[str] | str) -> bool:
        if isinstance(val, re.Match | str):
            val = type(self)(val)
        if val.lang != self.lang:
            return False
        for attr_name in ['script', 'extlang', 'region', 'private']:
            attr = getattr(val, attr_name)
            if attr and attr != getattr(self, attr_name):
                return False
        for variant in val.variants:
            if variant not in self.variants:
                return False
        self_extensions = set(map(str, self.extensions))
        for extension in val.extensions:
            if str(extension) not in self_extensions:
                return False
        return True

    def __repr__(self) -> str:
        return f"<LangTag '{self}'>"

class LanguageTagLite:
    langtag: Optional[LangTag]
    private: Optional[str]
    grandfathered: Optional[str]

    def __init__(self, match: re.Match[str] | str) -> None:
        if isinstance(match, str):
            match = match_rule('Language-Tag', match)
        groups = match.groupdict('')
        if groups['langtag']:
            self.langtag = LangTag(match)
        else:
            self.langtag = None
        self.private = groups['private_tag'].lower().removeprefix('x-') or None
        self.grandfathered = groups['grandfathered'].lower() or None

    def __str__(self) -> str:
        if self.grandfathered:
            return self.grandfathered
        if self.private:
            return '-'.join(['x', self.private])
        return str(self.langtag)

    def __repr__(self) -> str:
        return f"<LanguageTagLite '{self}'>"