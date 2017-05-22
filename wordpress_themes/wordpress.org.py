#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re,os,time
import csv
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')  


urlList = "wordpress.org.txt"
csvfile = "wordpress.org.csv"

def getThemeUrl():
    baseurl = "https://wordpress.org/themes/"
    finname = "wordpress.org.txt"
    fin = open(finname,"a")
    for i in range(1,196):
        pageurl = baseurl + "browse/new/page/"+str(i)+"/"
        res = requests.get(pageurl)
        soupUrl = BeautifulSoup(res.content,"lxml")
        themes = soupUrl.select('a[rel="bookmark"]')
        #print themes
        for theme in themes:
            themeUrl =  str(theme).split(" ")[2].split('\"')[1]
            fin.write(themeUrl+"\n")
    fin.close()
        
        
def getContent(themeUrl):
    url = themeUrl
    #url = "https://wordpress.org/themes/venice-lite/"
    res = requests.get(url)
    soup = BeautifulSoup(res.content,"lxml")
    return soup

#download zipfile
def getZipfile(ss):
    for zipfile in ss.find_all("a",class_="button button-primary alignright"):
        #print type(zipfile)
        zipfile = str(zipfile).split(" ")[-1].split('\"')
        #print zipfile[1]
        zipname = zipfile[1].split("/")[-1]
        filename = "zipFolder/"+zipname
        src = requests.get(zipfile[1])
        with open(filename,"wb") as code:
            code.write(src.content)
        return zipname

#get other information
def getAuthor(ss):
    authors = ss.select('h4[class="theme-author"]')
    for author in authors:
	try:
            author_name = str(author.get_text()).split()[1]
        except IndexError:
	    author_name = " "
        for a in author.select('a'):
            author_url = str(a).split('\"')[1]
    return author_name,author_url

def getInstalls(ss):
    installs = ss.select('p[class="active_installs"]')
    for install in installs:
        n = str(install.get_text()).split(": ")[1]
        #print n
    return n

def main():
    if not os.path.exists(urlList):
        getThemeUrl()
        print "ThemeUrl has been listed."
    if not os.path.exists("zipFolder"):
        os.mkdir("zipFolder")
    fin = open(urlList,"r")
    csvff = file(csvfile,"a")
    writer = csv.writer(csvff)
    writer.writerow(['Url','ZipName','Author','Installs'])
    for url in fin:
        url = url.strip("\n")
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print now+": crawling "+url+" ...Please waite..."
        soup = getContent(url)
        zipname = getZipfile(soup)
        author = getAuthor(soup)
        installs = getInstalls(soup)
        data = [url,zipname,author,installs]
        writer.writerow(data)
    csvff.close()
    fin.close()

if __name__ == '__main__':
    main()
