import sqlite3
import os
dir = os.path.dirname(__file__)

# Connecting to the database file
conn = sqlite3.connect(os.path.join(dir, 'puff_puff_db.sqlite'))
c = conn.cursor()

c.execute('CREATE TABLE Users (id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT NOT NULL, SortIndex INTEGER UNIQUE NOT NULL, IsCurrentlyPuffing INTEGER DEFAULT 0 NOT NULL, CountPaidEarly INTEGER DEFAULT 0 NOT NULL)')

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()