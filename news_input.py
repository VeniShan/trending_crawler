import pandas as pd
import sqlite3

def AsahiInput():
    data = pd.read_csv('~/Documents/04.Codespace/trending_crawler/news_input/Asahi.csv')
    i = 0
    while i < 960:
        if int(data['del'][i]) == 1:
            cur.execute('''
            UPDATE Asahi SET del = ? WHERE id = ?''',
            (int(data['del'][i]), int(data['Id'][i])))
        i = i + 1

def YomiuriInput():
    data = pd.read_csv('~/Documents/04.Codespace/trending_crawler/news_input/Yomiuri.csv')
    i = 0
    while i < 1160:
        if int(data['del'][i]) == 1:
            cur.execute('''
            UPDATE Yomiuri SET del = ? WHERE id = ?''',
            (int(data['del'][i]), int(data['Id'][i])))
        i = i + 1

def MainichiInput():
    data = pd.read_csv('~/Documents/04.Codespace/trending_crawler/news_input/Mainichi.csv')
    i = 0
    while i < 1024:
        if int(data['del'][i]) == 1:
            cur.execute('''
            UPDATE Mainichi SET del = ? WHERE id = ?''',
            (int(data['del'][i]), int(data['Id'][i])))
        i = i + 1

def NikkeiInput():
    data = pd.read_csv('~/Documents/04.Codespace/trending_crawler/news_input/Nikkei.csv')
    i = 0
    while i < 915:
        if int(data['del'][i]) == 1:
            cur.execute('''
            UPDATE Nikkei SET del = ? WHERE id = ?''',
            (int(data['del'][i]), int(data['Id'][i])))
        i = i + 1

def SankeiInput():
    data = pd.read_csv('~/Documents/04.Codespace/trending_crawler/news_input/Sankei.csv')
    i = 0
    while i < 707:
        if int(data['del'][i]) == 1:
            cur.execute('''
            UPDATE Sankei SET del = ? WHERE id = ?''',
            (int(data['del'][i]), int(data['Id'][i])))
        i = i + 1

#========== main ==========
conn = sqlite3.connect('trenddb.sqlite')
cur = conn.cursor()

AsahiInput()
YomiuriInput()
MainichiInput()
NikkeiInput()
SankeiInput()

conn.commit()
