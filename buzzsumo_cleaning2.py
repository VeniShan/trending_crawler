import pandas as pd
import sqlite3

conn = sqlite3.connect('trenddb.sqlite')
cur = conn.cursor()

cur.execute('''
SELECT id FROM Buzzsumo
''')
data_bid = cur.fetchall()

for i in range(len(data_bid)):
    cur.execute('''
    UPDATE Buzzsumo SET del = 1 WHERE id = ?
    ''', (data_bid[i][0],))
