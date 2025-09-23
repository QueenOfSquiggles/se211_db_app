import sqlite3

class DbHandle:
    def __init__(self):
        self.db = sqlite3.connect("db")
        self.db.autocommit = True # not sanctioned by PEP 249 but IDGAF
        self.tables = self.db.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

    def execute_script(self, path):
        with open(path,"r", encoding="utf-8") as script:
            contents = script.read()
            cursor = self.db.cursor()
            try:
                out = cursor.executescript(contents)
                self._update_tables_list()
                return out
            except sqlite3.Error as oe:
                print("Caught a SQL error running script: ", path, "\n", oe)

    def execute(self, code):
        try:
            cursor = self.db.cursor()
            out = cursor.execute(code)
            self._update_tables_list()
            return out
        except sqlite3.Error as oe:
            print("Caught a SQL error running statement: ", code, "\n\n", oe)

    def _update_tables_list(self):
        self.tables = self.db.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

