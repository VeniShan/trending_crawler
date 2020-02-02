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
    browser.get("https://waseda-jp.libguides.com/az.php?q=産経新聞データベース")
    time.sleep(5)
    targetlink=browser.find_element_by_xpath('//*[@id="s-lg-az-content"]/div[1]/div[1]/a')
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
    time.sleep(8)
    browser.find_element_by_xpath('//*[@id="FreeSpace"]/div/div[2]/div/a').click()
    time.sleep(3)
    browser.switch_to_window(browser.window_handles[2])
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
    date_year = int(date[:4])
    date_month = int(date[4:6])
    date_date = int(date[6:8])
    if dateed > 20190831 and dateed < 20190901:
        dateed = str(dateed + 69)
    elif dateed > 20190930 and dateed < 20191001:
        dateed = str(dateed + 70)
    else:
        dateed = str(dateed)
    dateed_year = int(dateed[:4])
    dateed_month = int(dateed[4:6])
    dateed_date = int(dateed[6:8])

    #期間限定
    browser.find_element_by_xpath('//*[@id="search_duration"]/div[2]').click()
    time.sleep(1)

    browser.find_element_by_xpath('//*[@id="select_duration_layer"]/div[3]/div[1]').click()
    time.sleep(1)
    cld_date = browser.find_element_by_xpath('//*[@id="calendar_header"]/div').text
    cld_year = int(cld_date[:4])
    cld_month = int(re.findall('年(.+)月', cld_date)[0])
    while True:
        if cld_year == date_year:
            break
        browser.find_element_by_xpath('//*[@id="next_year"]').click()
        time.sleep(0.5)
        cld_date = browser.find_element_by_xpath('//*[@id="calendar_header"]/div').text
        cld_year = int(cld_date[:4])
    if cld_month < date_month:
        while True:
            if cld_month == date_month:
                break
            browser.find_element_by_xpath('//*[@id="next_month"]').click()
            time.sleep(0.5)
            cld_date = browser.find_element_by_xpath('//*[@id="calendar_header"]/div').text
            cld_month = int(re.findall('年(.+)月', cld_date)[0])
    else:
        while True:
            if cld_month == date_month:
                break
            browser.find_element_by_xpath('//*[@id="prev_month"]').click()
            time.sleep(0.5)
            cld_date = browser.find_element_by_xpath('//*[@id="calendar_header"]/div').text
            cld_month = int(re.findall('年(.+)月', cld_date)[0])

    cld_date = 0
    cld_i = 2
    cld_j = 1
    while cld_i <= 7:
        cld_j = 1
        while cld_j <= 7:
            cld_p = '//*[@id="calendar_table"]/div[' + str(cld_i) + ']/div[' + str(cld_j) + ']'
            cld_date = int(browser.find_element_by_xpath(cld_p).text)
            if cld_date == date_date:
                browser.find_element_by_xpath(cld_p).click()
                time.sleep(1)
            cld_j = cld_j + 1
        cld_i = cld_i + 1
    ActionChains(browser).move_by_offset(0, 0).click().perform()
    time.sleep(1)

    browser.find_element_by_xpath('//*[@id="select_duration_layer"]/div[3]/div[2]').click()
    time.sleep(1)
    cld_date = browser.find_element_by_xpath('//*[@id="calendar_header"]/div').text
    cld_year = int(cld_date[:4])
    cld_month = int(re.findall('年(.+)月', cld_date)[0])
    while True:
        if cld_year == dateed_year:
            break
        browser.find_element_by_xpath('//*[@id="next_year"]').click()
        time.sleep(0.5)
        cld_date = browser.find_element_by_xpath('//*[@id="calendar_header"]/div').text
        cld_year = int(cld_date[:4])
    if cld_month < dateed_month:
        while True:
            if cld_month == dateed_month:
                break
            browser.find_element_by_xpath('//*[@id="next_month"]').click()
            time.sleep(0.5)
            cld_date = browser.find_element_by_xpath('//*[@id="calendar_header"]/div').text
            cld_month = int(re.findall('年(.+)月', cld_date)[0])
    else:
        while True:
            if cld_month == dateed_month:
                break
            browser.find_element_by_xpath('//*[@id="prev_month"]').click()
            time.sleep(0.5)
            cld_date = browser.find_element_by_xpath('//*[@id="calendar_header"]/div').text
            cld_month = int(re.findall('年(.+)月', cld_date)[0])
    cld_date = 0
    cld_i = 2
    cld_j = 1
    while cld_i <= 7:
        cld_j = 1
        while cld_j <= 7:
            cld_p = '//*[@id="calendar_table"]/div[' + str(cld_i) + ']/div[' + str(cld_j) + ']'
            cld_date = int(browser.find_element_by_xpath(cld_p).text)
            if cld_date == dateed_date:
                browser.find_element_by_xpath(cld_p).click()
                time.sleep(1)
            cld_j = cld_j + 1
        cld_i = cld_i + 1
    ActionChains(browser).move_by_offset(0, 0).click().perform()
    time.sleep(1)

    ActionChains(browser).move_by_offset(0, 0).click().perform()
    time.sleep(1)

    #クリア
    elem_inkw = browser.find_element_by_xpath('//*[@id="search_field"]')
    elem_inkw.clear()
    #キーワード入力
    elem_inkw.send_keys(keyword[1].replace('#',''))
    #検索結果一覧表示
    time.sleep(3)
    browser.find_element_by_xpath('//*[@id="serach_icon"]').click()
    time.sleep(6)
    browser.find_element_by_xpath('//*[@id="open_all_articles"]').click()
    time.sleep(3)
    cnt = int(str(browser.find_element_by_xpath('//*[@id="search_conatiner_result_text"]').text.replace(' 件', '')))
    pagemax = int(cnt/10)
    if not cnt%10 == 0:
        pagemax = pagemax + 1
    time.sleep(1)

    return browser, pagemax

def changepage(browser):
    browser.find_element_by_xpath('//*[@id="pagenation"]/div[3]').click()
    time.sleep(5)
    browser.find_element_by_xpath('//*[@id="open_all_articles"]').click()
    time.sleep(3)
    return browser


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

    tags_title = bs.find_all('div', class_="article_list_title")
    for tag_i in range(int(len(tags_title)/2)):
        if tag_i%2 == 1:continue
        #print(re.findall('>(.+)<', str(tags_title[tag_i]))[0].replace(' ', '').replace('<bclass="search_words_highlight">', '').replace('</b>',''))
        try:
            titlelst.append(re.findall('>(.+)<', str(tags_title[tag_i]))[0].replace(' ', '').replace('<bclass="search_words_highlight">', '').replace('</b>',''))
        except:
            print("tags_title error")
        cnt = cnt + 1

    tags_info = bs.find_all('div', class_="article_info")
    for tag_i in range(int(len(tags_info)/2)):
        #print(re.findall('>(.+)<', str(tags_info[tag_i]))[0].replace(' ', ''))
        try:
            datalst.append(re.findall('>(.+)<', str(tags_info[tag_i]))[0].replace(' ', ''))
        except:
            print('tags_info error')

    tags_cnt = bs.find_all('div', class_="article_body_text")
    for tag_i in range(int(len(tags_cnt)/2)):
        try:
            txtcntlst.append(len(str(tags_cnt[tag_i]).replace(' ', '')) - 100)
        except:
            print('tags_cnt error')

    tags_pagename = bs.find_all('div', class_="article_list_title")
    tags_data = bs.find_all('td', width="1000")
    for tag in tags_data:
        try:
            datalst.append(tag.br.img.contents[0].replace('\t','').replace('\n',''))
        except:
            print("tags_data error")
    for i in range(len(datalst)):
        datelst.append(datalst[i][:10].replace('-',''))
        paperlst.append(datalst[i][11:15])
        pagenamelst.append(datalst[i][16:])

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
    DROP TABLE IF EXISTS Sankei;

    CREATE TABLE Sankei (
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
    SELECT
    Trends_group.date,
    Trends_group.name,
    Trends_group.group2_id,
    Trends_group.id
    FROM Trends_group JOIN Trends_group_2
    ON
    Trends_group.group2_id = Trends_group_2.id
    WHERE Trends_group.id < 3100 AND Trends_group_2.type > 0 AND Trends_group.id > 1083''')
    keywordlst = cur.fetchall()

    conn.commit()
    return keywordlst

def table_insert(dic, keyword):
    conn = sqlite3.connect('trenddb.sqlite')
    cur = conn.cursor()

    for i in range(dic['cnt']):
        cur.execute('''
        INSERT INTO Sankei
        (title, date, paper, pagename,txtcnt, group2_id)
        VALUES ( ?, ?, ?, ?, ?, ?)''',
        (dic['title'][i], dic['date'][i], dic['paper'][i], dic['pagename'][i], dic['txtcnt'][i], keyword[2]))

    conn.commit()

#========== main ==========
#table_check()
browser = webdriver.Chrome(path)
browser = getpage(browser)
keywordlst = table_select()
for keyword in keywordlst:
    browserpages = search(browser, keyword)
    browser = browserpages[0]
    pagemax = browserpages[1]
    page = 1
    while page <= pagemax:
        try:
            dic = newslistdl(browser)
        except:
            print(keyword[3], 'newslistdl error')
        #    browser = backpage(browser)
        #    continue
        try:
            table_insert(dic, keyword)
        except:
            print(keyword[3], 'table_insert error')
        print(keyword[3],page, 'done')
        page = page + 1
        browser = changepage(browser)
    print(keyword[3], 'done')
    #browser = backpage(browser)
