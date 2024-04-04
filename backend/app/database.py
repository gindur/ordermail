import sqlite3
from flask import g

# Database helper functions
def __get_db():
    """Open a new database connection if there is none yet for the current application context."""
    if 'db' not in g:
        g.db = sqlite3.connect("db.sqlite")
        g.db.row_factory = __dict_factory
        
    return g.db

def __dict_factory(cursor, row):
    """Converts rows from a query to a dictionary."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
        
    return d

def cursor(include_database = False):
    """Return a cursor for the database connection."""
    db = __get_db()
    return (db, db.cursor()) if include_database else db.cursor()



