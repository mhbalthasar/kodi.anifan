# -*- coding: utf-8 -*-
import json
import re
import sys
import os
import urllib

import urllib2
import urlparse
import xbmc
import xbmcgui
import xbmcplugin
import xbmcgui as gui
import xbmcplugin as plug
import xbmcaddon
import time
from datetime import datetime
#import fs

reload(sys)
sys.setdefaultencoding("utf-8")

sys.path.append("%s/videosource" % os.path.split(os.path.realpath(__file__))[0])
import adapter2 as src

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    query["website"]="website2"
    return base_url + '?' + urllib.urlencode(query)

def setupinfo(li,vurl):
    url=vurl["url"]
    ext=vurl["ext"].lower()
    li.setProperty('isplayable', 'true')
    if ext == "mp4" :
        li.setProperty('mimetype', 'video/mp4')
    elif ext == "fdv" :
        li.setProperty('mimetype', 'video/mp4')

def readSrv():
    addon = xbmcaddon.Addon()
    if addon.getSetting('m3u8dex') == 'true':
        return addon.getSetting('m3u8srv')
    return ""

def main():
    mode = args.get('mode', None)
    #这里是初始界面
    if mode is None:
        byear=int(time.strftime("%Y", time.localtime()))
        li = gui.ListItem(u"全部年份".encode('utf-8'))
        url = build_url({'mode' : 'yearlist', 'year' : 'all', 'page': '1'})
        plug.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
        for i in range(10):
            xw=byear-i
            li = gui.ListItem((str(xw)).encode('utf-8'))
            url = build_url({'mode' : 'yearlist', 'year' : str(xw), 'page': '1'})
            plug.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
        
        plug.endOfDirectory(addon_handle)
    
    #按年加载
    elif mode[0] == 'yearlist':
        year = args['year'][0] #获取参数
        page = args['page'][0]
        lst=src.getList(year,str(int(page)))
        data=lst["Data"]
        for dti in data:
            aurl=dti["url"]
            atitle=dti["title"]
            astatus=dti["status"]
            avid=dti["vid"]
            apic=dti["pic"]
            li = gui.ListItem("%s [%s]" % (atitle,astatus))
            li.setIconImage( apic or '')
            li.setArt({ 'thumb': apic or ''})
            url = build_url({'mode' : 'bangumplay', 'aurl' : aurl, 'vid': avid, 'bangumtitle' : atitle, 'bpic': apic })
            plug.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    
        if lst["NextPage"]:
            li = gui.ListItem(u"下一页".encode('utf-8'))
            pg=int(page)+1
            url = build_url({'mode' : 'yearlist', 'year' : year, 'page': str(pg)})
            plug.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    
        plug.endOfDirectory(addon_handle)
    
    
    elif mode[0] == "bangumplay":
        aurl = args['aurl'][0] #Aurl
        avid = args['vid'][0]
        btitle = args['bangumtitle'][0]
        apic = args['bpic'][0]
        plist=src.getBangumVideoList(aurl,avid)
        for eli in plist:
            avid=eli["vid"]
            srcid=eli["srcid"]
            title=eli["title"]
            epid=eli["epid"]
            li = gui.ListItem("%s - %s" % (title, btitle))
            li.setIconImage( apic or '')
            li.setArt({ 'thumb': apic or ''})
            url = build_url({'mode' : 'playvideo', 'title': title, 'vid': avid, 'srcid': srcid, 'epid' : epid, 'bangumtitle': btitle, 'bpic': apic})
            plug.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    
        plug.endOfDirectory(addon_handle)
    
    elif mode[0] == 'playvideo':
        vid = args['vid'][0] #Aurl
        srcid = args['srcid'][0]
        epid = args['epid'][0]
        title = args['title'][0]
        vurl = src.getPlayUrl(vid,srcid,epid)
        btitle = args['bangumtitle'][0]
        apic = args['bpic'][0]
        if vurl == '':
            li = gui.ListItem("%s [ %s ]解析失败,请换源或重试" % (title,btitle))
            url = build_url({'mode' : 'playvideo', 'title': title, 'vid': vid, 'srcid': srcid, 'epid' : epid})
            li.setIconImage( apic or '')
            li.setArt({ 'thumb': apic or ''})
            plug.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
        elif vurl["url"] == '':
                li = gui.ListItem("%s [ %s ]地址解析失败,请换源或重试" % (title,btitle))
                li.setIconImage( apic or '')
                li.setArt({ 'thumb': apic or ''})
                url = build_url({'mode' : 'playvideo', 'title': title, 'vid': vid, 'srcid': srcid, 'epid' : epid})
                plug.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
        else:
            li = gui.ListItem("点击播放 %s [%s] - %s" % (title, vurl["ext"], btitle))
            li.setIconImage( apic or '')
            li.setArt({ 'thumb': apic or ''})
            #%s [%s]".decode().encode() % (title,vurl["ext"]))
            setupinfo(li,vurl)
            plug.addDirectoryItem(handle=addon_handle, url=vurl["url"], listitem=li)
            if vurl["ext"].lower()=="m3u8":
                if readSrv()!="":
                    li = gui.ListItem("点击解析播放 %s [%s] - %s" % (title, vurl["ext"], btitle))
                    li.setIconImage( apic or '')
                    li.setArt({ 'thumb': apic or ''})
                    #%s [%s]".decode().encode() % (title,vurl["ext"]))
                    setupinfo(li,vurl)
                    rsrv=readSrv()
                    if not rsrv.endswith("/"):
                        rsrv=rsrv+"/"
                    plug.addDirectoryItem(handle=addon_handle, url=rsrv+"m3u8/"+vurl["url"], listitem=li)
        
        plug.endOfDirectory(addon_handle)
    
    
    elif mode[0] == "setm3u8":
        sfile="m3u8srv.txt";
        saddr=readSrv();
        kb = xbmc.Keyboard(saddr, u'请输入M3U8解析服务器的地址,如:http://abc.com/'.encode('utf-8'))
        kb.doModal()
        if kb.isConfirmed():
            mhst=kb.getText()
            saddr=mhst
            with open(sfile,'w') as f:
                f.write(saddr)
        li = gui.ListItem(u"M3U8服务器:%s" % saddr)
        url = build_url({'mode' : 'setm3u8'})
        plug.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
        plug.endOfDirectory(addon_handle)
    
    #BELOW IS THE TEMPLATE CODE
    elif mode[0] == 'get_av_id':
        kb = xbmc.Keyboard('', u'手动输入 av 号'.encode('utf-8'), False)
        kb.doModal()
        if kb.isConfirmed():
            av_id = kb.getText()
            view_url = 'https://www.biliplus.com/api/view?id=%s' % av_id
            view_info = json.loads(urllib2.urlopen(view_url).read())
            pages = view_info['list']
            for page in pages:
                url = build_url({'mode': 'video', 'av_id': av_id, 'page': page['page'],'bangumi':'0'})
                li = xbmcgui.ListItem(page['part'].encode('utf-8'), iconImage=view_info['pic'])
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
            xbmcplugin.endOfDirectory(addon_handle)
    elif mode[0] == 'folder':
        foldername = args['foldername'][0]
        link = args['link'][0].encode('utf-8')
        bangumi_info = json.loads(urllib2.urlopen('https://www.biliplus.com/api/bangumi?season=%s' % link).read())
        episodes = bangumi_info['result']['episodes']
        for episode in episodes:
            av_id = episode['av_id'].encode('utf-8')
            index = episode['index'].encode('utf-8')
            title = episode['index_title'].encode('utf-8')
            cover = 'http:' + episode['cover'].encode('utf-8')
            url = build_url({'mode': 'video', 'av_id': av_id, 'page': '1', 'bangumi': '1'})
            li = xbmcgui.ListItem(index + ' ' + title, iconImage=cover)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
        xbmcplugin.endOfDirectory(addon_handle)
    
    elif mode[0] == 'video':
        av_id = args['av_id'][0]
        page = args['page'][0]
        bangumi = args['bangumi'][0]
        info_url = 'https://www.biliplus.com/api/geturl?bangumi=%s&av=%s&page=%s' % (bangumi, av_id, page)
        episode_info = json.loads(urllib2.urlopen(info_url).read())['data']
        for video in episode_info:
            if video['type'].encode('utf-8') == 'split':
                for pats in video['parts']:
                    name = video['name'].encode('utf-8')
                    video_url = pats['url'].encode('utf-8')
                    li = xbmcgui.ListItem(name)
                    xbmcplugin.addDirectoryItem(handle=addon_handle, url=video_url, listitem=li)
        xbmcplugin.endOfDirectory(addon_handle)
