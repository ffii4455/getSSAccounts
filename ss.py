# -*- coding: utf-8 -*-
import os
import requests
import re
import json
from subprocess import Popen
import traceback
import base64

TOKEN_IDT = "/url/jiema/token/"
SS_INF_IDT = "ss:\/\/"

SS_URL = 'https://my.ishadowx.biz/'

def qrCodeDecodeOnline(url):
    #获取token
    r = requests.get("http://jiema.wwei.cn/url.html")
    data = r.text
    start = data.find(TOKEN_IDT) + len(TOKEN_IDT)
    end = data.find(".html", start)
    token = data[start:end]
    
    #在线解析二维码
    r = requests.post('http://jiema.wwei.cn/url/jiema/token/%s.html' % token, data={'jiema_url':url})
    data = r.text
    start = data.find(SS_INF_IDT) + len(SS_INF_IDT)
    end = data.find("\"", start)
    ssKey = data[start:end]
    return base64.b64decode(ssKey)

def main():
    URL = SS_URL

    file = open('gui-config.json', 'r')

    j = json.load(file)
    file.close()
    configs = j['configs']

    print('读取来自%s的SS服务器数据...' % URL, end='')
    
    headers={"User-Agent" : "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language" : "en-us",
    "Connection" : "keep-alive",
    "Accept-Charset" : "GB2312,utf-8;q=0.7,*;q=0.7"}
    r = requests.get(URL, headers=headers)
    r.encoding = 'utf-8'
    
    #print(r.text)

    data = re.findall('IP Address:.+?>(\S+)<.+?Port:.+?(\d+).+?Password:.+?>(\S+)', r.text, re.S)
    print('成功！\n')
    print(data)
    configs.clear()
    for i in range(len(data)):
        dict = {'server': 'a.jpip.pro', 'server_port': 443, 'password': '83969268', 'method': 'aes-256-gcm', 'remarks': '', 'auth': False, 'timeout': 5}
        e = data[i]  
        dict['server'] = e[0]
        dict['server_port'] = e[1]
        dict['password'] = e[2]
       # dict['method'] = e[3]
        configs.append(dict)

    file = open('gui-config.json', 'w')
    json.dump(j, file)
    file.close()
    os.chdir('./')
    print (os.getcwd())
    os.system('taskkill /F /IM shadowsocks.exe')    
    Popen('shadowsocks.exe')
    #os.system("pause")
    
try:  
    main()
except :
    print('请注意，程序发生了错误！！！')
    traceback.print_exc()
    os.system("pause")
