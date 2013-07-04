# System Imports
import nltk
import sys

# Local Imports
from DbSchema import DbSchema
#from MySqlParser import MySqlParser

class MySQLParser(object):
    def __init__(self, query, position, config):
        """
            Input:
                query:      str
                position:   int
        """
        self.tables = None
        self.columns = None
        self.query = query
        self.position = position
        self.config = config
        self.index_char = query[position]
        self.query_tokens = nltk.word_tokenize(query)
        self.schema = DbSchema(self.config['DB_USER'], self.config['DB_PASSWORD'], self.config['DB_HOST'],
                    self.config['DB_PORT'], self.config['DB_NAME'])

    def getColumns(self):
        return self.columns

    def getTables(self):
        return self.tables


class MySQLSelectParser(MySQLParser):
    def __init__(self, query, position, config):
        super(MySQLSelectParser, self).__init__(query, position, config)

    def parse(self):
        curr_word, prev_word = self.search_precendent_words()
        self.tables = self.search_tables_names()
        self.columns = self.search_column_names()

    def search_tables_names(self):
        return [x for x in self.schema.getTables() if x in self.query_tokens]

    def search_column_names(self):
        cols = set()
        for table in self.schema.getTables():
            for col in self.schema.getColumns(table):
                cols.add(col)
        return [x for x in cols if x in self.query_tokens]

    def search_precendent_words(self):
        if not self.index_char:
            sys.exit(1)

        char = self.index_char
        position = self.position
        counter = 0
        prev_word_list = []
        while True:
            char = self.query[position]
            if char == ' ':
                counter += 1
            if counter == 2:
                break
            prev_word_list.insert(0, char)
            position -= 1

        tmp_word = ''.join(prev_word_list).split(' ')
        curr_word = ''
        prev_word = ''
        if tmp_word:
            curr_word = tmp_word[1]
            prev_word = tmp_word[0]

        return curr_word, prev_word

'''
qq = """
    select colonna1, colonna2 from prelievi_pf
    where colonna1 = (select id from righe_prelievi_pf)
    group by colonna2
    having sum( colonna2 ) > 10
"""

#for i in xrange(128):
i = 56
config = {
    'DB_USER': 'changeme',
    'DB_PASSWORD': 'changeme',
    'DB_HOST': 'localhost',
    'DB_PORT': '3306',
    'DB_NAME': 'changeme'
}
parse = MySQLSelectParser(qq, i, config)
print parse.parse()
'''
