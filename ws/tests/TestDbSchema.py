import unittest
from DbSchema import DbSchema
import mock

class TestDbSchema(unittest.TestCase):
    @classmethod
    @mock.patch.object(DbSchema,"_read_schema", new = lambda x: None)
    def setUpClass(self):
        self.dbschema = DbSchema("test", "test", "0.0.0.0", "1234", "test")
        self.tables = ["aTable", "bTable"]
        self.aCols = ["name", "addr", "value"]
        self.bCols = ["ref", "val"]
        self.fakeSchema = {"aTable" : self.aCols,
                          "bTable" : self.bCols}
        self.dbschema.schema = self.fakeSchema

    def test_getTables(self):
        for each in self.dbschema.getTables():
            self.assertTrue(each in self.tables)

    def test_getSchema(self):
        self.assertTrue(self.dbschema.getSchema() == self.fakeSchema)

    def test_getColumns(self):
        self.assertEquals(self.dbschema.getColumns("aTable"), self.aCols)
        self.assertEquals(self.dbschema.getColumns("bTable"), self.bCols)

    def test_columnInTable(self):
        self.assertTrue(self.dbschema.columnInTable("name", "aTable"))
        self.assertTrue(self.dbschema.columnInTable("addr", "aTable"))
        self.assertTrue(self.dbschema.columnInTable("value", "aTable"))
        self.assertFalse(self.dbschema.columnInTable("ref", "aTable"))
        self.assertFalse(self.dbschema.columnInTable("val", "aTable"))
        self.assertTrue(self.dbschema.columnInTable("ref", "bTable"))
        self.assertTrue(self.dbschema.columnInTable("val", "bTable"))

    def test_str(self):
        self.assertEqual("bTable: ref,val aTable: name,addr,value", str(self.dbschema))

