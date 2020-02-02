import sqlite3

conn = sqlite3.connect('trenddb.sqlite')
cur = conn.cursor()

cur.execute('''
SELECT id, title
FROM
Buzzsumo
WHERE title = '結果なし'
''')

data = cur.fetchall()

for i in range(len(data)):
    cur.execute('''
    UPDATE Buzzsumo SET twitter_shares = 0
    WHERE id = ?''', (data[i][0],))

conn.commit()
