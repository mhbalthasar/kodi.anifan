# -*- coding: utf-8 -*-

import json
import re
import sys
import urllib

import urllib2
import urlparse
import cookielib
import string
import random
import base64
import time
import os

baseurl = base64.b64decode("aHR0cHM6Ly93d3cucXVxaWRtLmNvbQ==")

def isfirstpage(code):
    sign=">上一页<"
    try:
        string.index(code, sign)
        return False
    except ValueError:
        return True

def islastpage(code):
    sign=">下一页<"
    try:
        string.index(code,sign)
        return False
    except ValueError:
        return True

def getlistitemarray(code):
    return re.findall("<li>\s*<a href=\"/view/(.*?)</li>",code, re.S)

def getlistitemdata(itemc):
    try:
        m1=re.findall("<a href=\"/view/([^.]+).html\" title=\"([^\"]+)",itemc)[0]
        url=baseurl+"/view/"+m1[0]+".html"
        vid=m1[0]
        title=m1[1]
    except:
        url=""
        title=""

    try:
        status=re.findall("<font color=\"red\">([^<]+)</font>",itemc)[0]
    except:
        status=""
    return {'vid': vid, 'url':url,'title':title,'status':status}

def downpage(url):

    header = {
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Alt-Used" : "www.quqidm.com",
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language" : "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding" : "deflate",
        "Connection" : "keep-alive",
        "Referer" : "https://www.quqidm.com/list/?region=%E6%97%A5%E6%9C%AC",
        "Sec-Fetch-Dest" : "document",
        "Sec-Fetch-Mode" : "navigate",
        "Sec-Fetch-Site" : "same-origin",
        "Upgrade-Insecure-Requests" : "1"
    }
    req = urllib2.Request(url, headers=header)
    res = urllib2.urlopen(req).read()

    #cookie.save(ignore_discard=True, ignore_expires=True)
    return res

def downsrc(vid,srcid,epid):
    url="%s/_getplay?aid=%s&playindex=%s&epindex=%s&r=%s" % (baseurl,vid,srcid,epid,str(random.random()))
    refurl="%s/vp/%s-%s-%s.html" % (baseurl,vid,srcid,epid)
    header = {
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Alt-Used" : "www.quqidm.com",
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language" : "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding" : "deflate",
        "Connection" : "keep-alive",
        "Referer" : refurl,
        "Sec-Fetch-Dest" : "document",
        "Sec-Fetch-Mode" : "navigate",
        "Sec-Fetch-Site" : "same-origin",
        "TE" : "trailers",
        "Upgrade-Insecure-Requests" : "1",
        "X-Requested-With" : "XMLHttpRequest"
    }
    #获取一个保存cookie的对象
    cj = cookielib.LWPCookieJar()
    #将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    #创建一个opener，将保存了cookie的http处理器，还有设置一个handler用于处理http的URL的打开
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    #将包含了cookie、http处理器、http的handler的资源和urllib2对象板顶在一起
    urllib2.install_opener(opener)
    ret=""
    i=5
    downpage(refurl) #this is to get cookie

     
    while i>0 and (ret=="err:timeout" or ret==""):
        try:
            req = urllib2.Request(url, headers=header)
            ret = urllib2.urlopen(req, timeout = 5).read()
            #cookie.save(ignore_discard=True, ignore_expires=True)
        except:
            pass
        i=i-1
    return ret


def getList(year,season,page):
    result={
            'PrevPage': False,
            'NextPage': False,
            'Data':[]
            }
    data="region=%E6%97%A5%E6%9C%AC&"
    if not (year==''):
        data="%syear=%s&" % (data,year)
    if not (season==''):
        data="%sseason=%s&" % (data,season)
    if page=='':
        page='0'
    data="%s&pagesize=24&pageindex=%s" % (data,page)
    code=downpage("%s/list/?%s" % (baseurl,data))
    result['PrevPage']=not isfirstpage(code)
    result['NextPage']=not islastpage(code)
    listi=getlistitemarray(code)
    for it in listi:
        result["Data"].append(getlistitemdata(it))
    return result

def getBangumPlayList(aurl,avid):
    code=downpage(aurl)
    season=[]
    for i in range(10):
        try:
            tstr="/vp/%s-%s-0.html" % (avid,str(i))
            string.index(code, tstr)
            lnn=len(re.findall("/vp/%s-%s-([\d]+).html" % (avid,str(i)),code))
            season.append({'title': "播放源%s" % str(i), 'srcid': str(i), 'count': str(lnn)})
        except ValueError:
            pass
    return season

def getBangumVideoList(aurl,avid,srcid):
    code=downpage(aurl)
    playlist=[]
    regstr="<a href=\"/vp/%s-%s-([\d]+).html\" title=\"([^\\\"]+)\"" % (avid,srcid)
    try:
        rpx=re.findall(regstr,code)
        for i in rpx:
            itm={'title' : i[1],
                  'vid': avid,
                  'srcid': srcid,
                  'epid': i[0]}
            playlist.append(itm)
    except ValueError:
            pass
    return playlist

def decodeUrl(panurl):
    hf_panurl = ""
    keyMP = 0x100000
    panurl_len = len(panurl)
    i=0
    while (i < panurl_len):
        ch="%s%s" % (panurl[i],panurl[i+1])
        mn=int(ch,16)
        mn = (mn + keyMP - (panurl_len / 0x2 - 0x1 -i / 0x2 )) % 0x100;
        hf_panurl = chr(mn) + hf_panurl
        i=i+0x2
    return(urllib.unquote(hf_panurl))

def getPlayUrl(avid,srcid,epid):
    cxurl=downsrc(avid,srcid,epid)
    if cxurl=="" or cxurl=="err:timeout":
        return ""
    obj=json.loads(cxurl)
    curl=decodeUrl(obj["vurl"])
    k1=curl.split("&")[0].split("?")[0]
    k2,k3=os.path.splitext(k1)
    if k3.startswith('.'):
        k3=k3[1:]
    if k3=="":
        k3="fdv"
    return {'url':curl,'ext':k3}
 
