import sqlite3

class DBHelper:
    def __init__(self, dbname="willdo.sqlite"):
        self.dbname = dbname
        self.connection = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text)"
        itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)"
        ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
        self.connection.execute(tblstmt)
        self.connection.execute(itemidx)
        self.connection.execute(ownidx)
        self.connection.commit()

    def add_item(self, item_text, owner):
        stmt = "INSERT INTO items (description, owner) VALUES (?, ?)"
        args = (item_text, owner)
        self.connection.execute(stmt, args)
        self.connection.commit()

    def delete_item(self, item_text, owner):
        stmt = "DELETE FROM items WHERE description = (?) AND owner = (?)"
        args = (item_text, owner)
        self.connection.execute(stmt, args)
        self.connection.commit()

    def get_items(self, owner):
        stmt = "SELECT description FROM items WHERE owner = (?)"
        args = (owner,)
        return [x[0] for x in self.connection.execute(stmt, args)]