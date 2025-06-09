"""
Tests that the variable Folders API is properly suported
"""
import os
from unittest import TestCase
from pycrunch.shoji import Catalog
from fixtures import NEWS_DATASET
from scrunch import connect
from scrunch import get_dataset
from scrunch.datasets import Variable
from scrunch.exceptions import InvalidPathError
from scrunch.folders import Folder
HOST = os.environ['SCRUNCH_HOST']
username = os.environ['SCRUNCH_USER']
password = os.environ['SCRUNCH_PASS']
site = connect(username, password, HOST)

def setup_folders(ds):
    sess = ds.session
    ds.settings.edit(variable_folders=True)
    ds.variables.create({'element': 'shoji:entity', 'body': {'name': 'testvar1', 'type': 'numeric'}})
    ds.variables.create({'element': 'shoji:entity', 'body': {'name': 'testvar2', 'type': 'numeric'}})
    ds.variables.create({'element': 'shoji:entity', 'body': {'name': 'testvar3', 'type': 'numeric'}})
    ds.variables.create({'element': 'shoji:entity', 'body': {'name': 'testvar4', 'type': 'numeric'}})
    ds.variables.create({'element': 'shoji:entity', 'body': {'name': 'testvar5', 'type': 'numeric'}})
    ds.variables.create({'element': 'shoji:entity', 'body': {'name': 'testvar6', 'type': 'numeric'}})
    ds.refresh()
    sf1 = Catalog(sess, body={'name': 'Subfolder 1'})
    sf1 = ds.folders.create(sf1)
    sfa = Catalog(sess, body={'name': 'Subfolder A'})
    sfa = sf1.create(sfa)
    sf2 = Catalog(sess, body={'name': 'Subfolder 2'})
    sf2 = ds.folders.create(sf2)
    variables = ds.variables.by('alias')
    sf1.patch({'index': {variables['age'].entity_url: {}}})
    sfa.patch({'index': {variables['gender'].entity_url: {}}})
    sf2.patch({'index': {variables['socialmedia'].entity_url: {}}})

class TestFolders(TestCase):

    def setUp(self):
        self._ds = site.datasets.create({'element': 'shoji:entity', 'body': {'name': 'test_folders', 'table': {'element': 'crunch:table', 'metadata': NEWS_DATASET}}}).refresh()
        ds = self._ds
        setup_folders(ds)
        self.ds = get_dataset(ds.body.id)

    def test_get_folders(self):
        ds = self.ds
        public = ds.folders.get('|')
        sf1 = ds.folders.get('| Subfolder 1')
        sfa = ds.folders.get('| Subfolder 1 | Subfolder A')
        sfa2 = public.get('Subfolder 1 | Subfolder A')
        sfa3 = sf1.get('Subfolder A')
        self.assertEqual(sfa.url, sfa2.url)
        self.assertEqual(sfa.url, sfa3.url)
        variable = ds.folders.get('| Subfolder 1 | Subfolder A | Gender')
        self.assertTrue(isinstance(sf1, Folder))
        self.assertTrue(isinstance(sfa, Folder))
        self.assertTrue(isinstance(variable, Variable))
        self.assertEqual(sf1.name, 'Subfolder 1')
        self.assertEqual(sfa.name, 'Subfolder A')
        self.assertEqual(sf1.parent, public)
        self.assertEqual(sfa.parent.name, sf1.name)
        self.assertEqual(sfa.parent.path, sf1.path)
        self.assertEqual(sfa.path, '| Subfolder 1 | Subfolder A')
        self.assertEqual(variable.alias, 'gender')
        self.assertEqual(variable.type, 'categorical')
        bad_path = '| bad folder'
        with self.assertRaises(InvalidPathError) as err:
            ds.folders.get(bad_path)
        self.assertEqual(str(err.exception), 'Invalid path: %s' % bad_path)

    def test_create_folder(self):
        ds = self.ds
        public = ds.folders.get('|')
        mit = public.create_folder('Made in test')
        self.assertEqual(mit.path, '| Made in test')
        mit2 = public.get(mit.name)
        self.assertEqual(mit2.url, mit.url)
        nested = mit.create_folder('nested level')
        self.assertEqual(mit.get_child(nested.name).url, nested.url)

    def test_create_folder_with_variables(self):
        ds = self.ds
        public = ds.folders.public
        sf = public.create_folder('with children', alias=['testvar1', 'testvar2'])
        self.assertEqual([Variable, Variable], [type(c) for c in sf.children])
        self.assertEqual(['testvar1', 'testvar2'], [c.alias for c in sf.children])

    def test_reorder_folder(self):
        ds = self.ds
        public = ds.folders.get('|')
        folder = public.create_folder('ToReorder')
        sf1 = folder.create_folder('1')
        sf2 = folder.create_folder('2')
        sf3 = folder.create_folder('3')
        var = ds['testvar1']
        folder.move_here([var])
        children = folder.children
        self.assertEqual([c.url for c in children], [c.url for c in [sf1, sf2, sf3, var]])
        self.assertEqual(list(map(type, children)), [Folder, Folder, Folder, Variable])
        folder.reorder([sf2, var, sf3, sf1])
        children = folder.children
        self.assertEqual([c.url for c in children], [c.url for c in [sf2, var, sf3, sf1]])
        folder.reorder(var.alias, sf1.name, sf2.name, sf3.name)
        self.assertEqual([c.url for c in folder.children], [c.url for c in [var, sf1, sf2, sf3]])

    def test_move_to_folder(self):
        ds = self.ds
        sf = ds.folders.public.create_folder('target')
        ds['testvar1'].move_to_folder(sf.path)
        self.assertEqual(['testvar1'], [c.alias for c in sf.children])

    def test_move_between_folders(self):
        public = self.ds.folders.public
        target1 = public.create_folder('t1')
        target2 = public.create_folder('t2')
        self.assertEqual(target1.children, [])
        self.assertEqual(target2.children, [])
        var1 = self.ds['testvar2']
        var2 = self.ds['testvar3']
        target1.move_here([var2, var1])
        self.assertEqual([c.url for c in target1.children], [var2.url, var1.url])
        nested = target1.create_folder('nested')
        self.assertEqual([c.url for c in target1.children], [var2.url, var1.url, nested.url])
        target2.move_here(var2)
        self.assertEqual([c.url for c in target1.children], [var1.url, nested.url])
        self.assertEqual([c.url for c in target2.children], [var2.url])
        target2.move_here([nested, var1])
        self.assertEqual([c.url for c in target2.children], [var2.url, nested.url, var1.url])
        self.assertEqual([c.url for c in target1.children], [])
        nested.move_here(var1)
        self.assertEqual([c.url for c in target2.children], [var2.url, nested.url])
        self.assertEqual([c.url for c in nested.children], [var1.url])
        target1.move_here(nested)
        self.assertEqual([c.url for c in target2.children], [var2.url])
        self.assertEqual([c.url for c in target1.children], [nested.url])

    def test_move_here_position(self):
        public = self.ds.folders.public
        sf = public.create_folder('here')
        sf.move_here(self.ds['testvar1'])
        sf.move_here(self.ds['testvar2'], before='testvar1')
        self.assertEqual([c.name for c in sf.children], ['testvar2', 'testvar1'])
        sf.move_here(self.ds['testvar3'], after='testvar2')
        self.assertEqual([c.name for c in sf.children], ['testvar2', 'testvar3', 'testvar1'])
        sf.move_here(self.ds['testvar4'], position=1)
        self.assertEqual([c.name for c in sf.children], ['testvar2', 'testvar4', 'testvar3', 'testvar1'])

    def test_move_by_alias(self):
        public = self.ds.folders.public
        target = public.create_folder('test_move_by_alias')
        target.move_here('testvar2')
        self.assertEqual([c.name for c in target.children], ['testvar2'])

    def test_make_folder_in_position(self):
        public = self.ds.folders.public.create_folder('testhere')
        public.create_folder('p1')
        public.create_folder('p2')
        public.create_folder('p3')
        public.create_folder('A', before='p2')
        self.assertEqual([c.name for c in public.children], ['p1', 'A', 'p2', 'p3'])
        public.create_folder('B', after='p2')
        self.assertEqual([c.name for c in public.children], ['p1', 'A', 'p2', 'B', 'p3'])
        public.create_folder('C', position=3)
        self.assertEqual([c.name for c in public.children], ['p1', 'A', 'p2', 'C', 'B', 'p3'])

    def test_hide_variables(self):
        hidden_folder = self.ds.folders.hidden
        public = self.ds.folders.public
        var1 = self.ds['testvar4']
        var2 = self.ds['testvar5']
        public.move_here(var1, var2)
        hidden_folder.move_here(var2)
        var1_id = var1.resource.body.id
        var2_id = var2.resource.body.id
        self.assertTrue(var2_id in self._ds.folders.hidden.by('id'))
        self.assertTrue(var2_id not in self._ds.folders.by('id'))
        self.assertTrue(var1_id in self._ds.folders.by('id'))
        self.assertTrue(var1_id not in self._ds.folders.hidden.by('id'))

    def test_rename(self):
        public = self.ds.folders.public
        sf = public.create_folder('rename me')
        sf.rename('renamed')
        self.assertTrue('renamed' in [c.name for c in public.children])
        self.assertEqual(sf.name, 'renamed')

    def test_delete_folder(self):
        public = self.ds.folders.public
        var = self.ds['testvar6']
        sf = public.create_folder('delete me')
        sf.move_here(var)
        self.assertTrue(var.url in self._ds.variables.index)
        sf.delete()
        self.assertFalse(sf.url in [c.url for c in public.children])

    def test_dict_protocol(self):
        public = self.ds.folders.public
        sf1 = public.create_folder('level1')
        sf1a = public.create_folder('level1a')
        sf2 = sf1.create_folder('level2')
        self.assertEqual(public[sf2.path].url, sf2.url)
        self.assertEqual(public[sf1.name].url, sf1.url)
        self.assertEqual(sf1[sf2.name].url, sf2.url)
        self.assertEqual([c.url for c in public], [c.url for c in public.children])
        self.assertEqual(set(dict(public).keys()), set(public.keys()))
        self.assertEqual({c.url for c in dict(public).values()}, {c.url for c in public.children})
        self.assertEqual(dict(public)[sf1.name].url, sf1.url)

    def test_dict_protocol_on_helper(self):
        public = self.ds.folders.public
        sf1 = public.create_folder('level1')
        sf1a = public.create_folder('level1a')
        sf2 = sf1.create_folder('level2')
        top_level = self.ds.folders
        self.assertEqual(top_level[sf2.path].url, sf2.url)
        self.assertEqual(top_level[sf1.name].url, sf1.url)
        self.assertEqual([c.url for c in top_level], [c.url for c in public.children])
        self.assertEqual(set(dict(top_level).keys()), set(public.keys()))
        self.assertEqual({c.url for c in dict(top_level).values()}, {c.url for c in public.children})
        self.assertEqual(dict(top_level)[sf1.name].url, sf1.url)