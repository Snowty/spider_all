#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re,os,time
import csv
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')  


urlList = "flexithemes.com.txt"
csvfile = "flexithemes.com.csv"

def getContent(themeUrl):
    url = themeUrl
    #url = "https://wordpress.org/themes/venice-lite/"
    res = requests.get(url)
    soup = BeautifulSoup(res.content,"lxml")
    return soup

def getThemeUrl():
    baseurl = "https://flexithemes.com/"
    finname = urlList
    fin = open(finname,"a")
    for i in range(1,3):
        pageurl = baseurl + "themes/page/"+str(i)+"/" 
        #print pageurl
        soupUrl = getContent(pageurl)
        themes = soupUrl.find_all("div",class_="theme-shot")
        #print themes
        for theme in themes:
            # print theme
            # print "------------------"
            themeUrl =  str(theme).split(" ")[3].split('\"')[1]
            fin.write(themeUrl+"\n")
    fin.close()
#getThemeUrl()        
        
#download zipfile
def getZipfile(ss):
    for zipfile in ss.find_all("div",class_="downloading"):
        #print zipfile
        zipfile = zipfile.select("iframe")
        for zipff in zipfile:
            zipfile = str(zipff).split(" ")[2].split('\"')[1]
        zipname = zipfile.split("/")[-1]
        filename = "zipFolder/"+zipname
        #print filename
        src = requests.get(zipfile)
        with open(filename,"wb") as code:
            code.write(src.content)
        return zipname

#getZipfile(soup)

def main():
    if not os.path.exists(urlList):
        getThemeUrl()
        print "ThemeUrl has been listed."
    if not os.path.exists("zipFolder"):
        os.mkdir("zipFolder")
    fin = open(urlList,"r")
    csvff = file(csvfile,"a")
    writer = csv.writer(csvff)
    writer.writerow(['Url','ZipName'])
    for url in fin:
        url = "https://flexithemes.com/download/?theme="+url.strip("\n").split("/")[3].split("-")[0]
        #print url
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print now+": crawling "+url+" ...Please waite..."
        soup = getContent(url)
        zipname = getZipfile(soup)
        data = [url,zipname]
        writer.writerow(data)
    csvff.close()
    fin.close()

if __name__ == '__main__':
    main()
