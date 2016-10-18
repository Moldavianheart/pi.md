#!/usr/bin/python

import os
import socket
from urllib.parse import urlparse

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
		    							

domen = Domen()
