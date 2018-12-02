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
startday=datetime.datetime(2017,1,1)
endday=datetime.datetime(2018,11,22)

def gen_dir_base(rightnow):
    return os.path.join(os.path.abspath('.'),rightnow.strftime('%Y-%m-%d'),'people.paper.com.cn','rmrb','html',rightnow.strftime('%Y-%m'),rightnow.strftime('%d'),'')
def write_file(save_path,content,write_type):
    ##print('保存位置：'+save_path)
    if(os.path.exists(save_path)==False):
        if(write_type=='wb'):
            with open(save_path,write_type) as f:
                f.write(content)
        else:
            with open(save_path,write_type,encoding='utf-8') as f:
                f.write(content)
def save_Page_From(content,type):
    #if type=='html':
    #    save_Html()
    #elif type=='img':
    #    save_Img()
    #elif type=='css':
    #    save_Css()
    #else:
    #    save_Js()
    pass
#def save_Html(save_path,content):
#    write_file(save_path,content,'w')
def save_Html(dir_base,base_url,url1,session):
    '''if os.path.exists(dir_base)==False:
        os.makedirs(dir_base)'''
    start_url=base_url+url1
    save_path=os.path.join(dir_base,url1)
    #请求页面
    while True:
        try:
            content=session.get(start_url)
            content.encoding='utf-8'
            content_soup=BeautifulSoup(content.text,'html.parser')
            break
        except (requests.exceptions.ConnectionError,requests.exceptions.ConnectTimeout) as e:
            print(str(e)+' 网络异常，尝试重连')
            #time.sleep(10)
    #保存页面
    '''if(os.path.exists(os.path.join(dir_base,url1))==False):
        write_file(save_path,content.text,'w')'''
    #print('网页：'+url1+' 保存完毕')
    return content_soup
def save_Article_Page(dir_base,base_url,content_soup,session):
    artical_url_set=set()
    for linkurl in content_soup.findAll('a'):
        if re.match(r'nw\.D110000renmrb_\d{8}_\d{1,2}\-\d{2}\.htm',str(linkurl.get('href'))):
            artical_url_set.add(linkurl.get('href'))
    for url in artical_url_set:
        content_soup=save_Html(dir_base,base_url,url,session)
        save_Img(dir_base,base_url,content_soup,session)
        save_Css(dir_base,base_url,content_soup,session)
        save_Js(dir_base,base_url,content_soup,session)
def save_Img(dir_base,base_url,content_soup,session):
    for img in set(content_soup.findAll('img')):
        if(os.path.exists(os.path.join(dir_base,urllib.request.url2pathname(img.get('src'))))==False):
            img_url=base_url+img.get('src')
            while True:
                try:
                    img_content=session.get(img_url)
                    break
                except (requests.exceptions.ConnectionError,requests.exceptions.ConnectTimeout) as e:
                    print(str(e)+' 网络异常，尝试重连')
                    #time.sleep(10)
            img_file_path=''
            for p in img.get('src').split('/')[:-1]:
                    img_file_path=img_file_path+p+'/'
            local_file_path=urllib.request.url2pathname(img_file_path)
            local_file_path=os.path.join(dir_base,local_file_path)
            if(os.path.exists(local_file_path)==False):
                os.makedirs(local_file_path)
            if(os.path.exists(os.path.join(dir_base,urllib.request.url2pathname(img.get('src'))))==False):
                write_file(os.path.join(dir_base,urllib.request.url2pathname(img.get('src'))),img_content.content,'wb')
            #print('图片：'+img.get('src')+' 保存完毕')
        #else:
            ##print('资源已存在')
def save_Css(dir_base,base_url,content_soup,session):
    for css in set(content_soup.findAll('link')):
        if(os.path.exists(os.path.join(dir_base,urllib.request.url2pathname(css.get('href'))))==False):
            css_url=base_url+css.get('href')
            while True:
                try:
                    css_content=session.get(css_url)
                    break
                except (requests.exceptions.ConnectionError,requests.exceptions.ConnectTimeout) as e:
                    print(str(e)+' 网络异常，尝试重连')
                    #time.sleep(10)
            css_file_path=''
            for p in css.get('href').split('/')[:-1]:
                    css_file_path=css_file_path+p+'/'
            local_file_path=urllib.request.url2pathname(css_file_path)
            local_file_path=os.path.join(dir_base,local_file_path)
            if(os.path.exists(local_file_path)==False):
                os.makedirs(local_file_path)
            if(os.path.exists(os.path.join(dir_base,urllib.request.url2pathname(css.get('href'))))==False):
                write_file(os.path.join(dir_base,urllib.request.url2pathname(css.get('href'))),css_content.text,'w')
            #print('css：'+css.get('href')+' 保存完毕')
        #else:
            ##print('资源已存在')
def save_Js(dir_base,base_url,content_soup,session):
    for js in set(content_soup.findAll('script')):
        if(js.get('src')!=None and js.get('src').split('/')[0]!='http:'):
            if(os.path.exists(os.path.join(dir_base,urllib.request.url2pathname(js.get('src'))))==False):
                js_url=base_url+js.get('src')
                while True:
                    try:
                        js_content=session.get(js_url)
                        break
                    except (requests.exceptions.ConnectionError,requests.exceptions.ConnectTimeout) as e:
                        print(str(e)+' 网络异常，尝试重连')
                        #time.sleep(10)
                js_file_path=''
                for p in js.get('src').split('/')[:-1]:
                        js_file_path=js_file_path+p+'/'
                local_file_path=urllib.request.url2pathname(js_file_path)
                local_file_path=os.path.join(dir_base,local_file_path)
                if(os.path.exists(local_file_path)==False):
                    os.makedirs(local_file_path)
                if(os.path.exists(os.path.join(dir_base,urllib.request.url2pathname(js.get('src'))))==False):
                    write_file(os.path.join(dir_base,urllib.request.url2pathname(js.get('src'))),js_content.text,'w')
                #print('js：'+js.get('src')+' 保存完毕')
            #else:
                ##print('资源已存在')
def count_Ten_More(dir_base,base_url,content_soup,s):
    count_set=set()
    for linkurl in content_soup.findAll('a'):
        if re.match(r'nw\.D110000renmrb_\d{8}_\d{1,2}\-\d{2}\.htm',str(linkurl.get('href'))):
            count_set.add(linkurl.get('href'))
    if len(count_set)>=10:
        return True
    else:
        return False
def runapp(start=startday,end=endday):
    rightnow=start
    rightnow_Year_Month=''
    rightnow_Day=''
    url0='http://paper.people.com.cn/rmrb/html'
    base_url=''
    url1='nbs.D110000renmrb_01.htm'
    dir_base=''
    start_url=''
    #content=''
    content_soup=''
    i=0
    while rightnow.strftime('%Y-%m-%d')<=end.strftime('%Y-%m-%d'):
        rightnow_Year_Month=rightnow.strftime('%Y-%m')
        rightnow_Day=rightnow.strftime('%d')
        dir_base=gen_dir_base(rightnow)
        base_url=url0+'/'+rightnow_Year_Month+'/'+rightnow_Day+'/'
        #先把文件夹创建了
        #if os.path.exists(dir_base)==False:
        #    os.makedirs(dir_base)
        ####################################################
        #
        #
        #拼接链接
        start_url=base_url+url1
        #请求页面
        #content=requests.get(start_url)
        #content.encoding='utf-8'
        #content_soup=BeautifulSoup(content.text,'html.parser')
        #保存页面
        #save_path=os.path.join(dir_base,url1)
        s=requests.session()
        s.keep_alive=False
        ##print(os.path.join(dir_base,url1))
        #if(os.path.exists(os.path.join(dir_base,url1))==False):  
        content_soup=save_Html(dir_base,base_url,url1,s)
        ##以下可以注释，调试
        '''save_Article_Page(dir_base,base_url,content_soup,s)
        save_Img(dir_base,base_url,content_soup,s)
        save_Css(dir_base,base_url,content_soup,s)
        save_Js(dir_base,base_url,content_soup,s)'''
        if(count_Ten_More(dir_base,base_url,content_soup,s)):
            with open(os.path.join('.','count.txt'),'a') as f:
                f.write(rightnow.strftime('%Y-%m-%d')+' '+url1+'\n')    
        ###########################################缓存完毕#########################################################################    
        for pageLink in content_soup.findAll('a'):
            if(pageLink.get('id')=='pageLink'):
                if(pageLink.get('href')!='./nbs.D110000renmrb_01.htm'):
                    ##print(os.path.join(dir_base,pageLink.get('href')))
                    #if(os.path.exists(os.path.join(dir_base,pageLink.get('href')))==False):
                    content_soup=save_Html(dir_base,base_url,pageLink.get('href'),s)
                    '''save_Article_Page(dir_base,base_url,content_soup,s)'''
                    if(count_Ten_More(dir_base,base_url,content_soup,s)):
                        with open(os.path.join('.','count.txt'),'a') as f:
                            f.write(rightnow.strftime('%Y-%m-%d')+' '+pageLink.get('href')+'\n')
        ####################################################
        ##print(os.path.join(os.path.abspath('.'),rightnow.strftime('%Y-%m-%d'),'Start.htm'))
        #shutil.copyfile(os.path.join(dir_base,url1),os.path.join(os.path.abspath('.'),rightnow.strftime('%Y-%m-%d'),'Start.htm'))
        rightnow=rightnow+datetime.timedelta(days=1)
        #i=i+1
        #break
    ##print(i)

runapp(start=datetime.datetime(2017,1,1),end=datetime.datetime(2018,12,1))
#定时运行
