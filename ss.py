# -*- coding: utf-8 -*-
import os
import requests
import re
import json
from subprocess import Popen
from tkinter import messagebox
import tkinter
import traceback
import base64

def qrCodeDecodeOnline(url):
    #此处的token还需根据网页上的token来修改
    r = requests.post('http://jiema.wwei.cn/url/jiema/token/225e628fa8ba8b8d9de95d773ac49527.html', data={'jiema_url':url})

    data = r.text
    start = data.find("ss:\/\/") + 7
    end = data.find("\"", start)
    ssKey = data[start:end]
    return base64.b64decode(ssKey)

def main():
    URL = "http://ss.ishadowx.com/"

    file = open('gui-config.json', 'r')

    j = json.load(file)
    file.close()
    configs = j['configs']

    print('读取来自%s的SS服务器数据...' % URL, end='')
    r = requests.get(URL)
    r.encoding = 'utf-8'

    data = re.findall('IP Address:.+?>(\S+)<.+?Port：(\d+)<.+?Password:.+?(\d+)<.+?Method:(\S+)<', r.text, re.S)
    print('成功！\n')
    configs.clear()
    for i in range(len(data)):
        dict = {'server': 'a.jpip.pro', 'server_port': 443, 'password': '83969268', 'method': ' \
        aes-256-cfb', 'remarks': '', 'auth': False, 'timeout': 5}
        e = data[i]  
        dict['server'] = e[0]
        dict['server_port'] = e[1]
        dict['password'] = e[2]
        dict['method'] = e[3]
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

