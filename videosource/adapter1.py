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
import math

basedomain = base64.b64decode("d3d3LmFnZW15cy5jb20=")
baseurl = "https://" + basedomain

#START DEFINE GLOBAL ACTION FUNCTION
WebCookie = {}
def initDefaultHeader(RefPath = "",IsXHR = False):
    header = {
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Alt-Used" : basedomain,
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language" : "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding" : "deflate",
        "Connection" : "keep-alive",
        "Referer" : baseurl+"/"+RefPath,
        "Sec-Fetch-Dest" : "document",
        "Sec-Fetch-Mode" : "navigate",
        "Sec-Fetch-Site" : "same-origin",
        "Cookie" : getCookieStr(),
        "Upgrade-Insecure-Requests" : "1"
    }
    if IsXHR :
        header["X-Requested-With"] = "XMLHttpRequest"
    return header

def setCookie(cookiename,value):
    WebCookie[cookiename]=value

def readCookie(res,cookiename):
    try:
        cw=res.headers["Set-Cookie"]
        sl=len(cookiename)+1
        dat=re.compile( cookiename + "=[^;]*;" ).search(cw).group()[sl:-1:]
        setCookie(cookiename,dat)
    except:
        pass

def getCookie(cookiename):
    try:
        return WebCookie[cookiename]
    except:
        return ""
    
def getCookies():
    return WebCookie;

def clearCookies():
    WebCookie.clear()

def delCookie(cookiename):
    del WebCookie[cookiename]

def getCookieStr():
    reqs = "rnd=123; ";
    for ix in WebCookie:
        t=ix
        v=WebCookie[t]
        reqs = reqs + t+"="+v+"; "
    return reqs

def printCookies():
    print(WebCookie)

#END DEFINE

#DEFINE WEBSITE PRIVATE FUNCTIONS

def setPCKs(t1):
    t1=int(t1)
    time_now = int(time.time()*1000)
    t1_tmp = int(math.floor(t1 / 1000 + 0.5)) >> 0x5
    k2 = (t1_tmp * (t1_tmp % 0x1000) * 0x3 + 0x1450f) * (t1_tmp % 0x1000) + t1_tmp
    t2 = time_now
    k2_s = str(k2)
    t2_s = str(t2)
    t2_s = t2_s[:-1:]+k2_s[-1]
    setCookie("t2",t2_s)
    setCookie("k2",k2_s)

def decodeUrl(url):
    return urllib.unquote(url)

def buildArg(year="all",season="all",pageid="1"):
    marg={
            "year":year, #年度：all，2022，2021...
            "season":season, #季度： all, 1,4,7,10
            "type":"all", #类别：all，TV，剧场版，OVA
            "Fcase":"all", #首字母： all，A，B，C
            "topic":"all", #主题：all，搞笑、运动...
            "disc":"all", #载体： all, BDRIP，ARIP
            "order":"time", #排序： time，name，点击量
            "pageid":pageid, #页码
            "area":"日本", #区域：all，日本，欧美，中国
            "status":"all", #状态：all，连载，完结，未播放
            }
    strs="%s-%s-%s-%s-%s-%s-%s-%s-%s-%s" % (
        marg["type"],
        marg["year"],
        marg["Fcase"],
        marg["topic"],
        marg["disc"],
        marg["order"],
        marg["pageid"],
        marg["area"],
        marg["season"],
        marg["status"]
    )
    return urllib.quote(strs)
#END DEFINE


#DEFINE GLOBAL URL GENERATOR

def downpage(url):
    header = initDefaultHeader()
    req = urllib2.Request(url, headers=header)
    res = urllib2.urlopen(req)
    readCookie(res,"t1")
    readCookie(res,"k1")
    t1=getCookie("t1")
    if not t1 == "":
        setPCKs(int(t1))
    return res.read()

def downsrc(vid,srcid,epid):
    url="%s/_getplay?aid=%s&playindex=%s&epindex=%s&r=%s" % (baseurl,vid,srcid,epid,str(random.random()))
    x=downpage("https://www.agemys.com/play/"+vid+"?playid="+srcid+"_"+epid)
    header = initDefaultHeader("",True)
    req = urllib2.Request(url, headers=header)
    res = urllib2.urlopen(req)
    readCookie(res,"t1")
    readCookie(res,"k1")
    printCookies()
    print(res.headers)
    ret=res.read()
    return ret


#END DEFINE

def isfirstpage(code):
    sign="<a class=\"pbutton pbutton_current asciifont\" href=\"javascript:void(0);\">首页</a>"
    try:
        string.index(code, sign)
        return True
    except ValueError:
        return False

def islastpage(code):
    sign="<a class=\"pbutton pbutton_current asciifont\" href=\"javascript:void(0);\">尾页</a>"
    try:
        string.index(code,sign)
        return True
    except ValueError:
        return False

def getlistitemarray(code):
    return re.findall("<div class=\"cell blockdiff\">(.*?)<div class=\"cell_imform\">",code,re.S)
    #re.findall("<li>\s*<a href=\"/view/(.*?)</li>",code, re.S)

def getlistitemdata(itemc):
    url=""
    title=""
    status=""
    pic=""
    try:
        vid=re.findall("<a href=\"/detail/(.*?)\"",itemc)[0]
        url="%s/play/%s" % (baseurl,vid)
        title=re.findall("<img.*alt=\"(.*?)\"",itemc)[0]
        status=re.findall("<span class=\"newname\">(.*?)</span>",itemc)[0]
        pic=re.findall("<img.*src=\"(.*?)\"",itemc)[0]
        if pic.startswith("//"):
            pic="https:"+pic
    except:
        pass
    return {'vid': vid, 'url':url,'title':title,'pic':pic,'status':status}

def getList(year,season,page):
    result={
            'PrevPage': False,
            'NextPage': False,
            'Data':[]
            }
    if year=='':
        year='all'
    if season=='':
        season='all'
    if page=='':
        page='1'
    arg=buildArg(year,season,page)
    urlx="%s/catalog/%s" % (baseurl,arg)
    code=downpage(urlx)
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
            tstr="/play/%s?playid=%s_1" % (avid,str(i))
            string.index(code, tstr)
            lnn=len(re.findall("/play/%s\?playid=%s_([\d]+)" % (avid,str(i)),code))
            season.append({'title': "播放源%s" % str(i), 'srcid': str(i), 'count': str(lnn)})
        except ValueError:
            pass
    return season

def getBangumVideoList(aurl,avid,srcid):
    code=downpage(aurl)
    playlist=[]
    regstr="<a href=\"/play/%s\?playid=%s_([\d]+)\".*title=\"([^\\\"]+)\"" % (avid,srcid)
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

def getPlayUrl(avid,srcid,epid):
    print("read url: avid : %s srcid: %s epid: %s" % (avid,srcid,epid))
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
    if k3=="html" or k3=="htm":
        curl=""
    return {'url':curl,'ext':k3}
 
