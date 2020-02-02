from urllib.request import urlopen
import sqlite3
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors for https
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('trenddb.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Trends;

CREATE TABLE Trends (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    date INTEGER,
    time INTEGER,
    rank INTEGER,
    name TEXT VARCHAR(128)
);
''')

date = int(input('Enter start:'))
dateed = int(input('Enter end:'))
url0 = 'https://twittrend.jp/time/1118370/'

while date <= dateed:
    url1 = url0 + str(date)
    try:
        urlopen(url1+'00/', context=ctx)
    except:
        date = date + 1
        continue
    time = 0

    while time < 24 :
        if time < 10:
            url2 = url1 + '0' + str(time) + '/'
        else:
            url2 = url1 + str(time) + '/'

        html = urlopen(url2, context=ctx).read()
        soup = BeautifulSoup(html, "html.parser")
        tags = soup('a')
        rank = 1

        for tag in tags:
            if not tag.get('target', None) == '_blank': continue
            try:
                if len(str(tag.contents[0])) > 20: continue
            except:
                continue

            trend = tag.contents[0]
            cur.execute('''INSERT INTO Trends
                (date, time, rank, name)
                VALUES ( ?, ?, ?, ?)''',
                (date, time, rank, trend))
            conn.commit()

            rank = rank + 1
        time = time + 1
    print(date,'done')
    date = date + 1
print('All done')
