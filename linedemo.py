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


data = '2019.08.03東京夕刊1頁政治面（全261字）'
print(re.findall('頁(.+)（', data))
