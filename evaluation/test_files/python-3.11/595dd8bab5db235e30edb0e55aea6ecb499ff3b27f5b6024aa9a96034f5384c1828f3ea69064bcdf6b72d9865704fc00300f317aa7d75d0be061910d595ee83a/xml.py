from bs4 import BeautifulSoup
from bs4.element import NavigableString
from logging import getLogger
from zpretty.attributes import PrettyAttributes
from zpretty.elements import PrettyElement
from zpretty.prettifier import ZPrettifier
logger = getLogger(__name__)

class AnyIn(object):

    def __contains__(self, item):
        return True

class XMLAttributes(PrettyAttributes):
    """Customized attribute formatter for zcml"""
    _boolean_attributes_are_allowed = False
    _known_boolean_attributes = ()
    _multiline_attributes = ()
    _xml_attribute_order = ()

    def sort_attributes(self, name):
        """Sort ZCML attributes in a consistent way"""
        if name in self._xml_attribute_order:
            return (100 + self._xml_attribute_order.index(name), name)
        return super(XMLAttributes, self).sort_attributes(name)

class XMLElement(PrettyElement):
    attribute_klass = XMLAttributes
    preserve_text_whitespace_elements = AnyIn()

    def is_self_closing(self):
        """Is this element self closing?"""
        if not self.is_tag():
            raise ValueError('This is not a tag')
        return not self.getchildren()

    @property
    def tag(self):
        """Return the tag name"""
        prefix = getattr(self.context, 'prefix', '')
        if not prefix:
            return self.context.name
        return f'{prefix}:{self.context.name}'

    @property
    def text(self):
        """Return the text contained in this element (if any)

        Convert the text characters to html entities
        """
        if not isinstance(self.context, NavigableString):
            return ''
        if self.is_comment():
            return self.context
        return self.escaper.substitute_xml(self.context.string)

class XMLPrettifier(ZPrettifier):
    """Prettify according to the ZCML style guide"""
    parser = 'xml'
    pretty_element = XMLElement

    def get_soup(self, text):
        """Tries to get the soup from the given test

        If the text is not some xml like think a dummy element will be used to wrap it.
        """
        original_soup = BeautifulSoup(text, self.parser)
        if original_soup.is_xml:
            return original_soup
        markup = '<{null}>{text}</{null}>'.format(null=self.pretty_element.null_tag_name, text=text)
        wrapped_soup = BeautifulSoup(markup, self.parser)
        return getattr(wrapped_soup, self.pretty_element.null_tag_name)