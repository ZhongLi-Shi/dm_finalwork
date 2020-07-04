#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import imp
imp.reload(sys)
#sys.setdefaultencoding('utf-8')

import time
import os
from os.path import exists
import json
import codecs
import gzip
import io

import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse

import re


def getComment(hotelnumber,Pgnum_max):
    comments = []

    for page in range(Pgnum_max):

        page=str(page)
        print("第"+page+"页")

        url="http://hotel.elong.com/ajax/detail/gethotelreviews/?hotelId="+hotelnumber+"&recommendedType=0&pageIndex="+page+"&mainTagId=0&subTagId=0&_=1468730838292"
        print(url)
        headers={

            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Connection':'keep-alive',
            'X-Requested-With':'XMLHttpRequest',
            #'Referer':'http://hotel.elong.com/guangzhou/32001005/',
            'Host':'hotel.elong.com'

        }


        #请求AJAX
        req=urllib.request.Request(url,None,headers)
        res=urllib.request.urlopen(req)
        data=res.read()
        res.close()

        #因为data有压缩所以要从内存中读出来解压
        data=io.StringIO(data)
        gz=gzip.GzipFile(fileobj=data)
        ungz=gz.read()
        # data = json.loads(ungz)
        # print data.get('contents')
        # #正则提取
        pattern_Comment=re.compile(r'"content"\W*')
        # pattern_Comment=re.compile(r'"content":"\W*"')

        for Comment in re.findall(pattern_Comment,ungz):
            if '感谢' in Comment or '谢谢' in Comment or '惠顾' in Comment:
                continue
            comments.append(Comment.replace('content','').replace('"','').replace(':',''))

    return comments



'''
程序入口
'''
def elongSpiderExcute(rawurl):
    hotelnumber = re.findall('\d+', rawurl)[0]

    Pgnum_max=5
    return getComment(hotelnumber,Pgnum_max)

# if __name__ == '__main__':
#     print elongSpiderExcute('http://hotel.elong.com/50101482/')