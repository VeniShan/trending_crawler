import pandas as pd
import sqlite3

conn = sqlite3.connect('trenddb.sqlite')
cur = conn.cursor()

cur.execute('''
SELECT group3_id FROM Trends_group_f
''')
data_tg3id = cur.fetchall()

for i in range(len(data_tg3id)):
    sns_value = 0
    cur.execute('''
    SELECT sns_value FROM Trends_group_2 WHERE group3_id = ?
    ''', (data_tg3id[i][0],))
    data_sv = cur.fetchall()
    for j in range(len(data_sv)):
        sns_value = sns_value + data_sv[j][0]
    cur.execute('''
    UPDATE Trends_group_f SET sns_value = ? WHERE group3_id = ?
    ''', (sns_value, data_tg3id[i][0]))

for i in range(len(data_tg3id)):
    txtcnt_1 = 0
    txtcnt_other = 0

    cur.execute('''
    SELECT page, txtcnt
    FROM
    Asahi JOIN Trends_group_2
    ON Asahi.group2_id = Trends_group_2.id
    WHERE group3_id = ? AND del = 0
    ''', (data_tg3id[i][0],))
    data_news = cur.fetchall()

    for aj in range(len(data_news)):
        if int(data_news[aj][0]) == 1:
            txtcnt_1 = txtcnt_1 + int(data_news[aj][1])
        else:
            txtcnt_other = txtcnt_other + int(data_news[aj][1])

    cur.execute('''
    SELECT page, txtcnt
    FROM
    Mainichi JOIN Trends_group_2
    ON Mainichi.group2_id = Trends_group_2.id
    WHERE group3_id = ? AND del = 0
    ''', (data_tg3id[i][0],))
    data_news = cur.fetchall()

    for mj in range(len(data_news)):
        txtcnt_m = data_news[mj][1]
        try:
            txtcnt_m = int(txtcnt_m.replace(',',''))
        except:
            pass
        if int(data_news[mj][0]) == 1:
            txtcnt_1 = txtcnt_1 + txtcnt_m
        else:
            txtcnt_other = txtcnt_other + txtcnt_m

    cur.execute('''
    SELECT page, txtcnt
    FROM
    Nikkei JOIN Trends_group_2
    ON Nikkei.group2_id = Trends_group_2.id
    WHERE group3_id = ? AND del = 0
    ''', (data_tg3id[i][0],))
    data_news = cur.fetchall()

    for nj in range(len(data_news)):
        if int(data_news[nj][0]) == 1:
            txtcnt_1 = txtcnt_1 + int(data_news[nj][1])
        else:
            txtcnt_other = txtcnt_other + int(data_news[nj][1])

    cur.execute('''
    SELECT pagename, txtcnt
    FROM
    Yomiuri JOIN Trends_group_2
    ON Yomiuri.group2_id = Trends_group_2.id
    WHERE group3_id = ? AND del = 0
    ''', (data_tg3id[i][0],))
    data_news = cur.fetchall()

    for yj in range(len(data_news)):
        if data_news[yj][0] == '一面' or data_news[yj][0] == '夕一面':
            txtcnt_1 = txtcnt_1 + int(data_news[yj][1])
        else:
            txtcnt_other = txtcnt_other + int(data_news[yj][1])

    cur.execute('''
    SELECT pagename, txtcnt
    FROM
    Sankei JOIN Trends_group_2
    ON Sankei.group2_id = Trends_group_2.id
    WHERE group3_id = ? AND del = 0
    ''', (data_tg3id[i][0],))
    data_news = cur.fetchall()

    for yj in range(len(data_news)):
        if data_news[yj][0] == '1ページ':
            txtcnt_1 = txtcnt_1 + int(data_news[yj][1])
        else:
            txtcnt_other = txtcnt_other + int(data_news[yj][1])

    cur.execute('''
    UPDATE Trends_group_f SET txtcnt_1 = ?, txtcnt_other = ?
    WHERE group3_id = ?
    ''',(txtcnt_1, txtcnt_other, data_tg3id[i][0]))

conn.commit()
