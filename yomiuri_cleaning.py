import pandas as pd
import sqlite3

conn = sqlite3.connect('trenddb.sqlite')
cur = conn.cursor()

cur.execute('''
SELECT * FROM Yomiuri
''')
data_news = cur.fetchall()

for i in range(len(data_news)):
    cur.execute('''
    UPDATE Yomiuri SET del = 0 WHERE id = ?
    ''', (data_news[i][0],))

for i in range(len(data_news)):
    cur.execute('''
    SELECT * FROM Trends_group_f JOIN Trends_group_2
    ON Trends_group_f.group3_id = Trends_group_2.group3_id
    WHERE Trends_group_2.id = ?
    ''',(data_news[i][7],))
    if len(cur.fetchall()) == 0:
        cur.execute('''
        UPDATE Yomiuri SET del = 1 WHERE id = ?
        ''',(data_news[i][0],))

cur.execute('''
SELECT group3_id FROM Trends_group_f
''')
data_tg3id = cur.fetchall()

for i in range(len(data_tg3id)):
    cur.execute('''
    SELECT
    min(Yomiuri.id) id, Yomiuri.title, Yomiuri.date
    FROM Yomiuri JOIN Trends_group_2
    ON Yomiuri.group2_id = Trends_group_2.id
    WHERE group3_id = ?
    GROUP BY
    title, date
    HAVING
    count(*) > 1
    ''', (data_tg3id[i][0],))

    data_nid = cur.fetchall()
    for j in range(len(data_nid)):
        cur.execute('''
        UPDATE Yomiuri SET del = 1 WHERE id > ? AND title = ? AND date = ?
        ''', (data_nid[j][0], data_nid[j][1], data_nid[j][2]))

cur.execute('''
UPDATE Yomiuri SET del = 1 WHERE paper = '西部朝刊' or paper = '西部夕刊' or paper = '大阪朝刊' or paper = '大阪夕刊' or paper = '中部朝刊'
''')

conn.commit()
