import urllib.request, urllib.parse, urllib.error
import requests
import sqlite3
import json
import time
import datetime
from datetime import timedelta

#apikey = g3x2WJi6OTBwtBan82cr1OsyFtKTpTHT

#========== database ===========
def db_select():
    conn = sqlite3.connect('trenddb.sqlite')
    cur = conn.cursor()

    cur.execute('''SELECT id, name, date, group2_id
    FROM Trends_group WHERE date <= 20190820 AND id > 1682''')
    keywordlst = cur.fetchall()

    conn.commit()
    return keywordlst

def db_insert(data, keyword, page):
    conn = sqlite3.connect('trenddb.sqlite')
    cur = conn.cursor()

    try:
        if int(data['total_results']) == 0:
            cur.execute('''INSERT INTO Buzzsumo (title, group2_id) VALUES (?, ?)''', ('結果なし', keyword[3]))
            print(keyword[0], 'page:', page, 'done 0')
        else:
            for data_i in range(int(len(data['results']))):
                cur.execute('''
                INSERT INTO Buzzsumo
                (title, date, author_name, domain_name, subdomain, url, twitter_shares, num_words, group2_id)
                VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (data['results'][data_i]['title'], data['results'][data_i]['published_date'],
                data['results'][data_i]['author_name'], data['results'][data_i]['domain_name'],
                data['results'][data_i]['subdomain'], data['results'][data_i]['url'],
                data['results'][data_i]['twitter_shares'], data['results'][data_i]['num_words'], keyword[3]))
            print(keyword[0], 'page:', page, 'done')
    except:
        print(keyword[0], 'page:', page, 'error')

    conn.commit()
    #return NULL

def db_check():
    conn = sqlite3.connect('trenddb.sqlite')
    cur = conn.cursor()

    cur.executescript('''
    DROP TABLE IF EXISTS Buzzsumo;

    CREATE TABLE Buzzsumo (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        title TEXT VARCHAR(128),
        date INTEGER,
        author_name TEXT VARCHAR(128),
        domain_name TEXT VARCHAR(128),
        subdomain TEXT VARCHAR(128),
        url TEXT VARCHAR(128),
        twitter_shares INTEGER,
        num_words INTEGER,
        group2_id INTEGER
    );
    ''')
    conn.commit()

#========= requests ==========
def getdata(keyword, page):
    url = "https://api.buzzsumo.com/search/articles.json"
    querystring = {}
    keyword_q = ''
    result_type = 'twitter'
    date = 0
    dateed = 0
    date_range = 1
    api_key = "g3x2WJi6OTBwtBan82cr1OsyFtKTpTHT"
    language = 'ja'
    num_results = 100

    keyword_q = keyword[1].replace('#', '')
    date = keyword[2] - date_range
    if date == 20190800: date = 20190731
    dateed = keyword[2] + date_range
    #if dateed > 20190831 and dateed < 20190901:
    #    dateed = dateed + 69
    #if dateed > 20190930 and dateed < 20191001:
    #    dateed = dateed + 70
    date = unixtime(date)
    dateed = unixtime(dateed)

    querystring['q'] = keyword_q
    querystring['result_type'] = result_type
    querystring['begin_date'] = date
    querystring['end_date'] = dateed
    querystring['api_key'] = api_key
    querystring['language'] = language
    querystring['num_results'] = num_results
    querystring['page'] = page

    response = requests.request("GET", url, params=querystring)
    time.sleep(1.1)

    data = json.loads(response.text)
    return data

def unixtime(date):
    date = str(date)
    dtime = datetime.datetime.strptime(date[0:4] + '-' + date[4:6] + '-' + date[6:8] + ' 12:00:00', '%Y-%m-%d %H:%M:%S')
    unix_ts = int(time.mktime(dtime.timetuple()))
    return unix_ts

#========== main ==========
#db_check()
keywordlst = db_select()
for i in keywordlst:
    page = 0
    data_page = 1
    while page < data_page:
        data = getdata(i, page)
        db_insert(data, i, page)
        page = page + 1
        data_page = int(data['total_pages'])
