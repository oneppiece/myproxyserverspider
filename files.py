# coding=utf-8
import re
from re import MULTILINE


l = open("1.txt", "r").read()
p = re.compile(
	r"<tr>\s+<td data-title=\"IP\">(?P<IP>.+?)</td>\s+<td data-title=\"PORT\">(?P<PORT>.+?)</td>"
	"\s+<td data-title=\"匿名度\">(?P<NIMINGDU>.+?)</td>"
	"\s+<td data-title=\"类型\">(?P<KIND>.+?)</td>"
	"\s+<td data-title=\"get/post支持\">(?P<HTTPMETHOD>.+?)</td>"
	"\s+<td data-title=\"位置\">(?P<LOCATION>.+?)</td>"
	"\s+<td data-title=\"响应速度\">(?P<SPEED>.+?)</td>"
	"\s+<td data-title=\"最后验证时间\">(?P<LASTVALID>.+?)</td>\s+</tr>", re.I)
# print l
m = p.match(l)
# if m is None:
print m
print p.findall(l)  # elif not m.group() is None:
# print m.group()
# print m.groups()
# print m.groupdict()  # for li in l:
# 	li = li.rstrip()
# 	print li
