
import requests
import os
import re
import time
from bs4 import BeautifulSoup
from datetime import date

from Engine.Database.utilities import *

#installation of firefox driver , need firefox to be installed to work properly

#link = https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
#wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz -O /tmp/geckodriver.tar.gz && tar -C /opt -xzf /tmp/geckodriver.tar.gz && chmod 755 /opt/geckodriver && ln -fs /opt/geckodriver /usr/bin/geckodriver && ln -fs /opt/geckodriver /usr/local/bin/geckodriver

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#pip3 install selenium

def OpenBrowser(module) :
    try:
        if module.url :
            browser = webdriver.Firefox()
            if module.cookies : browser.add_cookie(cookies)
            if browser.get(module.url) :
                if module.clicks : #clicks function
                    if "xpath" in clicks :
                        try: browser.find_element_by_xpath(module.clicks["xpath"]).click()
                        except: print("[browser] error click")
                if module.script : #execute additional js script
                    try: browser.execute_script(module.script)
                    except: print("[browser] error script")
                # Wait for 6 seconds for chargment
                scrollDown(browser, 6)
                html = browser.execute_script("return document.body.innerHTML;")
                browser.quit()
                module.html = html
                return html
    except:
        print("error while launching [browser]")

def scrollDown(browser, numberOfScrollDowns):
 body = browser.find_element_by_tag_name("body")
 while numberOfScrollDowns >=0:
  body.send_keys(Keys.PAGE_DOWN)
  numberOfScrollDowns -= 1
  time.sleep(1)
 return browser


class Module:
    def __init__(self, name, domain, url=""):
        self.name = name
        self.domain = domain
        self.url = url
        self.cookies = {} #dictionary
        self.data = {}
        self.clicks = {}
        self.script = None
        self.js_loading = True;
        self.html = None


    def setUrl(self, url):
        self.url = url

    def addCookie(self, key, value):
        self.cookies[key] = value

    def addData(self, key, value):
        self.data[key] = value

    def addClick(self, key, value):
        self.clicks[key] = value

    def setJSScript(self, jssript):
        self.script = jssript

    def isLoadedWithJS(self):
        self.js_loading = True

    def get_data(self, dictionary, data):
        if data and "tag" in dictionary:
            html = BeautifulSoup(str(html), features="lxml")
            data = html.find(dictionary["tag"])

        if data and "attr" in dictionary :
            html = BeautifulSoup(str(data), features="lxml")
            data = html.find(attrs=dictionary["attr"])

        if data and "inner-tag" in dictionary:
            html = BeautifulSoup(str(data), features="lxml")
            data = html.find(dictionary["inner-tag"])

        if data and "source" in dictionary : data = data.get(dictionary["source"])
        if data and "gettext" in dictionary : data = data.get_text().replace('\n','')
        if data and "before" in dictionary : data = dictionary["before"] + data
        if data and "after" in dictionary : data = data + dictionary["after"]
        return data
        """
        {"attr" : {"class":"thumb-unit"}} selection l'element avec l'attribut class=thumb-unit
        {"attr" : {"class":"lazy"}, "source": "src", "before": "https:"} selectionne le texte dans src et rajoute avant https
        {"attr": {"class":"sp-link"}, "source": "href"} selectionne le texte dans href
        {"tag": "img", "source": "title"} selection le tag img et prend ce qu'il y a dans title
        """

    def execute(self) :
        try:
            self.html = ""
            #if parsing the html code need to execute js
            if self.js_loading : self.html = OpenBrowser(self)
            #else we use a normal request
            else : self.html = requests.get(search_url, data=self.data, cookies=self.cookies).text

            if(self.html) : soup = BeautifulSoup(html, features="lxml")
            ## execution code with beautiful soup
        except : print("An error occurs while loading the page")
