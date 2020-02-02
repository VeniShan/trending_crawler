import pandas as pd
import sqlite3

conn = sqlite3.connect('trenddb.sqlite')
cur = conn.cursor()
cur.executescript('''
DROP TABLE IF EXISTS Trends_group_f;

CREATE TABLE Trends_group_f (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	TEXT VARCHAR(128),
	"sns_value"	INTEGER,
	"sns_eng" INTEGER,
	"txtcnt_1"	INTEGER,
	"txtcnt_other"	INTEGER,
	"type"	INTEGER,
	"group3_id" INTEGER
);
''')

data = pd.read_csv('~/Documents/04.Codespace/trending_crawler/news_input_f/trend_group.csv')
i = 0
while i < 3128:
    if int(data['group'][i]) == 0:
        cur.execute('''
        UPDATE Trends_group_2 SET type = ? , group3_id = ? WHERE id = ?''',
        (int(data['type'][i]), int(data['Id'][i]), int(data['Id'][i])))
    else:
        cur.execute('''
        UPDATE Trends_group_2 SET type = ? , group3_id = ? WHERE id = ?''',
        (int(data['type'][i]), int(data['group'][i]), int(data['Id'][i])))
    #print(int(data['group'][i]))
    i = i + 1

cur.execute('''
SELECT * FROM Trends_group_2 WHERE id <= 2725 ORDER BY group3_id
''')
data_tg2 = cur.fetchall()
for i in range(len(data_tg2)):
    if data_tg2[i][4] == 0:continue
    cur.execute('''
    SELECT * FROM Trends_group_f WHERE group3_id = ?
    ''', (data_tg2[i][5],))
    data_tgf = cur.fetchall()
    if len(data_tgf) > 0:
        cur.execute('''
        UPDATE Trends_group_f SET name = ? WHERE group3_id = ?
        ''', (data_tgf[0][1] + ' or ' + data_tg2[i][1], data_tg2[i][5]))
        continue
    cur.execute('''
    INSERT INTO Trends_group_f
    (name, type, group3_id)
    VALUES (?, ?, ?)
    ''',(data_tg2[i][1], data_tg2[i][4],data_tg2[i][5]))

conn.commit()
