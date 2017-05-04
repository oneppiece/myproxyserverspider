# coding=utf-8
import json
import urllib2

default_page_index = 1

__start_with__ = "var tvInfoJs="
html = urllib2.urlopen(r'http://cache.video.qiyi.com/jp/avlist/204969801/1/50/?albumId=204969801')

r = html.read()

j = r.strip()[len(__start_with__):]

result = json.loads(j)

v_info = result.get("data")  # dict

print "分页大小:", v_info.get("pp")
print "总集数:", v_info.get("pm")
print "当前返回多少条:", v_info.get("pn")
print "更新至第几集:", v_info.get("pt")
print "总页数:", v_info.get("pgt")
data_list = v_info.get("vlist")  # array
print "数据:"

count = 0

for data in data_list:
	print "图片地址:", data.get("vpic")
	print "视频地址:", data.get("vurl")
	print "视频短名称:", data.get("shortTitle")
	count += 1
	print "count:%d" % count
html.close
