from sqlalchemy import create_engine

class DbSchema(object):
	def __init__(self, db_user, db_password, db_host, db_port, db_name):
		self.db_user = db_user
		self.db_password = db_password
		self.db_host = db_host
		self.db_port = db_port
		self.db_name = db_name
		self.schema = {}

		dbConn = create_engine("mysql://%s:%s@%s:%s/%s" % ( self.db_user, self.db_password, self.db_host, self.db_port, self.db_name))
		tables = dbConn.execute("show tables")
		for table in tables:
			colNames = dbConn.execute("select column_name from information_schema.columns where table_schema = \'%s\' and table_name = \'%s\'" % (self.db_name, table[0]))
			for column in colNames:
				tableName = table[0]
				columnName = column[0]
				if tableName in self.schema:
					self.schema[tableName].append(columnName)
				else:
					self.schema[tableName] = [columnName]

	def getSchema(self):
		return self.schema

	def getTables(self):
		return self.schema.keys()

	def getColumns(self, table):
		try:
			return self.schema[table]
		except KeyError:
			raise ValueError("no table %s in schema" % table)

	def columnInTable(self, column, table):
		return (table in self.schema) and (column in self.schema[table])

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		out = []
		for k, v in self.schema.iteritems():
			out.append("%s: %s" % (k, ",".join(v)))
		return " ".join(out)


