import pandas as pd
import sqlite3

def AsahiOutput():
    cur.execute('''
    SELECT
    Asahi.id,
    Asahi.title,
    Asahi.date,
    Asahi.pagename,
    Trends_group_2.id,
    Trends_group_2.name,
    Asahi.del
    FROM
    Asahi JOIN Trends_group_2
    WHERE
    Asahi.group2_id = Trends_group_2.id
    AND Asahi.del = 0
    ''')

    data = cur.fetchall()
    columns = ['Id','title','date','page','id2','trend','del']
    test=pd.DataFrame(columns=columns,data=data)
    test.to_csv('~/Documents/04.Codespace/trending_crawler/news_output/Asahi.csv', encoding="utf-8", index=False)

def YomiuriOutput():
    cur.execute('''
    SELECT
    Yomiuri.id,
    Yomiuri.title,
    Yomiuri.date,
    Yomiuri.pagename,
    Trends_group_2.id,
    Trends_group_2.name,
    Yomiuri.del
    FROM
    Yomiuri JOIN Trends_group_2
    WHERE
    Yomiuri.group2_id = Trends_group_2.id
    AND Yomiuri.del = 0
    ''')

    data = cur.fetchall()
    columns = ['Id','title','date','page','id2','trend','del']
    test=pd.DataFrame(columns=columns,data=data)
    test.to_csv('~/Documents/04.Codespace/trending_crawler/news_output/Yomiuri.csv', encoding="utf-8", index=False)

def NikkeiOutput():
    cur.execute('''
    SELECT
    Nikkei.id,
    Nikkei.title,
    Nikkei.date,
    Nikkei.pagename,
    Trends_group_2.id,
    Trends_group_2.name,
    Nikkei.del
    FROM
    Nikkei JOIN Trends_group_2
    WHERE
    Nikkei.group2_id = Trends_group_2.id
    AND Nikkei.del = 0
    ''')

    data = cur.fetchall()
    columns = ['Id','title','date','page','id2','trend','del']
    test=pd.DataFrame(columns=columns,data=data)
    test.to_csv('~/Documents/04.Codespace/trending_crawler/news_output/Nikkei.csv', encoding="utf-8", index=False)

def MainichiOutput():
    cur.execute('''
    SELECT
    Mainichi.id,
    Mainichi.title,
    Mainichi.date,
    Mainichi.pagename,
    Trends_group_2.id,
    Trends_group_2.name,
    Mainichi.del
    FROM
    Mainichi JOIN Trends_group_2
    WHERE
    Mainichi.group2_id = Trends_group_2.id
    AND Mainichi.del = 0
    ''')

    data = cur.fetchall()
    columns = ['Id','title','date','page','id2','trend','del']
    test=pd.DataFrame(columns=columns,data=data)
    test.to_csv('~/Documents/04.Codespace/trending_crawler/news_output/Mainichi.csv', encoding="utf-8", index=False)

def SankeiOutput():
    cur.execute('''
    SELECT
    Sankei.id,
    Sankei.title,
    Sankei.date,
    Sankei.pagename,
    Trends_group_2.id,
    Trends_group_2.name,
    Sankei.del
    FROM
    Sankei JOIN Trends_group_2
    WHERE
    Sankei.group2_id = Trends_group_2.id
    AND Sankei.del = 0
    ''')

    data = cur.fetchall()
    columns = ['Id','title','date','page','id2','trend','del']
    test=pd.DataFrame(columns=columns,data=data)
    test.to_csv('~/Documents/04.Codespace/trending_crawler/news_output/Sankei.csv', encoding="utf-8", index=False)

#========== main ==========
conn = sqlite3.connect('trenddb.sqlite')
cur = conn.cursor()

AsahiOutput()
YomiuriOutput()
MainichiOutput()
NikkeiOutput()
SankeiOutput()

conn.commit()
