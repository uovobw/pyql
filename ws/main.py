# System imports
from flask import Flask
from flask.ext.basicauth import BasicAuth

#local imports
from DbSchema import DbSchema
from MySqlWords import MySqlWords

app = Flask(__name__)
app.debug = True

app.config.update(
    DB_HOST = "127.0.0.1",
    DB_USER = "root",
    DB_PASSWORD = "hackme",
    DB_NAME = "employees",
    DB_PORT = "3306"
)

app.config['BASIC_AUTH_USERNAME'] = 'user'
app.config['BASIC_AUTH_PASSWORD'] = 'password'

basic_auth = BasicAuth(app)

@app.route('/')
@basic_auth.required
def root():
    return 'ANO'

@app.route("/columns/<t>")
@basic_auth.required
def get_column(t):
    return ",".join(app.config['SCHEMA'].getColumns(t))

if __name__ == '__main__':
    schema = DbSchema(app.config['DB_USER'],
                      app.config['DB_PASSWORD'],
                      app.config['DB_HOST'],
                      app.config['DB_PORT'],
                      app.config['DB_NAME']
                      )
    app.config['SCHEMA'] = schema
    app.run()

