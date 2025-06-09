"""Tests for Tree.path2id('')"""
from breezy.tests import TestNotApplicable
from breezy.tests.per_tree import TestCaseWithTree
from breezy.workingtree import SettingFileIdUnsupported

class TestGetRootID(TestCaseWithTree):

    def make_tree_with_default_root_id(self):
        tree = self.make_branch_and_tree('tree')
        return self._convert_tree(tree)

    def make_tree_with_fixed_root_id(self):
        tree = self.make_branch_and_tree('tree')
        if not tree.supports_setting_file_ids():
            self.assertRaises(SettingFileIdUnsupported, tree.set_root_id, b'custom-tree-root-id')
            self.skipTest('tree format does not support setting tree id')
        tree.set_root_id(b'custom-tree-root-id')
        return self._convert_tree(tree)

    def test_get_root_id_default(self):
        tree = self.make_tree_with_default_root_id()
        if not tree.supports_file_ids:
            raise TestNotApplicable('file ids not supported')
        with tree.lock_read():
            self.assertIsNot(None, tree.path2id(''))

    def test_get_root_id_fixed(self):
        try:
            tree = self.make_tree_with_fixed_root_id()
        except SettingFileIdUnsupported:
            raise TestNotApplicable('file ids not supported')
        with tree.lock_read():
            self.assertEqual(b'custom-tree-root-id', tree.path2id(''))