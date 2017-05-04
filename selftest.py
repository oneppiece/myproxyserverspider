# coding=utf-8
import threading
import urllib2

import time

proxy_list_g = []


class proxy_test(threading.Thread):
	def __init__(self, proxylist, fname):
		threading.Thread.__init__(self)
		self.proxylist = proxylist
		self.timeout = 5
		self.test_url = "http://www.baidu.com"
		self.test_str = "030173"
		self.fname = fname
		self.checkedList = []

	def check(self):
		cookies = urllib2.HTTPCookieProcessor()
		# 构建代理服务器
		for proxy in self.proxylist:
			proxy_handler = urllib2.ProxyHandler({"http": r"http://%s:%s" % (proxy[0], proxy[1])})
			opener = urllib2.build_opener(cookies, proxy_handler)
			opener.addheaders = [("User-Agent",
			                      r"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2595.400 QQBrowser/9.6.10872.400")]
			urllib2.install_opener(opener)
			t1 = time.time()
			try:
				req = urllib2.urlopen(self.test_url, timeout=self.timeout)
				result = req.read()
				timeuse = time.time() - t1
				pos = result.find(self.test_str)
				if pos > 1:
					self.checkedList.append((proxy[0], proxy[1], proxy[2], timeuse))
				else:
					continue
			except Exception, e:
				print e.message
				continue

	def sort(self):
		sorted(self.checkedList, cmp=lambda x, y: cmp(x[3], y[3]))

	def save(self):
		f = open(self.fname, "w+")
		for proxy in self.checkedList:
			f.write("%s:%s \t %s %s\n" % (proxy[0], proxy[1], proxy[2], proxy[3]))
		f.close()

	def run(self):
		self.check()
		self.sort()
		self.save()


if __name__ == "__main__":
	f = open("result.txt", "r")
	r = f.readlines()
	count = 0
	for l in r:
		count += 1
		print "正在写:", l, count
		s = l.rstrip().split("---")
		if not s[0].startswith("写入时间"):
			ip = s[0]
			port = s[1]
			addr = s[5]
			result = [ip, port, addr]
			proxy_list_g.append(result)
	print len(proxy_list_g)

	t1 = proxy_test(proxy_list_g, "final_result.txt")
	t1.start()
