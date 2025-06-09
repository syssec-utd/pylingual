from ..lc_archive import LcArchive
from ...from_json import from_json
import os
import json
from shutil import rmtree
import unittest
from datetime import datetime
work_dir = os.path.join(os.path.dirname(__file__), 'scratch')
test_file = os.path.join(os.path.dirname(__file__), 'test_json.json')
test_json = {'dataReference': 'test.basic', 'dataSource': None, 'flows': [{'CasNumber': '', 'Comment': '', 'Compartment': ['Forestry and Logging', 'Logging'], 'Name': 'Reforesting, average state or private moist cold softwood forest, INW', 'characterizations': [{'entityType': 'characterization', 'isReference': True, 'quantity': 'cec3a58d-44c3-31f6-9c75-90e6352f0934', 'value': 1.0}], 'entityId': '51d92a19-e550-3000-b49b-e633137eac06', 'entityType': 'flow', 'externalId': 37572, 'origin': 'local.uslci.clean'}, {'CasNumber': '', 'Comment': '', 'Compartment': ['Forestry and Logging', 'Forest Nurseries, Gathering Forest Prod.'], 'Name': 'Greenhouse seedling, softwood, INW', 'characterizations': [{'entityType': 'characterization', 'isReference': True, 'quantity': '8703965a-7a6b-3e3e-a1cf-d9adf7bf1d9f', 'value': 1.0}], 'entityId': '9cc0ccce-8e33-35ca-a3c0-c7bb6c397e95', 'entityType': 'flow', 'externalId': 24235, 'origin': 'local.uslci.clean'}, {'CasNumber': '', 'Comment': '', 'Compartment': ['Utilities', 'Steam and Air-Conditioning Supply'], 'Name': 'Gasoline, combusted in equipment', 'characterizations': [{'entityType': 'characterization', 'isReference': True, 'quantity': '21d34f33-b0af-3d82-9bef-3cf03e0db9dc', 'value': 1.0}], 'entityId': 'c65e7555-7652-377b-b69a-126ba3d9b8b7', 'entityType': 'flow', 'externalId': 5233, 'origin': 'local.uslci.clean'}], 'initArgs': {'ns_uuid': 'a9d158e0-d48c-4427-8c55-42719e9e11cc'}, 'processes': [{'Classifications': ['Forestry and Logging', 'Logging'], 'Comment': 'Important note: although most of the data in the US LCI database has undergone some sort of                     review, the database as a whole has not yet undergone a formal validation process. Please email                     comments to lci@nrel.gov.', 'Name': 'Reforesting, average state or private moist cold softwood forest, INW', 'SpatialScope': 'RNA', 'TemporalScope': "{'begin': '1989-01-01-07:00', 'end': '1996-01-01-07:00'}", 'entityId': '78c8b1e5-ca60-38b6-9a94-dde046560a38', 'entityType': 'process', 'exchanges': [{'direction': 'Input', 'entityType': 'exchange', 'flow': '9cc0ccce-8e33-35ca-a3c0-c7bb6c397e95', 'value': 865.0}, {'direction': 'Input', 'entityType': 'exchange', 'flow': 'c65e7555-7652-377b-b69a-126ba3d9b8b7', 'value': 15.959999999999999}, {'direction': 'Output', 'entityType': 'exchange', 'flow': '51d92a19-e550-3000-b49b-e633137eac06', 'isReference': True, 'value': 1.0}], 'externalId': 'Reforesting, average state or private moist cold softwood forest, INW', 'origin': 'local.uslci.clean'}], 'quantities': [{'Comment': 'EcoSpold01 with altered uuid', 'Name': 'EcoSpold Quantity l', 'entityId': '21d34f33-c0af-3d82-9bef-3cf03e0db9dc', 'entityType': 'quantity', 'externalId': 'l', 'origin': 'local.uslci.clean', 'referenceUnit': 'l'}, {'Comment': 'EcoSpold01', 'Name': 'EcoSpold Quantity Item(s)', 'entityId': '8703965a-7a6b-3e3e-a1cf-d9adf7bf1d9f', 'entityType': 'quantity', 'externalId': 'Item(s)', 'origin': 'local.uslci.clean', 'referenceUnit': 'Item(s)'}, {'Comment': 'EcoSpold01', 'Name': 'EcoSpold Quantity ha', 'entityId': 'cec3a58d-44c3-31f6-9c75-90e6352f0934', 'entityType': 'quantity', 'externalId': 'ha', 'origin': 'local.uslci.clean', 'referenceUnit': 'ha'}]}

def setUpModule():
    if not os.path.exists(test_file):
        with open(test_file, 'w') as fp:
            print('writing to %s' % test_file)
            json.dump(test_json, fp, indent=2, sort_keys=True)

class LcArchiveTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._ar = LcArchive.from_file(test_file)

    def test_get_none(self):
        """
        get None returns None
        :return:
        """
        self.assertIsNone(self._ar[None])

    def test_get_by_uuid(self):
        """
        the standard getitem: put in an entity key, get back the entity.
        :return:
        """
        uuid = '21d34f33-c0af-3d82-9bef-3cf03e0db9dc'
        nsuuid = self._ar._ref_to_nsuuid('l')
        ent = self._ar[uuid]
        self.assertEqual(ent.entity_type, 'quantity')
        self.assertEqual(ent.external_ref, 'l')
        self.assertNotEqual(ent.uuid, nsuuid)
        self.assertEqual(self._ar[nsuuid].uuid, uuid)

    def test_get_by_nsuuid(self):
        uuid = 'cec3a58d-44c3-31f6-9c75-90e6352f0934'
        ent = self._ar['ha']
        self.assertEqual(ent.uuid, uuid)

    def test_get_entity(self):
        """
        An error-preventer: put in an entity itself, get back the entity IF the entity is part of the archive.
        :return:
        """
        ent = self._ar['21d34f33-b0af-3d82-9bef-3cf03e0db9dc']
        self.assertIs(self._ar[ent], ent)

    def test_ents_by_type(self):
        self.assertEqual(len([q for q in self._ar.entities_by_type('q')]), 3)

    def test_recursive_references(self):
        fl_uuid = '9cc0ccce-8e33-35ca-a3c0-c7bb6c397e95'
        q_uuid = '8703965a-7a6b-3e3e-a1cf-d9adf7bf1d9f'
        fl = self._ar[fl_uuid]
        self.assertEqual(self._ar._ref_to_nsuuid(fl.external_ref), fl_uuid)
        self.assertIs(self._ar[q_uuid], fl.reference_entity)

    def test_name(self):
        self.assertEqual(self._ar.ref, test_json['dataReference'])

    def test_json_init(self):
        """
        using load_from_dict(), you cannot read namespace uuid automatically from the json. But, you can specify source and
        ref manually.
        :return:
        """
        ar = LcArchive('/my/file')
        ar._entities['21d34f33-b0af-3d82-9bef-3cf03e0db9dc'] = None
        ar.load_from_dict(from_json(test_file), jsonfile='/my/test/json')
        self.assertIn(test_json['dataReference'], ar.catalog_names)
        self.assertEqual(ar.ref, 'local.my.file')
        self.assertSequenceEqual([k for k in ar.get_sources(test_json['dataReference'])], [None])
        uuid = 'cec3a58d-44c3-31f6-9c75-90e6352f0934'
        nsuuid = ar._ref_to_nsuuid('ha')
        self.assertNotEqual(uuid, nsuuid)
        ent = ar['ha']
        ent1 = ar[nsuuid]
        self.assertIs(ent, ent1)
        self.assertEqual(ar[nsuuid].uuid, uuid)

    def test_assign_name(self):
        ar = LcArchive(test_json['dataSource'], ref='test.basic', ns_uuid=test_json['initArgs']['ns_uuid'])
        self.assertIsNone(ar.source)
        self.assertEqual(ar.ref, 'test.basic')
        ar.load_from_dict(from_json(test_file), jsonfile=test_file)
        self.assertEqual(ar.source, test_file)
        self.assertEqual(ar.ref, 'test.basic')

class DescendantTest(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        try:
            rmtree(work_dir)
        except FileNotFoundError:
            pass

    def test_create_descendant(self):
        new_date = datetime.now().strftime('%Y%m%d')
        sig = 'mybaby'
        ar = LcArchive.from_file(test_file)
        dref = ar.create_descendant(work_dir, signifier=sig, force=True)
        self.assertEqual(dref, ar.ref)
        self.assertTrue(dref.startswith('.'.join(['test.basic', sig, new_date])))
        self.assertSetEqual({k for k in ar.get_sources(dref)}, {os.path.join(work_dir, '%s.json.gz' % dref)})
if __name__ == '__main__':
    unittest.main()