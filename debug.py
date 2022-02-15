import sys
import os
import sourceadapter as src
import json
import urllib

#sys.path.append("./pkg")

#import js2py

#dat=src.getList(2022,1,0)
#print(dat)
#adat=src.getBangumVideoList("","18729","1")
dat=src.getPlayUrl("23080","1","1")
print(dat)
