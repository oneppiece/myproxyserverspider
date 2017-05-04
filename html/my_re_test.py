# coding=utf-8
import sys
import urllib2

import re

reload(sys)
print sys.getdefaultencoding()
sys.setdefaultencoding("utf-8")
print sys.getdefaultencoding()

conn = urllib2.urlopen(r"http://list.iqiyi.com/www/2/----------------iqiyi--.html")
r = conn.read()

reg_tv1 = re.compile(
	r"(data-qipuid=\"\d+\"\s+)(alt=\".+?\")(\s+.+?\s?){4}>\s+<img(\s+.+?\s?){5}src\s=(\s?\".+?\")",
	re.I)  # 正则表达式
f = reg_tv1.findall(r)
for ff in f:  # 每个正则解析结果
	print ff[4].strip()[1:len(ff[4].strip())-1]
conn.close()
