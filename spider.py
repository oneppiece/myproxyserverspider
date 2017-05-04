# -*- coding=UTF-8 -*-
import urllib2
import re
import sys
import datetime

reload(sys)
print sys.getdefaultencoding()
sys.setdefaultencoding("utf-8")
print sys.getdefaultencoding()


def get_html(addr, pages):
	f = open("1.txt", "w")
	for i in range(1, pages):
		target = str(addr) % i
		print target
		req = urllib2.urlopen(target)
		html = req.read()
		d = str(html).decode("utf-8")
		print isinstance(d, str)
		print isinstance(d, unicode)
		f.write(d)
		get_result(html)

	f.close()


def get_result(html):
	p = re.compile(
		r"<tr>\s+<td data-title=\"IP\">(?P<IP>.+?)</td>\s+<td data-title=\"PORT\">(?P<PORT>.+?)</td>"
		"\s+<td data-title=\"匿名度\">(?P<NIMINGDU>.+?)</td>"
		"\s+<td data-title=\"类型\">(?P<KIND>.+?)</td>"
		"\s+<td data-title=\"get/post支持\">(?P<HTTPMETHOD>.+?)</td>"
		"\s+<td data-title=\"位置\">(?P<LOCATION>.+?)</td>"
		"\s+<td data-title=\"响应速度\">(?P<SPEED>.+?)</td>"
		"\s+<td data-title=\"最后验证时间\">(?P<LASTVALID>.+?)</td>\s+</tr>", re.I)
	m = p.findall(html)
	write_result(m)


def write_result(result=list):
	if len(result):
		print len(result)
		f = open("result.txt", "a")
		writedate = "写入时间:" + str(datetime.datetime.now()) + "\n"
		f.write(writedate)
		for line in result:
			content = ""
			for i in range(len(line)):
				l = line[i].encode("utf-8")
				content += (l + "---")
			f.write(content + "\n")
		f.flush()
		f.close()


def selftest():
	f = open("result.txt", "w")
	rl = f.readlines()


get_html(r"http://www.kuaidaili.com/proxylist/%d/", 11)
	# write_result(html)
