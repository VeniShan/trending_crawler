import sqlite3

conn = sqlite3.connect('trenddb.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Trends_group_2;

CREATE TABLE Trends_group_2 (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT VARCHAR(128),
    Gerne TEXT VARCHAR(128),
    sns_value INTEGER,
    media_value INTEGER
);
''')

date = 20190801
dateed = 20190930

while date <= dateed:
    cur.execute('''SELECT name FROM Trends_group WHERE date = ?''', (date, ))
    rst = cur.fetchall()
    for i in rst:
        if date == 20190901:
            cur.execute('''SELECT group2_id FROM Trends_group WHERE name = ? AND date = ?''',
            (i[0], 20190831))
        else:
            cur.execute('''SELECT group2_id FROM Trends_group WHERE name = ? AND date = ?''',
            (i[0], date - 1))
#        if not cur.fetchone() == None:
        try:
            group2_id = int(cur.fetchone()[0])
            #print('--------------try',group2_id)
            cur.execute('''UPDATE Trends_group SET group2_id = ?
            WHERE name = ? AND date = ?''', (group2_id, i[0], date))

        except:
            cur.execute('''INSERT INTO Trends_group_2(name)
            VALUES ( ? )''',( i[0], ))
            cur.execute('''SELECT * FROM Trends_group_2 WHERE name = ? ORDER BY id DESC ''',
            (i[0],))
            group2_id = int(cur.fetchone()[0])
            cur.execute('''UPDATE Trends_group SET group2_id = ?
            WHERE name = ? AND date = ?''', (group2_id, i[0], date))
            #print('except',group2_id)
    date = date + 1

conn.commit()
print('All done')
