import json
import re
import sys
import urllib

import urllib2
import urlparse
import string

#http://www.ccknkj.com/ribendongman/index___2022__addtime.html
baseurl="http://www.ccknkj.com/ribendongman"

def isfirstpage(code):
    sign="prev disabled"
    try:
        string.index(code, sign)
        return True
    except ValueError:
        return False

def islastpage(code):
    sign="next disabled"
    try:
        string.index(code,sign)
        return True
    except ValueError:
        return False

def getlistitemarray(code):
    return re.findall(r"<a class=\"img-pic\" (.*)</a>",code)

def getlistitemdata(itemc):
    m1=re.match("href=\"([^\"]+)\" title=\"([^\"]+)\"",itemc)
    url=m1.group(1)
    title=m1.group(2)
    try:
        status=re.findall("<span class=\"vtitle text-right\">([^<]+)</span>",itemc)[0]
    except:
        status=""
    return {'url':url,'title':title,'status':status}

def downpage(url):
    header = {
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language" : "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding" : "deflate",
        "Connection" : "keep-alive",
        "Referer" : "http://www.ccknkj.com/ribendongman/index___2022___2.html",
        "Upgrade-Insecure-Requests" : "1"
    }
    req = urllib2.Request(url, headers=header)
    return urllib2.urlopen(req).read()

def getList(year,page):
    result={
            'PrevPage': False,
            'NextPage': False,
            'Data':[]
            }
    code=downpage("%s/index___%s___%s.html" % (baseurl,year,page))
    result['PrevPage']=not isfirstpage(code)
    result['NextPage']=not islastpage(code)
    listi=getlistitemarray(code)
    for it in listi:
        result["Data"].append(getlistitemdata(it))
    return result


def getBangum(aurl):
    result=[]
    code=downpage(aurl)
    ml=re.findall("<a href=\"%s(.*).html\" target=\"_blank\">([^<]+)</a>" % aurl,code)
    for it in ml:
        itm={'title':it[1],'url' : "%s/%s.html" % (aurl,it[0])}
        result.append(itm)
    return result

def getVideo(aurl):
    code=downpage(aurl)
    m2=re.findall('zanpiancms_player\s=\s([^;<]+)',code)[0]
    m2j=json.loads(m2)
    vid=m2j["url"]
    api=m2j["apiurl"]
    furl="%s%s" % (api,vid)
    code2=downpage(furl)

