# -*- coding: utf-8 -*-
import json
import re
import sys
import urllib

import urllib2
import urlparse
import xbmc
import xbmcgui
import xbmcplugin
import xbmcgui as gui
import xbmcplugin as plug
import sourceadapter as src
import time

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

#bangumi_list_url = 'https://www.biliplus.com/?bangumi'


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)


mode = args.get('mode', None)
#这里是初始界面
if mode is None:
    byear=int(time.strftime("%Y", time.localtime()))
    li = gui.ListItem(u"全部年份".encode('utf-8'))
    url = build_url({'mode' : 'yearlist', 'year' : '', 'page': '1'})
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
    lst=src.getList(year,page)
#    if lst["PrevPage"]:
#        li = gui.ListItem(u"上一页".encode('utf-8'))
#        pg=int(page)-1
#        url = build_url({'mode' : 'yearlist', 'year' : year, 'page': str(pg)})
#        plug.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    data=lst["Data"]
    for dti in data:
        aurl=dti["url"]
        atitle=dti["title"]
        astatus=dti["status"]
        li = gui.ListItem("%s [%s]" % (atitle,astatus))
        url = build_url({'mode' : 'bangumpage', 'aurl' : aurl})
        plug.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
 
    if lst["NextPage"]:
        li = gui.ListItem(u"下一页".encode('utf-8'))
        pg=int(page)+1
        url = build_url({'mode' : 'yearlist', 'year' : year, 'page': str(pg)})
        plug.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    plug.endOfDirectory(addon_handle)

elif mode[0] == "bangumpage":
    aurl = args['aurl'][0] #Aurl
    plist=src.getBangum(aurl)

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
