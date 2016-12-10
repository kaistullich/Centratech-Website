import sqlite3
sqlite_file = 'Centratech.sqlite'

conn = sqlite3.connect(sqlite_file)
cursor = conn.cursor()