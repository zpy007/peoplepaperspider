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

with open(os.path.join('.','count.txt'),'r') as f:
    for fdir in f.readlines():
        dir_path=fdir.strip().split(' ')[0]
        if(os.path.exists(os.path.join('.',dir_path,'paper.people.com.cn'))):
            shutil.rmtree(os.path.join('.',dir_path,'paper.people.com.cn'),ignore_errors=True)       
#print(str(i))
                    



        
    