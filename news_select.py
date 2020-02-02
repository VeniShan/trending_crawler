import sqlite3

conn = sqlite3.connect('trenddb.sqlite')
cur = conn.cursor()


cur.execute('''
SELECT * FROM Buzzsumo
''')
id_b = cur.fetchall()

for i_b in id_b:
    cur.execute('''
    UPDATE Buzzsumo SET news_select = 0 WHERE id = ?
    ''',(i_b[0],))

cur.execute('''
SELECT id, group3_id, sns_eng FROM Trends_group_f
''')
id = cur.fetchall()

for i in id:
    sns_eng = 0
    cur.execute('''
    SELECT Buzzsumo.id, twitter_shares
    FROM Buzzsumo JOIN Trends_group_2
    ON Buzzsumo.group2_id = Trends_group_2.id
    WHERE Trends_group_2.group3_id = ?
    ORDER BY twitter_shares DESC
    ''', (i[1],))
    data = cur.fetchall()
    for j in data:
        #if sns_eng/i[2] > 0.95:
        if int(j[1]) < 100:
            break
        cur.execute('''
        UPDATE Buzzsumo SET news_select = 1 WHERE id = ?
        ''',(j[0],))
        sns_eng = sns_eng + int(j[1])

conn.commit()
