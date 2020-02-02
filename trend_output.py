import pandas as pd
import sqlite3

conn = sqlite3.connect('trenddb.sqlite')
cur = conn.cursor()

cur.execute('''
SELECT
Trends_group_2.id,
Trends_group_2.name,
Buzzsumo.title,
Buzzsumo.twitter_shares,
Buzzsumo.url
FROM
    Trends_group_2
        JOIN
    Buzzsumo ON Trends_group_2.id = Buzzsumo.group2_id
WHERE
    (Buzzsumo.group2_id , Buzzsumo.twitter_shares) IN
    (   SELECT
            group2_id, MAX(twitter_shares)
        FROM
            Buzzsumo
        GROUP BY group2_id
    )
ORDER BY Trends_group_2.id
''')
data = cur.fetchall()
columns = ['Id','Trends','Web_News_Title','Twitter_shares','URL']

test=pd.DataFrame(columns=columns,data=data)

test.to_csv('~/Documents/04.Codespace/trending_crawler/test.csv', encoding="utf-8", index=False)

conn.commit()
