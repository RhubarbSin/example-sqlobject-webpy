from sqlobject import *

sqlhub.processConnection = connectionForURI('sqlite:mydatabase.db')

class User(SQLObject):

    class sqlmeta:

        table = 'users'

    name = StringCol()
    fullname = StringCol()
    password = StringCol()

if __name__ == "__main__":
    User.dropTable(ifExists=True)
    User.createTable()
