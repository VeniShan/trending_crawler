from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import sys
import time
import sqlite3
import unicodedata
import re

path = '/Users/Venitas/Documents/04.Codespace/trending_crawler/chromedriver'
waseda_username = "senkikai"
keypass = "Pm88422994Pm"
waittime = 3

#========== browser ==========
def getpage(browser):
    #早稲田検索ページを開ける
    browser.get("https://waseda-jp-libguides-com.ez.wul.waseda.ac.jp/az.php?q=LGaz47316627")
    time.sleep(3)
    #新しいページでログインする
    allHandles = browser.window_handles
    for handle in allHandles:
        if browser.title.find("EZproxy") == -1:
            browser.switch_to_window(handle)
    elem_user = browser.find_element_by_name("user")
    elem_user.send_keys(waseda_username)
    elem_pwd = browser.find_element_by_name("pass")
    elem_pwd.send_keys(keypass)
    browser.find_element_by_xpath('//*[@type="submit"]').click()
    time.sleep(5)
    targetlink=browser.find_element_by_xpath('//*[@id="s-lg-az-content"]/div/div[1]/a')
    targetlink.click()
    time.sleep(1)
    browser.switch_to_window(browser.window_handles[1])
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="nk-mainmenu"]/div/div[1]/div/ul/li[2]/p').click()
    time.sleep(1)

    return browser

def search(browser,keyword):
    flag = 1
    date_range1 = 2
    date_range2 = 5
    date = keyword[0] - date_range1
    dateed = keyword[0] + date_range2

    if date < 20190801:
        date = str(date - 69)
    elif date > 20190831 and date < 20190901:
        date = str(date - 69)
    else:
        date = str(date)
    if dateed > 20190831 and dateed < 20190901:
        dateed = str(dateed + 69)
    elif dateed > 20190930 and dateed < 20191001:
        dateed = str(dateed + 70)
    else:
        dateed = str(dateed)

    #クリア
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="nk-mainmenu"]/div/div[1]/div/ul/li[2]/ul/li[1]/p').click()
    time.sleep(2)

    #キーワード入力
    elem_inkw = browser.find_element_by_xpath('//*[@id="contentsPanel"]/div[2]/form/div[3]/div[1]/div[2]/div[1]/input')
    elem_inkw.send_keys(keyword[1].replace('#',''))

    #詳細を開く
    browser.find_element_by_xpath('//*[@id="contentsPanel"]/div[2]/form/div[8]/div[2]/div[2]/div[1]/div[2]/div[2]').click()
    #期間限定
    browser.find_element_by_xpath('//*[@id="contentsPanel"]/div[2]/form/div[8]/div[3]/div/div[1]/div[2]/div[6]/input').click()
    time.sleep(1)
    elem_indate = browser.find_element_by_xpath('//*[@id="contentsPanel"]/div[2]/form/div[8]/div[3]/div/div[1]/div[2]/div[6]/span/input[1]')
    elem_indate.clear()
    elem_indate.send_keys(date)
    elem_indate = browser.find_element_by_xpath('//*[@id="contentsPanel"]/div[2]/form/div[8]/div[3]/div/div[1]/div[2]/div[6]/span/input[2]')
    elem_indate.clear()
    elem_indate.send_keys(dateed)

    #東京朝刊＆東京夕刊限定
    browser.find_element_by_xpath('//*[@id="contentsPanel"]/div[2]/form/div[8]/div[4]/div[1]/div[1]/span[2]').click()
    browser.find_element_by_xpath('//*[@id="contentsPanel"]/div[2]/form/div[8]/div[4]/div[1]/div[1]/span[2]').click()
    browser.find_element_by_xpath('//*[@id="contentsPanel"]/div[2]/form/div[8]/div[4]/div[3]/div[1]/div[1]/div[2]/div/div[2]/div[1]/span[1]').click()
    browser.find_element_by_xpath('//*[@id="contentsPanel"]/div[2]/form/div[8]/div[4]/div[3]/div[1]/div[1]/div[2]/div/div[2]/div[2]/span[1]').click()

    time.sleep(1)
    #検索結果一覧表示
    browser.find_element_by_xpath('//*[@id="contentsPanel"]/div[2]/form/div[3]/button').click()
    time.sleep(3)
    browser.find_element_by_xpath('//*[@id="contentsPanel"]/div[2]/form/div[2]/button').click()
    time.sleep(2)
    try:
        browser.find_element_by_xpath('/html/body/div[10]/div[2]/div/div[2]/button[1]').click()
        time.sleep(waittime)
    except:
        flag = 0

    return [browser, flag]

def backpage(browser):
    try:
        browser.find_element_by_xpath('//*[@id="rightPane"]/div[2]/input').click()
        time.sleep(waittime)
    except:
        time.sleep(3)
        backpage(browser)

    return browser

#========= package =========
def newslistdl(browser):
    html = browser.page_source
    bs = BeautifulSoup(html, "html.parser")
    datalst = []
    titlelst = []
    datelst = []
    paperlst = []
    pagenamelst = []
    pagelst = []
    txtcntlst = []
    cnt = 0

    tags_title = bs.find_all('span', class_ = "nk-list-headline")
    for tag in tags_title:
        title = ''
        for i in range(len(tag.contents)):
            try:
                if 'span' in str(tag.contents[i]):
                    title = title + tag.span.contents[0]
                    continue
                title = title + tag.contents[i]
            except:
                print('tags_title error')
        titlelst.append(title)


    tags_data = bs.find_all('p', class_ = "nk-list-body-text")
    for tag in tags_data:
        try:
            data = tag.contents[0].replace('絵写表有', '').replace('PDF有', '').replace('/', '').replace('　', '')
            data = unicodedata.normalize('NFKC', data).replace(' ', '')
            datalst.append(data)
        except:
            print("tags_data error")
    for i in range(len(datalst)):
        datelst.append(datalst[i][:8])
        paperlst.append(re.findall('新聞(.+刊)', datalst[i])[0])
        pagelst.append(re.findall('刊(.+)ページ', datalst[i])[0])
        txtcntlst.append(re.findall('ページ(.+)文字', datalst[i])[0])
        cnt = cnt + 1

    dic = {}
    dic['cnt'] = cnt
    dic['date'] = datelst
    dic['paper'] = paperlst
    dic['page'] = pagelst
    dic['txtcnt'] = txtcntlst
    dic['title'] = titlelst
    return dic

#========== Database ==========
def table_check():
    conn = sqlite3.connect('trenddb.sqlite')
    cur = conn.cursor()

    cur.executescript('''
    DROP TABLE IF EXISTS Nikkei;

    CREATE TABLE Nikkei (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        title TEXT VARCHAR(128),
        date INTEGER,
        paper TEXT VARCHAR(128),
        pagename TEXT VARCHAR(128),
        page INTEGER,
        txtcnt INTEGER,
        group2_id INTEGER
    );
    ''')
    conn.commit()

def table_select():
    conn = sqlite3.connect('trenddb.sqlite')
    cur = conn.cursor()

    cur.execute('''
    SELECT date, name, group2_id, id
    FROM Trends_group WHERE date <= 20190820 AND
    id = 241
    OR id = 539
    OR id = 662
    OR id = 727
    OR id = 1404
    OR id = 1437
    OR id = 1778
    OR id = 2243
    OR id = 3055
    OR id = 3068
    ''')
    keywordlst = cur.fetchall()

    conn.commit()
    return keywordlst

def table_insert(dic, keyword):
    conn = sqlite3.connect('trenddb.sqlite')
    cur = conn.cursor()

    try:
        for i in range(dic['cnt']):
            cur.execute('''
            INSERT INTO Nikkei
            (title, date, paper, page, txtcnt, group2_id)
            VALUES ( ?, ?, ?, ?, ?, ?)''',
            (dic['title'][i], dic['date'][i], dic['paper'][i], dic['page'][i], dic['txtcnt'][i], keyword[2]))
    except:
        for i in range(dic['cnt']):
            cur.execute('''
            INSERT INTO Nikkei
            (title, date, paper, page, txtcnt, group2_id)
            VALUES ( ?, ?, ?, ?, ?, ?)''',
            (dic['title'][i+1], dic['date'][i], dic['paper'][i], dic['page'][i], dic['txtcnt'][i], keyword[2]))

    conn.commit()

#========== main ==========
#table_check()
browser = webdriver.Chrome(path)
browser = getpage(browser)
keywordlst = table_select()
for keyword in keywordlst:
    browserflag = search(browser, keyword)
    browser = browserflag[0]
    if browserflag[1] == 0:
        print(keyword[3], 'done 0')
        continue
    try:
        dic = newslistdl(browser)
    except:
        print(keyword[3], 'newslistdl error')
        continue
    try:
        table_insert(dic, keyword)
    except:
        print(keyword[3], 'table_insert error')
        continue
    print(keyword[3], 'done')
