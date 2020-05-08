from interface.database.rdbms.mysql.scripts.Database import Database
from config.connection import Connection
from config.base import Base

db = Database(Connection.connections[Base.active_connection][0]['host'],
              Connection.connections[Base.active_connection][0]['user'],
              Connection.connections[Base.active_connection][0]['password'],
              Connection.connections[Base.active_connection][0]['database'])
db.open()
db.install()
