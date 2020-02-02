import sqlite3

conn = sqlite3.connect('trenddb.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Trends_group;

CREATE TABLE Trends_group (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    date INTEGER,
    name TEXT VARCHAR(128)
    group2_id INTEGER
);
''')

date = 20190801
dateed = 20190930
rank = 20

while date <= dateed:
    cur.execute('''SELECT name FROM Trends WHERE date = ? AND rank < ?''', (date, rank))
    rst = cur.fetchall()
    for i in rst:
        cur.execute('''SELECT * FROM Trends_group WHERE name = ? AND date = ?''',
        (i[0], date))
        if not cur.fetchone() == None: continue
        cur.execute('''INSERT INTO Trends_group(name, date)
        VALUES ( ?,? )''',( i[0], date))
    date = date + 1
conn.commit()
print('All done')
