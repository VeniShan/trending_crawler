from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
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
    browser.get("http://waseda.summon.serialssolutions.com/jp/search?q=毎日新聞=jp#!/search?ho=t&l=jp&q=毎日新聞")
    time.sleep(3)
    targetlink=browser.find_element_by_xpath('//*[@ng-bind="::item.bet.title"]')
    targetlink.click()
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
    time.sleep(3)
    browser.find_element_by_xpath('//*[@id="leftPane"]/div[1]/div[2]/div[3]/div[1]/h2/a').click()
    time.sleep(3)
    allHandles = browser.window_handles
    for handle in allHandles:
        if browser.title.find("マイサク") == -1:
            browser.switch_to_window(handle)
    time.sleep(3)

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

    browser.find_element_by_xpath('//*[@id="rightPane"]/form/div[2]/div[2]/a/img').click()
    #キーワード入力
    elem_inkw = browser.find_element_by_name("paraTi")
    elem_inkw.send_keys(keyword[1].replace('#',''))

    #ハイライトなし
    browser.find_element_by_xpath('//*[@id="rightPane"]/form/div[2]/div[1]/div[4]/input[2]').click()

    #期間限定
    Select(browser.find_element_by_name("paraYearFrom")).select_by_value(date[:4])
    Select(browser.find_element_by_name("paraMonthFrom")).select_by_value(str(int(date[4:6])))
    Select(browser.find_element_by_name("paraDayFrom")).select_by_value(str(int(date[6:])))
    Select(browser.find_element_by_name("paraFromTo")).select_by_value("1")
    Select(browser.find_element_by_name("paraYearTo")).select_by_value(dateed[:4])
    Select(browser.find_element_by_name("paraMonthTo")).select_by_value(str(int(dateed[4:6])))
    Select(browser.find_element_by_name("paraDayTo")).select_by_value(str(int(dateed[6:])))

    #東京朝刊＆東京夕刊限定
    browser.find_element_by_xpath('//*[@value="東京朝刊"]').click()
    browser.find_element_by_xpath('//*[@value="東京夕刊"]').click()

    time.sleep(1)
    browser.find_element_by_name("btn1Top").click()
    time.sleep(waittime)

    #検索結果一覧表示
    try:
        browser.find_element_by_xpath('//*[@name="paraSort" and @value="4"]').click()
        Select(browser.find_element_by_name("paraHyoujiKensuu")).select_by_value("200")
        w_news=browser.find_element_by_xpath('//*[@class="num"]').text
        browser.find_element_by_xpath('//*[@value="一覧表示"]').click()
    except:
        browser.find_element_by_xpath('//*[@id="rightPane"]/form/div[2]/input').click()
        flag = 0
    time.sleep(waittime)

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

    tags_title = bs.find_all('td', width="1000")
    for tag in tags_title:
        try:
            titlelst.append(tag.a.contents[0])
        except:
            titlelst.append(tag.img.contents[0].replace('\t','').replace('\n',''))
        cnt = cnt + 1

    tags_data = bs.find_all('td', width="1000")
    for tag in tags_data:
        try:
            datalst.append(tag.br.img.contents[0].replace('\t','').replace('\n',''))
        except:
            print("tags_data error")
    for i in range(len(datalst)):
        datelst.append(datalst[i][:10].replace('.',''))
        paperlst.append(datalst[i][10:14])
        pagelst.append(re.findall('刊(.+)頁', datalst[i])[0])
        pagenamelst.append(re.findall('頁(.+)（', datalst[i])[0])
        txtcntlst.append(re.findall('全(.+)字', datalst[i])[0])

    dic = {}
    dic['cnt'] = cnt
    dic['date'] = datelst
    dic['paper'] = paperlst
    dic['pagename'] = pagenamelst
    dic['page'] = pagelst
    dic['txtcnt'] = txtcntlst
    dic['title'] = titlelst
    return dic

#========== Database ==========
def table_check():
    conn = sqlite3.connect('trenddb.sqlite')
    cur = conn.cursor()

    cur.executescript('''
    DROP TABLE IF EXISTS Mainichi;

    CREATE TABLE Mainichi (
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
    id = 1101
    ''')
    keywordlst = cur.fetchall()

    conn.commit()
    return keywordlst

def table_insert(dic, keyword):
    conn = sqlite3.connect('trenddb.sqlite')
    cur = conn.cursor()

    for i in range(dic['cnt']):
        cur.execute('''
        INSERT INTO Mainichi
        (title, date, paper, pagename, page, txtcnt, group2_id)
        VALUES ( ?, ?, ?, ?, ?, ?, ?)''',
        (dic['title'][i], dic['date'][i], dic['paper'][i], dic['pagename'][i], dic['page'][i], dic['txtcnt'][i], keyword[2]))

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
        browser = backpage(browser)
        continue
    try:
        table_insert(dic, keyword)
    except:
        print(keyword[3], 'table_insert error')
        browser = backpage(browser)
        continue
    browser = backpage(browser)
    print(keyword[3], 'done')
