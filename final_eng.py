import sqlite3

conn = sqlite3.connect('trenddb.sqlite')
cur = conn.cursor()

cur.execute('''
SELECT id, group3_id FROM Trends_group_f
''')
id = cur.fetchall()

for i in id:
    sns_eng = 0
    cur.execute('''
    SELECT twitter_shares
    FROM Buzzsumo JOIN Trends_group_2
    ON Buzzsumo.group2_id = Trends_group_2.id
    WHERE Trends_group_2.group3_id = ?
    ''', (i[1],))
    data = cur.fetchall()
    for j in data:
        sns_eng = sns_eng + int(j[0])
    cur.execute('''
    UPDATE Trends_group_f SET sns_eng = ? WHERE id = ?
    ''',(sns_eng, i[0]))

conn.commit()
