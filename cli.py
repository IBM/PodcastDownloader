import os
import sqlite3

db_filename = 'RSS.db'

db = not os.path.exists(db_filename)

conn = sqlite3.connect(db_filename)

if db:
    print 'Need to create database and schema.'
else:
    print 'Database already exists.'

conn.close()
