import sys
import os
import json
import urllib
sys.path.append("%s/plugins/videosource" % os.path.split(os.path.realpath(__file__))[0])
import adapter1 as src1
import adapter2 as src2

#print("Debug Via: 22880 -2 -2")
#dat=src.getPlayUrl("22880","2","2")
#print(dat)
#dat=src.getWeekdayList()
#print(dat)

#dat=src2.getList("2022","1")
dat=src2.getPlayUrl("5143","1","1")
print(dat)
#c=src2.decodeKey("Viu6sq7HXZkltndm1F140MfTQwKwBYT0xE4rMzbpJLUpobwJ7IZRlBQl8WJBjsPDyiC19d9KZMAfvfgJ9NQLYmydcjSO4Qh7M8xutgDxHf02xk5ZeIvH3RpVMZgGf5RfyudaHUbijPvoOgZNwGob3aw2Ib36ZdsosV++huP9GNEP2OM1fos2C+a36B4NtLtO","ce361206ffb9f298")
#print(c)
