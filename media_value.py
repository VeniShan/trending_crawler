import sqlite3

conn = sqlite3.connect('trenddb.sqlite')
cur = conn.cursor()

media_value = 0
top_value = 50
page = 0

cur.execute('''SELECT id FROM Trends_group_2''')
group2_idlst = cur.fetchall()
for i in group2_idlst:
    media_value = 0

    cur.execute('''SELECT page FROM Asahi
    WHERE group2_id = ? ''', (i[0], ))
    pagelst = cur.fetchall()
    for j in pagelst:
        media_value = media_value + (top_value - j[0])
    cur.execute('''UPDATE Trends_group_2
    SET media_value = ? WHERE id = ?''', (media_value * 5, i[0]))

conn.commit()
