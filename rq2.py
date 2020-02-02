import pandas as pd
import sqlite3



def BuzzsumoCodeInput():
    cur.executescript('''
    DROP TABLE IF EXISTS Buzzsumo_2;

    CREATE TABLE Buzzsumo_2 (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        title TEXT VARCHAR(128),
        url TEXT VARCHAR(128),
        type_site INTEGER,
        type_author INTEGER,
        sns_eng INTEGER,
        group2_id INTEGER,
        buzzsumo_id INTEGER,
        type INTEGER
    );
    ''')
    data = pd.read_csv('~/Documents/04.Codespace/trending_crawler/news_input_f/Buzzsumocode.csv')

    for i in range(len(data['id'])):
        if int(data['del'][i]) == 0:continue
        if int(data['type2'][i]) != 99:
            cur.execute('''
            INSERT INTO Buzzsumo_2(title, url, type_site, type_author, group2_id, buzzsumo_id)
            VALUES(?, ?, ?, ?, ?, ?)''',
            (data['title'][i], data['url'][i], int(data['type1'][i]), int(data['type2'][i]), int(data['group2_id'][i]), int(data['id'][i])))

        if int(data['type2'][i]) == 99:
            if int(data['1'][i]) == 1:
                cur.execute('''
                INSERT INTO Buzzsumo_2(title, url, type_site, type_author, group2_id, buzzsumo_id)
                VALUES(?, ?, ?, ?, ?, ?)''',
                (data['title'][i]+'1', data['url'][i], int(data['type1'][i]), 1, int(data['group2_id'][i]), int(data['id'][i])))
            if int(data['2'][i]) == 1:
                cur.execute('''
                INSERT INTO Buzzsumo_2(title, url, type_site, type_author, group2_id, buzzsumo_id)
                VALUES(?, ?, ?, ?, ?, ?)''',
                (data['title'][i]+'2', data['url'][i], int(data['type1'][i]), 2, int(data['group2_id'][i]), int(data['id'][i])))
            if int(data['3'][i]) == 1:
                cur.execute('''
                INSERT INTO Buzzsumo_2(title, url, type_site, type_author, group2_id, buzzsumo_id)
                VALUES(?, ?, ?, ?, ?, ?)''',
                (data['title'][i]+'3', data['url'][i], int(data['type1'][i]), 3, int(data['group2_id'][i]), int(data['id'][i])))
            if int(data['5'][i]) == 1:
                cur.execute('''
                INSERT INTO Buzzsumo_2(title, url, type_site, type_author, group2_id, buzzsumo_id)
                VALUES(?, ?, ?, ?, ?, ?)''',
                (data['title'][i]+'5', data['url'][i], int(data['type1'][i]), 5, int(data['group2_id'][i]), int(data['id'][i])))
            if int(data['6'][i]) == 1:
                cur.execute('''
                INSERT INTO Buzzsumo_2(title, url, type_site, type_author, group2_id, buzzsumo_id)
                VALUES(?, ?, ?, ?, ?, ?)''',
                (data['title'][i]+'6', data['url'][i], int(data['type1'][i]), 6, int(data['group2_id'][i]), int(data['id'][i])))
            if int(data['7'][i]) == 1:
                cur.execute('''
                INSERT INTO Buzzsumo_2(title, url, type_site, type_author, group2_id, buzzsumo_id)
                VALUES(?, ?, ?, ?, ?, ?)''',
                (data['title'][i]+'7', data['url'][i], int(data['type1'][i]), 7, int(data['group2_id'][i]), int(data['id'][i])))
            if int(data['8'][i]) == 1:
                cur.execute('''
                INSERT INTO Buzzsumo_2(title, url, type_site, type_author, group2_id, buzzsumo_id)
                VALUES(?, ?, ?, ?, ?, ?)''',
                (data['title'][i]+'8', data['url'][i], int(data['type1'][i]), 8, int(data['group2_id'][i]), int(data['id'][i])))
            if int(data['11'][i]) == 1:
                cur.execute('''
                INSERT INTO Buzzsumo_2(title, url, type_site, type_author, group2_id, buzzsumo_id)
                VALUES(?, ?, ?, ?, ?, ?)''',
                (data['title'][i]+'11', data['url'][i], int(data['type1'][i]), 11, int(data['group2_id'][i]), int(data['id'][i])))
            if int(data['12'][i]) == 1:
                cur.execute('''
                INSERT INTO Buzzsumo_2(title, url, type_site, type_author, group2_id, buzzsumo_id)
                VALUES(?, ?, ?, ?, ?, ?)''',
                (data['title'][i]+'12', data['url'][i], int(data['type1'][i]), 12, int(data['group2_id'][i]), int(data['id'][i])))
            if int(data['13'][i]) == 1:
                cur.execute('''
                INSERT INTO Buzzsumo_2(title, url, type_site, type_author, group2_id, buzzsumo_id)
                VALUES(?, ?, ?, ?, ?, ?)''',
                (data['title'][i]+'13', data['url'][i], int(data['type1'][i]), 13, int(data['group2_id'][i]), int(data['id'][i])))


def SnsEng():
    cur.execute('''
    SELECT id, buzzsumo_id FROM Buzzsumo_2
    ''')
    datalst = cur.fetchall()
    for data in datalst:
        cur.execute('''
        SELECT id FROM Buzzsumo_2 WHERE buzzsumo_id = ?
        ''',(data[1],))
        idlst = cur.fetchall()
        cnt = len(idlst)

        cur.execute('''
        SELECT twitter_shares FROM Buzzsumo WHERE id = ?
        ''',(data[1],))
        sns_eng = cur.fetchall()

        for id in idlst:
            cur.execute('''
            UPDATE Buzzsumo_2 SET sns_eng = ? WHERE id = ?
            ''',(int(sns_eng[0][0]/cnt), id[0]))

    cur.execute('''
    SELECT id, group2_id FROM Buzzsumo_2
    ''')
    idlst = cur.fetchall()
    for id in idlst:
        cur.execute('''
        SELECT type FROM Trends_group_2 WHERE id = ?
        ''',(id[1],))
        type = cur.fetchall()[0][0]
        cur.execute('''
        UPDATE Buzzsumo_2 SET type = ? WHERE id = ?
        ''',(type, id[0]))

#------------------------------------
conn = sqlite3.connect('trenddb.sqlite')
cur = conn.cursor()

BuzzsumoCodeInput()
SnsEng()

conn.commit()
