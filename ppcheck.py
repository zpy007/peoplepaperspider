#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import re
import os
import requests
import urllib
import shutil
import time
from bs4 import BeautifulSoup

i=0
s=requests.session()
s.keep_alive=False
url_base='http://paper.people.com.cn/rmrb/html/'
sub_path=os.path.join('paper.people.com.cn','rmrb','html')
file_path=''
with open(os.path.join('.','count.txt'),'r') as f:
    for url_param in f.readlines():

        year_month_path=url_year_month=url_param.strip().split(' ')[0].split('-')[0]+'-'+url_param.strip().split(' ')[0].split('-')[1]
        day_path=url_day=url_param.strip().split(' ')[0].split('-')[2]
        url_that_day=url_year_month+'/'+url_day+'/'
        url_that_page=url_param.strip().split(' ')[1]
        dir_path=url_param.strip().split(' ')[0]

        #http://paper.people.com.cn/rmrb/html/2018-09/21
        article_url_base=url_base+url_that_day
        
        #http://paper.people.com.cn/rmrb/html/2018-09/21/nbs.D110000renmrb_02.htm
        url=url_base+url_that_day+url_that_page

        #2017-04-12\paper.people.com.cn\rmrb\html\2017-04\12
        file_path=os.path.join(dir_path,sub_path,year_month_path,day_path)

        if(os.path.exists(file_path)==False):
            os.makedirs(file_path)
        while True:
            try:
                content=s.get(url)
                content.encoding='utf-8'

                #nbs.D110000renmrb_02.htm
                content_soup=BeautifulSoup(content.text,'html.parser')

                break
            except (requests.exceptions.ConnectionError,requests.exceptions.ConnectTimeout) as e:
                print(str(e)+' 网络异常，尝试重连')
        
        artical_url_set=set()
        for linkurl in content_soup.findAll('a'):
            if re.match(r'nw\.D110000renmrb_\d{8}_\d{1,2}\-\d{2}\.htm',str(linkurl.get('href'))):
                artical_url_set.add(linkurl.get('href'))

        for article_url in artical_url_set:
            while True:
                try:
                    content=s.get(article_url_base+article_url)
                    content.encoding='utf-8'
                    #content_soup=BeautifulSoup(content.text,'html.parser')
                    break
                except (requests.exceptions.ConnectionError,requests.exceptions.ConnectTimeout) as e:
                    print(str(e)+' 网络异常，尝试重连')
            if(os.path.exists(os.path.join(file_path,article_url))==False):
                with open(os.path.join('.','writelog.txt'),'a') as f:
                    f.write('writting'+'\n')    
                with open(os.path.join(file_path,article_url),'w',encoding='utf-8') as f:
                    f.write(content.text)
        with open(os.path.join('.','writelog.txt'),'a') as f:
            f.write(dir_path+'\n')            
#print(str(i))
                    



        
    