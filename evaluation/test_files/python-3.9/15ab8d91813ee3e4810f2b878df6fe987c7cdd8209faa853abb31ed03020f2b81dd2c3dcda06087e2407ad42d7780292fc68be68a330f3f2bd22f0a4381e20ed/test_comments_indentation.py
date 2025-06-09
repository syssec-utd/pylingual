from tests.common import RuleTestCase

class CommentsIndentationTestCase(RuleTestCase):
    rule_id = 'comments-indentation'

    def test_disable(self):
        conf = 'comments-indentation: disable'
        self.check('---\n # line 1\n# line 2\n  # line 3\n  # line 4\n\nobj:\n # these\n   # are\n  # [good]\n# bad\n      # comments\n  a: b\n\nobj1:\n  a: 1\n  # comments\n\nobj2:\n  b: 2\n\n# empty\n#\n# comment\n...\n', conf)

    def test_enabled(self):
        conf = 'comments-indentation: enable'
        self.check('---\n# line 1\n# line 2\n', conf)
        self.check('---\n # line 1\n# line 2\n', conf, problem=(2, 2))
        self.check('---\n  # line 1\n  # line 2\n', conf, problem1=(2, 3))
        self.check('---\nobj:\n  # normal\n  a: b\n', conf)
        self.check('---\nobj:\n # bad\n  a: b\n', conf, problem=(3, 2))
        self.check('---\nobj:\n# bad\n  a: b\n', conf, problem=(3, 1))
        self.check('---\nobj:\n   # bad\n  a: b\n', conf, problem=(3, 4))
        self.check('---\nobj:\n # these\n   # are\n  # [good]\n# bad\n      # comments\n  a: b\n', conf, problem1=(3, 2), problem2=(4, 4), problem3=(6, 1), problem4=(7, 7))
        self.check('---\nobj1:\n  a: 1\n  # the following line is disabled\n  # b: 2\n', conf)
        self.check('---\nobj1:\n  a: 1\n  # b: 2\n\nobj2:\n  b: 2\n', conf)
        self.check('---\nobj1:\n  a: 1\n  # b: 2\n# this object is useless\nobj2: "no"\n', conf)
        self.check('---\nobj1:\n  a: 1\n# this object is useless\n  # b: 2\nobj2: "no"\n', conf, problem=(5, 3))
        self.check('---\nobj1:\n  a: 1\n  # comments\n  b: 2\n', conf)
        self.check('---\nmy list for today:\n  - todo 1\n  - todo 2\n  # commented for now\n  # - todo 3\n...\n', conf)

    def test_first_line(self):
        conf = 'comments-indentation: enable'
        self.check('# comment\n', conf)
        self.check('  # comment\n', conf, problem=(1, 3))

    def test_no_newline_at_end(self):
        conf = 'comments-indentation: enable\nnew-line-at-end-of-file: disable\n'
        self.check('# comment', conf)
        self.check('  # comment', conf, problem=(1, 3))

    def test_empty_comment(self):
        conf = 'comments-indentation: enable'
        self.check('---\n# hey\n# normal\n#\n', conf)
        self.check('---\n# hey\n# normal\n #\n', conf, problem=(4, 2))

    def test_inline_comment(self):
        conf = 'comments-indentation: enable'
        self.check('---\n- a  # inline\n# ok\n', conf)
        self.check('---\n- a  # inline\n # not ok\n', conf, problem=(3, 2))
        self.check('---\n # not ok\n- a  # inline\n', conf, problem=(2, 2))