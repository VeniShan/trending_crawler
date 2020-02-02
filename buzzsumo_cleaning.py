import sqlite3

conn = sqlite3.connect('trenddb.sqlite')
cur = conn.cursor()

cur.execute('''
SELECT id FROM Buzzsumo
''')
data_bid = cur.fetchall()

for i in range(len(data_bid)):
    cur.execute('''
    UPDATE Buzzsumo SET del = 1 WHERE id = ?
    ''', (data_bid[i][0],))

cur.execute('''
  SELECT
   min(Buzzsumo.id) id,
   Trends_group_2.group3_id,
   Buzzsumo.title,
   Buzzsumo.url
  FROM
   Buzzsumo JOIN Trends_group_2
  ON
  Buzzsumo.group2_id = Trends_group_2.id
  GROUP BY
   group3_id,
   title,
   url
  HAVING
   count(*) >= 1
''')

resultslst = cur.fetchall()

for results in resultslst:
    cur.execute('''
    SELECT Buzzsumo.id
    FROM
    Buzzsumo JOIN Trends_group_2
    ON
    Buzzsumo.group2_id = Trends_group_2.id
    WHERE Buzzsumo.id > ? AND Trends_group_2.group3_id = ? AND Buzzsumo.title = ? AND Buzzsumo.url = ?
    ''',(results[0], results[1], results[2], results[3]))

    delid = cur.fetchall()
    for i in range(len(delid)):
        cur.execute('''
        UPDATE Buzzsumo SET del = 0 WHERE id = ?
        ''', (delid[i]))
    print(results[0], "done")

print('done')

conn.commit()
