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


path = '/Users/Venitas/Documents/04.Codespace/trending_crawler/chromedriver'
waseda_username = "senkikai"
keypass = "Pm88422994Pm"
waittime = 3

#========== browser ==========
def getpage(browser):
    #早稲田検索ページを開ける
    browser.get("http://waseda.summon.serialssolutions.com/jp/search?q=読売新聞=jp#!/search?ho=t&l=jp&q=読売新聞")
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
    browser.get("https://database-yomiuri-co-jp.ez.wul.waseda.ac.jp/rekishikan/yomiuriNewsSearch.action")
    time.sleep(3)

    return browser

def search(browser,keyword):
    actions = ActionChains(browser)
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

    #検索キーワードを入力する
    elem_inkw = browser.find_elements_by_name("yomiuriNewsSearchDto.txtWordSearch")
    elem_inkw[1].send_keys(keyword[1].replace('#',''))

    browser.find_element_by_class_name("choiceArea1Open").click()
    browser.find_element_by_name("yomiuriNewsSearchDto.selSelectArea").click()
    browser.find_element_by_id("txtSYear").send_keys(date[:4])
    browser.find_element_by_id("txtSMonth").send_keys(date[4:6])
    browser.find_element_by_id("txtSDay").send_keys(date[6:])
    browser.find_element_by_id("txtEYear").send_keys(dateed[:4])
    browser.find_element_by_id("txtEMonth").send_keys(dateed[4:6])
    browser.find_element_by_id("txtEDay").send_keys(dateed[6:])
    time.sleep(1)
    browser.find_element_by_id("yomiuriNewsSubmitButton").click()
    time.sleep(waittime)

    return browser

def backpage(browser):
    try:
        browser.find_element_by_xpath('//*[@id="heiseiOperationRight"]/span[2]/input').click()
        time.sleep(waittime)
    except:
        time.sleep(waittime)
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
    txtcntlst = []
    cnt = 0

    tags_title = bs.find_all('td', class_ ="wp40")
    for tag in tags_title:
        title = ''
        try:
            for i in range(len(tag.a.contents)):
                try:
                    try:
                        title = title + tag.a.contents[i].replace('\n','').replace('\t','')
                    except:
                        title = title + tag.a.span.contents[0].replace('\n','').replace('\t','')
                        continue
                except:
                    pass
        except:
            for i in range(len(tag.contents)):
                try:
                    title = title + tag.contents[i].replace('\n','').replace('\t','')
                except:
                    title = title + tag.span.contents[0].replace('\n','').replace('\t','')
                print(title)
        titlelst.append(title)
        #print(title)
        cnt = cnt + 1

    tags_data = bs.find_all('td', style="text-align:center;")
    for tag in tags_data:
        try:
            datalst.append(tag.contents[0])
        except:
            print('tags_data error')
            continue

    for i in range(int(len(datalst) / 3)):
        datelst.append(datalst[i * 3].replace('.', ''))
        paperlst.append(datalst[i * 3 + 1])
        pagenamelst.append(datalst[i * 3 + 2])

    tags_txtcnt = bs.find_all("td", style="text-align:right;")
    datalst = []
    for tag in tags_txtcnt:
        try:
            datalst.append(tag.contents[0])
        except:
            print('tags_txtcnt error')
            continue
    for i in range(int(len(datalst) / 3)):
        txtcntlst.append(datalst[i * 3 + 1])

    dic = {}
    dic['cnt'] = cnt
    dic['date'] = datelst
    dic['paper'] = paperlst
    dic['pagename'] = pagenamelst
    dic['txtcnt'] = txtcntlst
    dic['title'] = titlelst
    return dic

#========== Database ==========
def table_check():
    conn = sqlite3.connect('trenddb.sqlite')
    cur = conn.cursor()

    cur.executescript('''
    DROP TABLE IF EXISTS Yomiuri;

    CREATE TABLE Yomiuri (
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
    FROM Trends_group WHERE date <= 20190820 AND id = 2615
    ''')
    keywordlst = cur.fetchall()

    conn.commit()
    return keywordlst

def table_insert(dic, keyword):
    conn = sqlite3.connect('trenddb.sqlite')
    cur = conn.cursor()

    for i in range(dic['cnt']):
        cur.execute('''
        INSERT INTO Yomiuri
        (title, date, paper, pagename, txtcnt, group2_id)
        VALUES ( ?, ?, ?, ?, ?, ?)''',
        (dic['title'][i], dic['date'][i], dic['paper'][i], dic['pagename'][i],  dic['txtcnt'][i], keyword[2]))

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
