from atc_tools.testing.DataframeTestCase import DataframeTestCase
from pyspark.sql import DataFrame
from pyspark.sql.types import IntegerType, StringType, StructField, StructType
from atc import Configurator
from atc.functions import get_unique_tempview_name
from atc.utils import DataframeCreator
from tests.cluster.sql.DeliverySqlServer import DeliverySqlServer
from . import extras

class DeliverySqlServerTests(DataframeTestCase):
    tc = None
    sql_server = None
    table_name = get_unique_tempview_name()
    table_upsert_name = get_unique_tempview_name()
    view_name = get_unique_tempview_name()

    @classmethod
    def setUpClass(cls):
        cls.sql_server = DeliverySqlServer()
        cls.tc = Configurator()
        cls.tc.add_resource_path(extras)
        cls.tc.reset(debug=True)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.sql_server.drop_table_by_name(cls.table_name)
        cls.sql_server.drop_table_by_name(cls.table_upsert_name)
        t1 = cls.tc.table_name('SqlTestTable1')
        t2 = cls.tc.table_name('SqlTestTable2')
        v1 = cls.tc.table_name('SqlTestView')
        cls.sql_server.drop_table_by_name(t1)
        cls.sql_server.drop_table_by_name(t2)
        cls.sql_server.drop_view_by_name(v1)
        cls.tc.reset(debug=False)

    def test01_can_connect(self):
        self.sql_server.test_odbc_connection()
        self.assertTrue(True)

    def test02_can_create_dummy(self):
        self.create_test_table()
        self.assertTrue(True)

    def test03_can_read_dummy(self):
        self.sql_server.read_table_by_name(self.table_name)
        self.assertTrue(True)

    def test03_can_truncate_dummy(self):
        self.insert_single_row()
        df_with_data = self.sql_server.read_table_by_name(self.table_name)
        self.assertEqual(df_with_data.count(), 1)
        self.sql_server.truncate_table_by_name(self.table_name)
        df_without_data = self.sql_server.read_table_by_name(self.table_name)
        self.assertEqual(df_without_data.count(), 0)

    def test04_can_load_sql_spark_dummy(self):
        sql_argument = f'\n                (select * from {self.table_name}) target\n                                '
        self.insert_single_row()
        df_with_data = self.sql_server.load_sql(sql_argument)
        self.assertEqual(df_with_data.count(), 1)

    def test05_can_drop_table_dummy(self):
        self.sql_server.drop_table_by_name(self.table_name)
        sql_argument = f"\n        (SELECT * FROM INFORMATION_SCHEMA.TABLES\n        WHERE TABLE_NAME = '{self.table_name}') target\n        "
        table_exists = self.sql_server.load_sql(sql_argument)
        self.assertEqual(table_exists.count(), 0)

    def test06_write_table_spark_dummy(self):
        self.create_test_table()
        df_export = self.create_data()
        self.sql_server.write_table_by_name(df_export, self.table_name)
        df_with_data = self.sql_server.read_table_by_name(self.table_name)
        self.assertEqual(df_with_data.count(), 1)

    def test08_get_table_name(self):
        test_name1 = self.sql_server.table_name('SqlTestTable1')
        self.assertIn('dbo.test1', test_name1)
        test_name2 = self.sql_server.table_name('SqlTestTable2')
        self.assertIn('dbo.test2', test_name2)

    def test09_execute_sql_file(self):
        file_name = 'test1'
        path_name = extras
        self.sql_server.execute_sql_file(resource_path=path_name, sql_file=file_name)
        self.assertTrue(True)

    def test10_read_w_id(self):
        self.sql_server.read_table('SqlTestTable1')
        self.sql_server.read_table('SqlTestTable2')
        self.assertTrue(True)

    def test11_write_w_id(self):
        df = self.create_data()
        self.sql_server.write_table(df, 'SqlTestTable1')
        df_with_data = self.sql_server.read_table('SqlTestTable1')
        self.assertEqual(df_with_data.count(), 1)

    def test12_truncate_w_id(self):
        self.sql_server.truncate_table('SqlTestTable1')
        df_without_data = self.sql_server.read_table('SqlTestTable1')
        self.assertEqual(df_without_data.count(), 0)

    def test13_drop_w_id(self):
        self.sql_server.drop_table('SqlTestTable1')
        table1_name = self.tc.table_name('SqlTestTable1')
        sql_argument = f"\n                (SELECT * FROM INFORMATION_SCHEMA.TABLES\n                WHERE TABLE_NAME = '{table1_name}') target\n                "
        table_exists = self.sql_server.load_sql(sql_argument)
        self.assertEqual(table_exists.count(), 0)

    def test14_can_drop_view_w_id(self):
        view_name = self.tc.table_name('SqlTestView')
        self.assertIn('viewtest1', view_name)
        table_from = self.tc.table_name('SqlTestTable2')
        self.create_test_view(view_name, table_from)
        self.assertTrue(True)
        self.sql_server.drop_view('SqlTestView')
        sql_argument = f"\n        (select\n                    *\n                    from\n                    INFORMATION_SCHEMA.VIEWS\n                    where\n                    table_name = '{view_name}') target\n        "
        table_exists = self.sql_server.load_sql(sql_argument)
        self.assertEqual(table_exists.count(), 0)

    def test15_can_drop_view_by_name(self):
        table_from = self.tc.table_name('SqlTestTable2')
        self.create_test_view(self.view_name, table_from)
        self.sql_server.drop_view_by_name(self.view_name)
        sql_argument = f"\n                (select\n                            *\n                            from\n                            INFORMATION_SCHEMA.VIEWS\n                            where\n                            table_name = '{self.view_name}') target\n                "
        table_exists = self.sql_server.load_sql(sql_argument)
        self.assertEqual(table_exists.count(), 0)

    def test16_upsert_to_table_none_input(self):
        val_return = self.sql_server.upsert_to_table_by_name(df_source=None, table_name=self.table_upsert_name, join_cols=['testid'], filter_join_cols=False)
        self.assertEqual(val_return, None)

    def test17_upsert_to_table(self):
        self.create_upsert_test_table()
        upsertTableSchema = StructType([StructField('testid', IntegerType(), True), StructField('testdata', StringType(), True)])
        df_preTest = DataframeCreator.make_partial(schema=upsertTableSchema, columns=['testid', 'testdata'], data=[(1, 'testdata1'), (2, 'testdata2')])
        self.sql_server.write_table_by_name(df_source=df_preTest, table_name=self.table_upsert_name, append=False)
        df_upsertTest = DataframeCreator.make_partial(schema=upsertTableSchema, columns=['testid', 'testdata'], data=[(2, 'newtestdata2'), (3, 'testdata3')])
        self.sql_server.upsert_to_table_by_name(df_source=df_upsertTest, table_name=self.table_upsert_name, join_cols=['testid'], filter_join_cols=False, overwrite_if_target_is_empty=False)
        df_afterUpsert = self.sql_server.read_table_by_name(self.table_upsert_name)
        expectedData = [(1, 'testdata1'), (2, 'newtestdata2'), (3, 'testdata3')]
        self.assertDataframeMatches(df=df_afterUpsert, expected_data=expectedData)

    def test18_upsert_to_table_with_join_cols_filter(self):
        upsertTableSchema = StructType([StructField('testid', IntegerType(), True), StructField('testdata', StringType(), True)])
        df_preTest = DataframeCreator.make_partial(schema=upsertTableSchema, columns=['testid', 'testdata'], data=[(1, 'testdata1'), (2, 'testdata2')])
        self.sql_server.write_table_by_name(df_source=df_preTest, table_name=self.table_upsert_name, append=False)
        df_upsertTest = DataframeCreator.make_partial(schema=upsertTableSchema, columns=['testid', 'testdata'], data=[(2, 'newtestdata2'), (3, 'testdata3'), (None, 'testdata4')])
        self.sql_server.upsert_to_table_by_name(df_source=df_upsertTest, table_name=self.table_upsert_name, join_cols=['testid'], filter_join_cols=True)
        df_afterUpsert = self.sql_server.read_table_by_name(self.table_upsert_name)
        expectedData = [(1, 'testdata1'), (2, 'newtestdata2'), (3, 'testdata3')]
        self.assertDataframeMatches(df=df_afterUpsert, expected_data=expectedData)

    def test19_upsert_to_table_overwrite_empty_target(self):
        upsertTableSchema = StructType([StructField('testid', IntegerType(), True), StructField('testdata', StringType(), True)])
        df_preTest = DataframeCreator.make_partial(schema=upsertTableSchema, columns=['testid', 'testdata'], data=[])
        self.sql_server.write_table_by_name(df_source=df_preTest, table_name=self.table_upsert_name, append=False)
        df_upsertTest = DataframeCreator.make_partial(schema=upsertTableSchema, columns=['testid', 'testdata'], data=[(2, 'newtestdata2'), (3, 'testdata3')])
        self.sql_server.upsert_to_table_by_name(df_source=df_upsertTest, table_name=self.table_upsert_name, join_cols=['testid'], overwrite_if_target_is_empty=True)
        df_afterUpsert = self.sql_server.read_table_by_name(self.table_upsert_name)
        expectedData = [(2, 'newtestdata2'), (3, 'testdata3')]
        self.assertDataframeMatches(df=df_afterUpsert, expected_data=expectedData)

    def create_test_table(self):
        sql_argument = f"\n            IF OBJECT_ID('{self.table_name}', 'U') IS NULL\n            BEGIN\n            CREATE TABLE {self.table_name}\n            (\n                testcolumn INT NULL\n            )\n            END\n        "
        self.sql_server.execute_sql(sql_argument)

    def insert_single_row(self):
        insert_data = 123
        sql_argument = f'\n            INSERT INTO {self.table_name} values ({insert_data})\n        '
        self.sql_server.execute_sql(sql_argument)

    def create_upsert_test_table(self):
        sql_argument = f"\n            IF OBJECT_ID('{self.table_upsert_name}', 'U') IS NULL\n            BEGIN\n            CREATE TABLE {self.table_upsert_name}\n            (\n                testid INT NULL,\n                testdata nvarchar(max) NULL\n            )\n            END\n        "
        self.sql_server.execute_sql(sql_argument)

    def create_data(self) -> DataFrame:
        schema = StructType([StructField('testcolumn', IntegerType(), True)])
        cols = ['testcolumn']
        df_new = DataframeCreator.make_partial(schema=schema, columns=cols, data=[(456,)])
        return df_new.orderBy('testcolumn')

    def create_test_view(self, view_name, select_from_table):
        sql_argument = f'\n            CREATE OR ALTER VIEW {view_name} as\n            (\n            select * from {select_from_table}\n            )\n        '
        self.sql_server.execute_sql(sql_argument)