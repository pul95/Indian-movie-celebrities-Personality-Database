# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 23:55:50 2020

@author: 91907
"""

#Program to get the list of twitter handle of bollywood celebrities
import requests 
from bs4 import BeautifulSoup
import re
URL = "http://www.socialsamosa.com/2014/05/indian-celebrities-twitter/"
r = requests.get(URL) 

soup = BeautifulSoup(r.content, 'html5lib') 
print(soup.prettify()) 

table = soup.find('div', attrs = {'class':'td-post-text-content'})

list_hashtag = []
for row in table.findAll('h2'):
    for a in row.findAll('a'):
        list_hashtag.append(a.text)
#list of names of celebrities        
list_names = []
for row in table.findAll('h2'):
    temp = row.text
    temp = re.sub(r'@\w*','',temp)
    temp = re.sub(r'–','',temp)
    temp = temp.replace(u'\xa0', u' ')
    temp = temp.replace(u'  ','')
    print(temp)
    list_names.append(temp)

