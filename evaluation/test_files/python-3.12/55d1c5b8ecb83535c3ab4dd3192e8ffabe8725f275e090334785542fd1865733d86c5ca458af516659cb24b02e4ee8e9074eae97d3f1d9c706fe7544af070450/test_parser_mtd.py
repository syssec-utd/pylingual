"""Test_sysbasetype module."""
import unittest
from pineboolib import application
from pineboolib.loader.main import init_testing, finish_testing

class TestMtdParserGeneral(unittest.TestCase):
    """TestMtdParserGeneral Class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic_1(self) -> None:
        """Test ORM parser."""
        from pineboolib.application.parsers.parser_mtd import pnmtdparser, pnormmodelsfactory
        import os
        for mtd_name in application.PROJECT.files.keys():
            if mtd_name.endswith('.mtd'):
                file_path = pnmtdparser.mtd_parse(mtd_name, application.PROJECT.files[mtd_name].path())
                if file_path:
                    self.assertTrue(os.path.exists(file_path))
                else:
                    self.assertTrue(False)
        pnormmodelsfactory.load_models()

    def test_basic_3(self) -> None:
        """Test create table."""
        from sqlalchemy import MetaData
        meta = MetaData()
        meta.create_all(application.PROJECT.conn_manager.mainConn().engine())

    def test_basic_4(self) -> None:
        """Test load model."""
        from pineboolib.qsa import qsa
        flmodules_orm = qsa.orm_('flmodules')
        self.assertTrue(flmodules_orm)

    def test_basic_5(self) -> None:
        """Test regexp."""
        from pineboolib.qsa import qsa
        test_orm = qsa.orm_('fltest5')
        self.assertTrue(test_orm)
        field = test_orm.table_metadata().field('version')
        self.assertTrue(field)
        self.assertEqual(field.regExpValidator(), '^(\\d{1,2}(,\\d{1,2})*)?$')

    @classmethod
    def tearDownClass(cls) -> None:
        """Ensure test clear all data."""
        finish_testing()