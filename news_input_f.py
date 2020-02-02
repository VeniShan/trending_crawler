import pandas as pd
import sqlite3

def AsahiInput():
    data = pd.read_csv('~/Documents/04.Codespace/trending_crawler/news_input_f/Asahi.csv')
    i = 0
    while i < 601:
        if int(data['del'][i]) == 1:
            cur.execute('''
            UPDATE Asahi SET del = ? WHERE id = ?''',
            (int(data['del'][i]), int(data['Id'][i])))
        i = i + 1

def YomiuriInput():
    data = pd.read_csv('~/Documents/04.Codespace/trending_crawler/news_input_f/Yomiuri.csv')
    i = 0
    while i < 700:
        if int(data['del'][i]) == 1:
            cur.execute('''
            UPDATE Yomiuri SET del = ? WHERE id = ?''',
            (int(data['del'][i]), int(data['Id'][i])))
        i = i + 1

def MainichiInput():
    data = pd.read_csv('~/Documents/04.Codespace/trending_crawler/news_input_f/Mainichi.csv')
    i = 0
    while i < 649:
        if int(data['del'][i]) == 1:
            cur.execute('''
            UPDATE Mainichi SET del = ? WHERE id = ?''',
            (int(data['del'][i]), int(data['Id'][i])))
        i = i + 1

def NikkeiInput():
    data = pd.read_csv('~/Documents/04.Codespace/trending_crawler/news_input_f/Nikkei.csv')
    i = 0
    while i < 592:
        if int(data['del'][i]) == 1:
            cur.execute('''
            UPDATE Nikkei SET del = ? WHERE id = ?''',
            (int(data['del'][i]), int(data['Id'][i])))
        i = i + 1

def SankeiInput():
    data = pd.read_csv('~/Documents/04.Codespace/trending_crawler/news_input_f/Sankei.csv')
    i = 0
    while i < 571:
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
