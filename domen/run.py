#!/usr/bin/python
import os
import urllib.request
import bs4 as bs
from urllib.parse import urlparse
already_crawled = []
crawling  = []

def get_details(url):
    req = urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'})
    req.addheaders = [('User-agent', 'PiBot/0.1\n')]
    with urllib.request.urlopen(req) as u:
        s = u.read()
    soup = bs.BeautifulSoup(s,'lxml')
    title =soup.title.string
    desc = soup.findAll(attrs={"name":"description"})
    keyword = soup.findAll(attrs={"name":"keywords"})
    keyword = keyword[0]['content']

def follow_links(url):
    global already_crawled
    global crawling 
    req = urllib.request.Request(url)
    req.addheaders = [('User-agent', 'PiBot/0.1\n')]
    with urllib.request.urlopen(req) as u:
        s = u.read()
    soup = bs.BeautifulSoup(s,'lxml')
    body = soup.body
    for u  in body.find_all('a'):
        l = u.get('href')
        if l:
            if l[0:1] == '/' and l[0:2] != '//':
                l = "{}://{}{}".format(urlparse(url).scheme,urlparse(url).hostname,l)
            elif l[0:2] == '//':
                l="{}:{}".format(urlparse(url).scheme,l)
            elif l[0:2] == './':
                l=urlparse(url).scheme+"://"+urlparse(url).hostname+os.path.dirname(urlparse(url).path)+l[1]
            elif l[0:1] == '#': 
                l = urlparse(url).scheme+"://"+urlparse(url).hostname+urlparse(url).path+l
            elif l[0:3] == '../':
                l = "{}://{}/{}".format(urlparse(url).scheme,urlparse(url).hostname,l)
            elif l[0:11] == 'javascript:':
                continue
            elif l[0:4] == 'tel:':
                continue
            elif l[0:7] == 'mailto:':
                continue        
            elif l[0:5] != 'https' and l[0:4] != 'http':
                l = "{}://{}/{}".format(urlparse(url).scheme,urlparse(url).hostname,l)
            
            if l not in already_crawled:
            
                already_crawled.append(l)
                crawling.append(l)
                print(l)


    crawling.pop()
    
    for site in crawling:
        follow_links(site)
        

get_details('https://molddata.md/')    
