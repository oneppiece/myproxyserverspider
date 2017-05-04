# coding=utf-8
import re

p = re.compile(
	r"<tr><td data-title=\"IP\">(?P<IP>.+?)</td><td data-title=\"PORT\">(?P<PORT>.+?)</td>"
	"<td data-title=\"匿名度\">(?P<NIMINGDU>.+?)</td>"
	"<td data-title=\"类型\">(?P<KIND>.+?)</td>"
	"<td data-title=\"get/post支持\">(?P<HTTPMETHOD>.+?)</td>"
	"<td data-title=\"位置\">(?P<LOCATION>.+?)</td>"
	"<td data-title=\"响应速度\">(?P<SPEED>.+?)</td>"
	"<td data-title=\"最后验证时间\">(?P<LASTVALID>.+?)</td></tr>", re.I)

m = p.match(
	"<tr><td data-title=\"IP\">127.0.0.1</td><td data-title=\"PORT\">9000</td>"
	"<td data-title=\"匿名度\">高匿名</td><td data-title=\"类型\">HTTP</td>"
	"<td data-title=\"get/post支持\">GET, POST</td>"
	"<td data-title=\"位置\">中国 江苏省 镇江市 电信</td>"
	"<td data-title=\"响应速度\">2秒</td>"
	"<td data-title=\"最后验证时间\">1分钟前</td></tr>")
# print m
print m.group()
print m.groups()
print m.groupdict()


# p = re.compile(r"<tr><td data-title=\"IP\">(?P<IP>.+?)</td><td data-title=\"PORT\">(?P<PORT>.+?)</td>")
# m = p.match("<tr><td data-title=\"IP\">127.0.0.1</td><td data-title=\"PORT\">9000</td>")
# print m.groupdict()