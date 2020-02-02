import pandas as pd
import sqlite3

conn = sqlite3.connect('trenddb.sqlite')
cur = conn.cursor()

cur.execute('''
SELECT * FROM Nikkei
''')
data_news = cur.fetchall()

for i in range(len(data_news)):
    cur.execute('''
    UPDATE Nikkei SET del = 0 WHERE id = ?
    ''', (data_news[i][0],))

for i in range(len(data_news)):
    cur.execute('''
    SELECT * FROM Trends_group_f JOIN Trends_group_2
    ON Trends_group_f.group3_id = Trends_group_2.group3_id
    WHERE Trends_group_2.id = ?
    ''',(data_news[i][7],))
    if len(cur.fetchall()) == 0:
        cur.execute('''
        UPDATE Nikkei SET del = 1 WHERE id = ?
        ''',(data_news[i][0],))

cur.execute('''
SELECT group3_id FROM Trends_group_f
''')
data_tg3id = cur.fetchall()

for i in range(len(data_tg3id)):
    cur.execute('''
    SELECT
    min(Nikkei.id) id, Nikkei.title, Nikkei.date
    FROM Nikkei JOIN Trends_group_2
    ON Nikkei.group2_id = Trends_group_2.id
    WHERE group3_id = ?
    GROUP BY
    title, date
    HAVING
    count(*) > 1
    ''', (data_tg3id[i][0],))

    data_nid = cur.fetchall()
    for j in range(len(data_nid)):
        cur.execute('''
        UPDATE Nikkei SET del = 1 WHERE id > ? AND title = ? AND date = ?
        ''', (data_nid[j][0], data_nid[j][1], data_nid[j][2]))

conn.commit()
