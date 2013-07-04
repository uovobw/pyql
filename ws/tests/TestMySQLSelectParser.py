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
        return MySQLSelectParser(query, position, self.fakeConfig)

    def test_parse(self):
        qSet = (
            ('select * from test', ['test']),
            ('select * col1, col2 from table1 where col1 = (select id from table2) group by col2 having sum(col2) > 10', ['table1', 'table2'])
        )
        for each in qSet:
            mySqlSelectParser = self._create_fake_parser_for_query(each[0], 4)
            assert (mySqlSelectParser.parse() == each[1])

