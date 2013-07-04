import unittest
from MySqlParser import MySQLSelectParser
import mock

class TestMySQLSelectParser(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.fakeConfig = {
            "DB_USER" : "test",
            "DB_PASSWORD" : "test",
            "DB_HOST" : "0.0.0.0",
            "DB_PORT" : "1234",
            "DB_NAME" : "test"
        }

    @mock.patch("DbSchema.DbSchema._read_schema", lambda x: None)
    def _create_fake_parser_for_query(self, query, position):
        to_return = MySQLSelectParser(query, position, self.fakeConfig)
        to_return.schema.schema = {"test" : ["a", "b"],
                                     "table1" : ["col1", "col2"],
                                     "table2" : ["id", "another"]
                                    }
        return to_return

    def test_parse(self):
        qSet = (
            ('select * from test', set(('test',))),
            ('select col1, col2 from table1 where col1 = (select id from table2) group by col2 having sum(col2) > 10', set(('table1', 'table2')))
        )
        for each in qSet:
            mySqlSelectParser = self._create_fake_parser_for_query(each[0], 4)
            assert (set(mySqlSelectParser.parse()) == each[1])

