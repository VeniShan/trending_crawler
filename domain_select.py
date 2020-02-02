import pandas as pd
import sqlite3



def DomainSelect():
    cur.executescript('''
    DROP TABLE IF EXISTS Domain_2;

    CREATE TABLE Domain_2 (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name UNIQUE,
        type1 INTEGER,
        type2 INTEGER
    );
    ''')
    cur.execute('''
    SELECT subdomain
    FROM Buzzsumo JOIN Trends_group_2
    ON Buzzsumo.group2_id = Trends_group_2.id
    WHERE Trends_group_2.type > 0 AND Buzzsumo.news_select = 1
    ''')

    data = cur.fetchall()

    for i in range(len(data)):
        cur.execute('''
        INSERT OR IGNORE INTO Domain_2 (name ) VALUES (?)
        ''',(data[i]))

def DomainInput():
    data = pd.read_csv('~/Documents/04.Codespace/trending_crawler/news_input_f/Domain_2.csv')
    for i in range(len(data['id'])):
        cur.execute('''
        UPDATE Domain_2 SET type1 = ?, type2 = ?, author_name = ? WHERE id = ?
        ''',(int(data['type1'][i]), int(data['type2'][i]), data['author'][i],int(data['id'][i])))
        #print(i,'done')

def BuzzsumoCodeOutput():
    cur.execute('''
    SELECT Buzzsumo.id, Buzzsumo.title, Buzzsumo.subdomain, Domain_2.type1, Domain_2.type2, Buzzsumo.author_name, Domain_2.author_name, Buzzsumo.url, group2_id, Buzzsumo.news_select, Buzzsumo.del
    FROM Buzzsumo JOIN Domain_2
    ON Buzzsumo.subdomain = Domain_2.name
    WHERE Buzzsumo.news_select = 1 AND Buzzsumo.del = 1
    ''')

    data = cur.fetchall()
    columns = ['id','title','subdomain','type1','type2','author_name','author_name2','url','group2_id','news_select','del']
    test=pd.DataFrame(columns=columns,data=data)
    test.to_csv('~/Documents/04.Codespace/trending_crawler/news_output_f/Buzzsumocode.csv', encoding="utf-8", index=False)

def BuzzsumoCodeInput():
    cur.executescript('''
    DROP TABLE IF EXISTS Buzzsumo_2;

    CREATE TABLE Buzzsumo_2 (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        title TEXT VARCHAR(128),
        url TEXT VARCHAR(128),
        type_site INTEGER,
        type_author INTEGER,
        sns_eng,
        group2_id INTEGER,
        buzzsumo_id INTEGER
    );
    ''')
    data = pd.read_csv('~/Documents/04.Codespace/trending_crawler/news_input_f/Buzzsumocode.csv')




def DomainResults():
    cur.execute('''
    SELECT Buzzsumo.id, Buzzsumo.title, Trends_group_2.type, Domain_type.name, Buzzsumo.twitter_shares
    FROM
    ((Buzzsumo JOIN Trends_group_2 ON Buzzsumo.group2_id = Trends_group_2.id)
    JOIN Domain ON Buzzsumo.domain_name = Domain.name)
    JOIN Domain_type ON Domain.type1 = Domain_type.id
    WHERE Buzzsumo.news_select = 1
    ''')

    data = cur.fetchall()
    columns = ['id','title','type','domain_type','twitter_shares']
    test=pd.DataFrame(columns=columns,data=data)
    test.to_csv('~/Documents/04.Codespace/trending_crawler/final_output/domain_f.csv', encoding="utf-8", index=False)

#========== main ==========
conn = sqlite3.connect('trenddb.sqlite')
cur = conn.cursor()

#DomainSelect()
#DomainInput()
#BuzzsumoCodeOutput()
#DomainResults()

conn.commit()
