from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
import sqlite3
import unicodedata
#import pandas as pd

#path = '/Users/Venitas/Documents/04.Codespace/trending_crawler/chromedriver'
#driver = webdriver.Chrome(path)

path = '/Users/Venitas/Documents/04.Codespace/trending_crawler/chromedriver'
waseda_username = "senkikai"
keypass = "Pm88422994Pm"

#========== browser ==========
def getpage(browser):
    #早稲田検索ページを開ける
    browser.get("http://waseda.summon.serialssolutions.com/jp/search?q=%E6%9C%9D%E6%97%A5%E6%96%B0%E8%81%9E&l=jp#!/search?ho=t&l=jp&q=%E6%9C%9D%E6%97%A5%E6%96%B0%E8%81%9E")
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
    time.sleep(2)
    browser.find_element_by_xpath('//*[@alt="ログイン（Login）へ"]').click()
    time.sleep(2)
    browser.switch_to_frame("Introduce")
    time.sleep(3)

    return browser

def search(browser,keyword):
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

    try:
        browser.find_element_by_xpath('//input[@value="クリア"]').click()
    except:
        try:
            time.sleep(2)
            browser.find_element_by_xpath('//input[@value="クリア"]').click()
        except:
            time.sleep(5)
            browser.find_element_by_xpath('//input[@value="クリア"]').click()
    browser.find_element_by_xpath('//input[@id="chkShishi2"]').click()
    browser.find_element_by_xpath('//input[@id="chkShishi3"]').click()
    browser.find_element_by_xpath('//input[@id="chkShishi4"]').click()
    browser.find_element_by_xpath('//input[@id="rdoSrchMode2"]').click() #詳細検索
    #browser.find_element_by_xpath('//input[@id="rdoSrchItem3"]').click() #見出しだけ検索

    browser.find_element_by_xpath('//input[@id="chkHochi2"]').click() #地方紙
    browser.find_element_by_xpath('//input[@id="chkIssueS2"]').click()
    browser.find_element_by_xpath('//input[@id="chkIssueS3"]').click()
    browser.find_element_by_xpath('//input[@id="chkIssueS4"]').click()
    browser.find_element_by_xpath('//input[@id="chkIssueS5"]').click()
    Select(browser.find_element_by_name("cmbDspNum")).select_by_value("100")
    #検索キーワードを入力する
    elem_inkw = browser.find_element_by_name("txtWord")
    elem_inkw.send_keys(keyword[1].replace('#',''))

    Select(browser.find_element_by_name("cmbIDFy")).select_by_value(date[:4])
    Select(browser.find_element_by_name("cmbIDFm")).select_by_value(date[4:6])
    Select(browser.find_element_by_name("cmbIDFd")).select_by_value(date[6:])
    Select(browser.find_element_by_name("cmbIDTy")).select_by_value(dateed[:4])
    Select(browser.find_element_by_name("cmbIDTm")).select_by_value(dateed[4:6])
    Select(browser.find_element_by_name("cmbIDTd")).select_by_value(dateed[6:])
    browser.find_element_by_xpath('//input[@value="検索実行"]').click()
    time.sleep(3)
    #ページの切り替え
    #w_start=1
    #w_news=browser.find_element_by_xpath('//*[@class="fontcolor001"]')
    #w_page=int(w_news.text)//100+1
    #while w_start<=w_page:
    #   newsdownload(browser,newsdata)
    #   w_start+=1

    #browser.close()
    return browser

def backpage(browser):
    try:
        browser.find_element_by_xpath('//img[@alt="検索画面へ戻る"]').click()
        time.sleep(3)
    except:
        try:
            time.sleep(2)
            browser.find_element_by_xpath('//img[@alt="検索画面へ戻る"]').click()
            time.sleep(3)
        except:
            time.sleep(5)
            browser.find_element_by_xpath('//img[@alt="検索画面へ戻る"]').click()
            time.sleep(3)

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

    tags = bs.find_all('td', class_ ="topic-list", align="center")
    for tag in tags:
        try:
            tags_date = tag('nobr')
            for tag_date in tags_date:
                datalst.append(tag_date.contents[0])
        except:
            pass
        if len(tag.contents) > 1: continue
        if len(tag('font')) > 0: continue
        if unicodedata.normalize('NFKC', tag.contents[0]) == ' ':continue
        if tag.contents[0].replace('\n', '').replace('\t', '').replace(u'\xa0', u' ') == ' ':continue
        datalst.append(tag.contents[0].replace('\n', '').replace('\t', '').replace(u'\xa0', u''))
    print(datalst)

    cnt = int(len(datalst)/7)
    #print(datalst)
    for i in range(cnt):
        date = int(str(datalst[ i * 7 + 1 ].replace( "年", "")
        + datalst[ i * 7 + 2]).replace( "月", "").replace( "日", ""))
        paper = datalst[ i * 7 + 3]
        pagename = datalst[ i * 7 + 4]
        page = int(datalst[ i * 7 + 5])
        txtcnt = int(datalst[ i * 7 + 6].replace("文字", ""))

        datelst.append(date)
        paperlst.append(paper)
        pagenamelst.append(pagename)
        pagelst.append(page)
        txtcntlst.append(txtcnt)

    tags_title = bs.find_all('span', class_ = "font001")
    for tag_title in tags_title:
        try:
            title = tag_title.a.contents[0].replace("\n", "")
            titlelst.append(title)
        except:
            title = tag_title.font.contents[0].replace("\n", "")
            titlelst.append(title)
    print(titlelst)
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
    DROP TABLE IF EXISTS Asahi;

    CREATE TABLE Asahi (
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
    FROM Trends_group WHERE date <= 20190820 AND id = 2034''')
    keywordlst = cur.fetchall()

    conn.commit()
    return keywordlst

def table_insert(dic, keyword):
    conn = sqlite3.connect('trenddb.sqlite')
    cur = conn.cursor()

    for i in range(dic['cnt']):
        cur.execute('''
        INSERT INTO Asahi
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
    browser = search(browser, keyword)
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
