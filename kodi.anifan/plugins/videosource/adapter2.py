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

sys.path.append("%s/../pkgs" % os.path.split(os.path.realpath(__file__))[0])
import pyaeshelper as aeshelper

basedomain = base64.b64decode("b21vZnVuLnR2")
baseurl = "https://" + basedomain

playdomain = base64.b64decode("cGxheS5vbW9mdW4udHY=")
playurl = "https://" + playdomain

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

def decodeUrl(url):
    return urllib.unquote(url)

def buildArg(year="all",pageid="1"):
    if year=="all":
        strs="/vod/show/id/20/page/"+pageid+".html"
    else:
        strs="/vod/show/id/20/page/"+pageid+".html"
        strs="/vod/show/id/20/page/"+pageid+"/year/"+year+".html"
    return urllib.quote(strs)

def decodeKey(vstr,bttoken):
    print(vstr)
    print(bttoken)
    TKS="B89C9D4AEA78D9F5"
    try:
        aes = aeshelper.PYAESCipher(TKS,bttoken)
        aes_text = aes.decrypt(vstr)
        if aes_text.startswith("http"):
            return aes_text
        else:
            return ""
    except:
        return ""

#END DEFINE


#DEFINE GLOBAL URL GENERATOR

def downpage(url):
    header = initDefaultHeader()
    req = urllib2.Request(url, headers=header)
    res = urllib2.urlopen(req)
    return res.read()

def downsrc(purl):
    url="%s/m3u8.php?url=%s" % (playurl,purl)
    header = initDefaultHeader()
    header["Alt-Used"]=playdomain
    header["Sec-Fetch-Dest"]="iframe"
    header["Sec-Fetch-Site"]="same-site"
    req = urllib2.Request(url, headers=header)
    res = urllib2.urlopen(req)
    return res.read()

#END DEFINE
def IsStrContains(substr,strs):
    try:
        string.index(strs, substr)
        return True
    except ValueError:
        return False

def isfirstpage(code):
    sign="<span class=\"page-number page-current display\">1</span>"
    try:
        string.index(code, sign)
        return True
    except ValueError:
        return False

def islastpage(code):
    try:
      tailpage=re.findall("<a href=\"/index.php/vod/show/id/20/page/([\d]+).*>尾页</a>",code)[0]
    except:
        return False
    sign="<span class=\"page-number page-current display\">"+tailpage+"</span>"
    try:
        string.index(code,sign)
        return True
    except ValueError:
        return False

def getlistitemarray(code):
    arr=code.split('<div class="module-item">')
    return arr[1:]
    #return re.findall("<div class=\"cell blockdiff[2]*\">(.*?)<div class=\"cell_imform\">",code,re.S)
    #re.findall("<li>\s*<a href=\"/view/(.*?)</li>",code, re.S)

def getlistitemdata(itemc):
    url=""
    title=""
    status=""
    pic=""
    try:
        status=re.findall("<div class=\"module-item-text\">(.*?)</div>",itemc)[0]
        itemc=itemc.split("<div class=\"module-item-text\">"+status+"</div>")[0]
        vcc=re.findall("<a href=\"/index.php/vod/detail/id/(\d+).html\" title=\"(.*?)\">(.*?)</a>",itemc)[0]
        vid=vcc[0]
        url="%s/index.php/vod/detail/id/%s.html" % (baseurl,vid)
        title=vcc[1]
        pic=re.findall("<img class=\"lazy lazyloaded\" data-src=\"(.*?)\"",itemc)[0]
        if pic.startswith("//"):
            pic="https:"+pic
    except:
        pass
    return {'vid': vid, 'url':url,'title':title,'pic':pic,'status':status}

def getList(year,page):
    result={
            'PrevPage': False,
            'NextPage': False,
            'Data':[]
            }
    if year=='':
        year='all'
    if page=='':
        page='1'
    arg=buildArg(year,page)
    urlx="%s/index.php%s" % (baseurl,arg)
    code=downpage(urlx)
    result['PrevPage']=not isfirstpage(code)
    result['NextPage']=not islastpage(code)
    listi=getlistitemarray(code)
    for it in listi:
        result["Data"].append(getlistitemdata(it))
    return result

def getBangumVideoList(aurl,avid):
    code=downpage(aurl)
    try:
        code=code.split("<div class=\"module\">")[1]
    except:
        pass
    playlist=[]
    cnc=[]
    srcid="1"
    regstr="<a href=\"/index.php/vod/play/id/%s/sid/%s/nid/([\d]+).html\".*title=\"([^\\\"]+)\"><span>(.*?)</span></a>" % (avid,srcid)
    try:
        rpx=re.findall(regstr,code)
        for i in rpx:
            itm={'title' : i[2],
                  'vid': avid,
                  'srcid': srcid,
                  'epid': i[0]}
            if i[0] not in cnc:
                playlist.append(itm)
                cnc.append(i[0])
    except ValueError:
            pass
    return playlist

def getPlayUrl(avid,srcid,epid):
    print("read url: avid : %s srcid: %s epid: %s" % (avid,srcid,epid))
    playurl="%s/index.php/vod/play/id/%s/sid/%s/nid/%s.html" % (baseurl,avid,srcid,epid)
    playpage=downpage(playurl)
    purl=""
    try:
        sr=re.findall("var player_aaaa=(.*?)</script>",playpage)[0]
        jr=json.loads(sr)
        purl=jr["url"]
    except:
        return ""
    if purl=="":
        return ""
    code=downsrc(purl)
    bt_token=re.findall("var\sbt_token\s=\s\"(.*?)\"",code)[0]
    video_key=re.findall("getVideoInfo\(\"(.*?)\"\)",code)[0]
    curl=decodeKey(video_key,bt_token)
    k1=curl.split("&")[0].split("?")[0]
    k2,k3=os.path.splitext(k1)
    if k3.startswith('.'):
        k3=k3[1:]
    if k3=="":
        k3="fdv"
    if k3=="html" or k3=="htm":
        curl=""
    return {'url':curl,'ext':k3}
 
