#!/usr/bin/python
import os
import json
import ssl
import urllib.request
import bs4 as bs
from urllib.parse import urlparse
already_crawled = []
crawling  = []
class Domen:

    def zona(self,url):
        if url.find(".md") != -1 :
            return ".md"
        elif url.find(".com") != -1:
            return ".com"
        elif url.find(".net") != -1:
            return ".net"    
        elif url.find(".org") != -1:
            return ".org"
        elif url.find(".ru")  != -1:
            return ".ru"
        elif url.find(".ro")  != -1:
            return ".ro"
        elif url.find(".ua")  != -1:
            return ".ua"    
        elif url.find(".biz") != -1:
            return ".biz"
        elif url.find(".eu") != -1:
            return ".eu"
        elif url.find(".tv") != -1:
            return ".tv"              
        elif url.find(".info") != -1:
            return ".info"        
        else:
            return "NULL ZONA"          
    
    def host(self,url):
        o = urlparse(url)
        return o.hostname


def get_details(url):
    with urllib.request.urlopen(url) as u:
        s = u.read()
    soup = bs.BeautifulSoup(s,'lxml')
    title =soup.title.string
    desc =''
    keyword =''


    if soup.findAll(attrs={"name":"description"}):
        desc = soup.findAll(attrs={"name":"description"})
        desc = desc[0]['content']
    if soup.findAll(attrs={"name":"keywords"}):
        keyword = soup.findAll(attrs={"name":"keywords"})
        keyword = keyword[0]['content']   
    domen = Domen()
    return json.dumps({'Title':title.replace("\n", ""),'Description':desc.replace("\n", ""),'Keywords':keyword.replace("\n", ""),'Url':url.replace("\n", ""),'Host':domen.host(url),'Zona':domen.zona(url)})


def follow_links(url):
    global already_crawled
    global crawling 
    try:
    with urllib.request.urlopen(url) as u:
        s = u.read() 
    except urllib2.HTTPError, error:
    contents = error.read()    
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
                details = json.loads(get_details(l))
                print(details['Host'])


    crawling.pop()
    
    for site in crawling:
        follow_links(site)
        


follow_links('https://molddata.md/') 
