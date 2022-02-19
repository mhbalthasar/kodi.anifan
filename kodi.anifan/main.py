# -*- coding: utf-8 -*-
import sys
import os
import xbmc
import xbmcgui
import xbmcplugin
import xbmcgui as gui
import xbmcplugin as plug
import xbmcaddon
import urllib
import urlparse
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("%s/plugins" % os.path.split(os.path.realpath(__file__))[0])
import website1 as web1
import website2 as web2



base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(website):
    query={}
    query["website"]=website
    return base_url + '?' + urllib.urlencode(query)


site = args.get('website', None)

if site is None:
    li = gui.ListItem(u"网站A>>".encode('utf-8'))
    url = build_url("website1")
    plug.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    
    li = gui.ListItem(u"网站O>>".encode('utf-8'))
    url = build_url("website2")
    plug.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
  
    plug.endOfDirectory(addon_handle)
elif site[0] == "website1":
    web1.main();
elif site[0] == "website2":
    web2.main();
