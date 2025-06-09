import io
import os
import re
import numpy as np
import pytest
from lxml import etree
from extractnet import Blockifier, BlockifyError
from extractnet.features import KohlschuetterFeatures
from extractnet.compat import range_, str_cast

@pytest.fixture(scope='module')
def html():
    fname = os.path.join('test', 'datafiles', 'HTML', 'page_for_testing.html')
    with io.open(fname, mode='rt') as f:
        html_ = f.read()
    return html_

def block_output_tokens(blocks, true_tokens):
    """
    blocks = the output from blockify
    true_tokens = a list of true tokens
    """
    assert len(blocks) == len(true_tokens)
    for k in range_(len(blocks)):
        block_tokens = re.split('\\s+', blocks[k].text.strip())
        assert block_tokens == true_tokens[k]

def link_output_tokens(blocks, true_tokens):
    assert len(blocks) == len(true_tokens)
    link_tokens = [ele.link_tokens for ele in blocks]
    for k in range_(len(link_tokens)):
        assert link_tokens[k] == true_tokens[k]

def css_output_tokens(blocks, attrib, true_tokens):
    assert len(blocks) == len(true_tokens)
    for k in range_(len(blocks)):
        css_tokens = re.split('\\s+', blocks[k].css[attrib].strip())
        assert css_tokens == true_tokens[k]

class TestBlockifier(object):

    def test_lxml_error(self):
        """tests the case where lxml raises an error during parsing

        also handles case where lxml returns None for the tree"""
        with pytest.raises(BlockifyError):
            Blockifier.blockify('')
        assert etree.fromstring('<!--', etree.HTMLParser(recover=True)) is None
        with pytest.raises(BlockifyError):
            Blockifier.blockify('<!--')

    def test_very_simple(self):
        """test_very_simple"""
        s = '<div>some text\n                    <script> skip this </script>\n                    more text here\n               </div>'
        blocks = Blockifier.blockify(s)
        block_output_tokens(blocks, [['some', 'text', 'more', 'text', 'here']])

    def test_very_simple2(self):
        s = '<div>some text <i>in italic</i> and something else\n                    <script> <div>skip this</div> </script>\n                    <b>bold stuff</b> after the script\n               </div>'
        blocks = Blockifier.blockify(s)
        block_output_tokens(blocks, [['some', 'text', 'in', 'italic', 'and', 'something', 'else', 'bold', 'stuff', 'after', 'the', 'script']])

    @staticmethod
    def count_divs(tree):
        div_xpath = etree.XPath('//div')
        TestBlockifier.div_count = len(div_xpath(tree))

    def test_callback(self):
        s = '<div>some text <i>in italic</i> and something else\n                    <pre> <div>skip this</div> </pre>\n                    <b>bold stuff</b> after the script\n               </div>'
        blocks = Blockifier.blockify(s, parse_callback=self.count_divs)
        assert self.div_count == 2

    def test_simple_two_blocks(self):
        s = '<h1>A title <i>with italics</i> and other words</h1>\n               some text outside the h1\n               <div>a div <span class="test"> with a span </span> more </div>'
        blocks = Blockifier.blockify(s)
        block_output_tokens(blocks, [['A', 'title', 'with', 'italics', 'and', 'other', 'words', 'some', 'text', 'outside', 'the', 'h1'], ['a', 'div', 'with', 'a', 'span', 'more']])

    def test_comment(self):
        s = '<H1>h1 tag word</H1>\n               <!-- a comment -->\n               orphaned text\n               <TABLE><tr><td>table data</td></tr><tr><td>second row</td></tr></TABLE>\n               final\n               '
        blocks = Blockifier.blockify(s)
        block_output_tokens(blocks, [['h1', 'tag', 'word', 'orphaned', 'text'], ['table', 'data', 'second', 'row', 'final']])

    def test_empty_blocks(self):
        s = '<div> .! </div>\n                some text\n               <h1> in an h1 </h1>\n               <p> ! _ </p>\n            '
        blocks = Blockifier.blockify(s)
        block_output_tokens(blocks, [['.!', 'some', 'text'], ['in', 'an', 'h1']])

    def test_nested_blocks(self):
        s = 'initial text\n            <div>div <p> with paragraph </p>\n            after Paragraph\n            <div> nested div <div> and again </div>here</div>\n            </div>\n            final\n            <div> <i> italic </i> before <h1>tag</h1></div>'
        blocks = Blockifier.blockify(s)
        block_output_tokens(blocks, [['initial', 'text'], ['div'], ['with', 'paragraph', 'after', 'Paragraph'], ['nested', 'div'], ['and', 'again', 'here', 'final'], ['italic', 'before'], ['tag']])

    def test_anchors(self):
        s = '<a href=".">anchor text</a>\n               more\n               <div>text <a href=".">123</a><div>MORE!</div></div>\n               an img link<a href="."><img src="."></a>there\n               <table><tr><td><a href=".">WILL <img src="."> THIS PASS <b>THE TEST</b> ??</a></tr></td></table>'
        blocks = Blockifier.blockify(s)
        block_output_tokens(blocks, [['anchor', 'text', 'more'], ['text', '123'], ['MORE!', 'an', 'img', 'link', 'there'], ['WILL', 'THIS', 'PASS', 'THE', 'TEST', '??']])
        link_output_tokens(blocks, [['anchor', 'text'], ['123'], [], ['WILL', 'THIS', 'PASS', 'THE', 'TEST', '??']])

    def test_unicode(self):
        s = u'<div><div><a href="."> the registered trademark ®</a></div></div>'
        blocks = Blockifier.blockify(s)
        block_output_tokens(blocks, [['the', 'registered', 'trademark', u'®']])
        link_output_tokens(blocks, [['the', 'registered', 'trademark', u'®']])

    def test_all_non_english(self):
        s = u'<div> <div> δογ </div> <div> <a href="summer">été</a> </div>\n         <div> 报道一出 </div> </div>'
        blocks = Blockifier.blockify(s)
        block_output_tokens(blocks, [[u'δογ'], [u'été'], [u'报道一出']])
        link_output_tokens(blocks, [[], [u'été'], []])

    def test_class_id(self):
        s = '<div CLASS=\'d1\'>text in div\n                <h1 id="HEADER">header</h1>\n                <div class="nested">dragnet</div>\n                </div>'
        blocks = Blockifier.blockify(s)
        block_output_tokens(blocks, [['text', 'in', 'div'], ['header'], ['dragnet']])
        css_output_tokens(blocks, 'id', [[''], ['header'], ['']])
        css_output_tokens(blocks, 'class', [['d1'], [''], ['nested']])

    def test_class_id_unicode(self):
        s = b'<div CLASS=\' class1 \xc2\xae\'>text in div\n                <h1 id="HEADER">header</h1>\n                </div>'
        blocks = Blockifier.blockify(s, encoding='utf-8')
        block_output_tokens(blocks, [['text', 'in', 'div'], ['header']])
        css_output_tokens(blocks, 'id', [[''], ['header']])
        css_output_tokens(blocks, 'class', [['class1', str_cast(b'\xc2\xae')], ['']])

    def test_invalid_bytes(self):
        s = b"<div CLASS='\x80'>text in div</div><p>invalid bytes \x80</p>"
        blocks = Blockifier.blockify(s, encoding='utf-8')
        block_output_tokens(blocks, [['text', 'in', 'div']])
        css_output_tokens(blocks, 'class', [[str_cast(b'\xc2\x80')]])

    def test_big_html(self, html):
        s = html
        blocks = Blockifier.blockify(s)
        block_output_tokens(blocks, [['Inside', 'the', 'h1', 'tag'], ['First', 'line', 'of', 'the', 'content', 'in', 'bold'], ['A', 'paragraph', 'with', 'a', 'link', 'and', 'some', 'additional', 'words.'], ['Second', 'paragraph', 'Insert', 'a', 'block', 'quote', 'here'], ['Some', 'more', 'text', 'after', 'the', 'image'], ['An', 'h2', 'tag', 'just', 'for', 'kicks'], ['Finally', 'more', 'text', 'at', 'the', 'end', 'of', 'the', 'content'], ['This', 'is', 'a', 'comment'], ['with', 'two', 'paragraphs', 'and', 'some', 'comment', 'spam'], ['Second', 'comment'], ['Footer', 'text']])
        link_output_tokens(blocks, [[], [], ['a', 'link'], [], [], [], [], [], ['and', 'some', 'comment', 'spam'], [], []])
        css_output_tokens(blocks, 'class', [[''], ['title'], ['link'], [''], [''], [''], [''], [''], [''], [''], ['footer']])
        css_output_tokens(blocks, 'id', [[''], ['content'], ['para'], [''], [''], [''], [''], [''], [''], [''], ['']])

class TestKohlschuetter(object):

    def test_small_doc(self):
        kf = KohlschuetterFeatures()
        s = '<html></html>'
        with pytest.raises(ValueError):
            kf.transform(Blockifier.blockify(s))
        s = '<html> <p>a</p> <div>b</div> </html>'
        with pytest.raises(ValueError):
            kf.transform(Blockifier.blockify(s))

    def test_transform(self):
        kf = KohlschuetterFeatures()
        s = "<html> <p>first </p> <div> <p>second block with <a href=''>anchor</a> </p> <p>the third block</p> </div> </html>"
        blocks = Blockifier.blockify(s)
        features = kf.transform(blocks)
        block_output_tokens(blocks, [['first'], ['second', 'block', 'with', 'anchor'], ['the', 'third', 'block']])
        link_output_tokens(blocks, [[], ['anchor'], []])
        text_density = [1.0, 4.0, 3.0]
        link_density = [1.0, 0.25, 1.0 / 3.0]
        assert np.allclose(features[0, :], [0.0, 0.0, link_density[0], text_density[0], link_density[1], text_density[1]])
        assert np.allclose(features[1, :], [link_density[0], text_density[0], link_density[1], text_density[1], link_density[2], text_density[2]])
        assert np.allclose(features[2, :], [link_density[1], text_density[1], link_density[2], text_density[2], 0.0, 0.0])