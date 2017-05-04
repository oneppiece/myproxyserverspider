# -*- coding=UTF-8 -*-
import json
import sys
import threading
import urllib2

import re

import datetime
import time

import MySQLdb

reload(sys)
print sys.getdefaultencoding()
sys.setdefaultencoding("utf-8")
print sys.getdefaultencoding()
a = ""

# 爬爱奇艺排行榜
# 1.根据排行 爬vid
# 2.根据vid 爬分集

# a = "http://list.iqiyi.com/www/category/----------kind---11-page-1-iqiyi--.html"

# 默认 1页
v_default_page = 1


# (网址模板,正则表达式)
class aiqiyi(threading.Thread):
	def __init__(self, url_template):
		threading.Thread.__init__(self)
		self.url_template = url_template  # 爱奇艺网址模板
		self.reg_tv1 = re.compile(
			r"(href=.+?\s+class=\"site-piclist_pic_link\"\s+target=\"_blank\">)\s+(<img(\s.+?=.+?){5}\s+src\s=\s.+?\s+/>)\s+(<p(\s.+?=.+?)+></p>\s+)?(<\w+\s\w+=.+?>\s+){3}(<span\s\w+=.+?>\s+.+?\s+</span>\s+)(</\w+>\s+){5}(<\w+\s(.+?=.+?(\s)?\"(\s)?>))?(.+?)(<div\sclass=\"site-piclist_info\">\s?([\s\S]+?)(<em>.+?:</em>\s+(<em>([\s\S]+?)</em>\s+)+)+)",
			re.I)  # 正则表达式
		self.reg_tv = re.compile(r"(data-qipuid=\"\d+\"\s+)(alt=\".+?\")", re.I)  # 正则表达式

		self.read_list = []  # 读列表
		self.write_temp_list = []  # 写临时列表
		self.category_range = (1, 2)  # 1 电影 2 电视剧
		self.kind_range = (0, 2, "")  # 0 免费 2 付费 "" 全部
		self.sort_range = (4, 11)  # 4 更新时间 11热门
		self.page_range = 10  # 页数
		self.url_count = 0  # url地址的个数
		self.v_slot_info = []  # 视频以及vid写列表
		self.__start_with__ = "var tvInfoJs="  # jsonp变量名
		self.next_page_list = []  # 不止一页的剧集

	def generate_url(self):
		# global category_range, kind_range, page_range, all_urls
		url_template = self.url_template
		for c in self.category_range:
			if c == 1:
				continue
			else:
				cr = url_template.replace("category", str(c))
				for k in self.kind_range:
					rk = cr.replace("kind", str(k))
					for s in self.sort_range:
						sr = rk.replace("sort", str(s))
						for p in range(self.page_range):
							if k == 2 and p >= 2:
								continue
							else:
								pr = sr.replace("page", str(p + 1))
								self.read_list.append(pr)
		self.url_count = len(self.read_list)
		print "生成了%d个网址" % self.url_count

	# 通过正则表达式读结果
	def get_html_reg(self):
		for u in self.read_list:  # 每个网址
			# time.sleep(1)
			print "睡觉..."
			try:
				conn = urllib2.urlopen(u)
				r = conn.read()
				f = self.reg_tv.findall(r)
				for ff in f:  # 每个正则解析结果
					v_id = ff[0][ff[0].find("=") + 2:len(ff[0].rstrip()) - 1]
					v_name = ff[1][ff[1].find("=") + 2:len(ff[1].rstrip()) - 1]
					v_temp = [v_id, v_name]
					self.write_temp_list.append(v_temp)
				conn.close()

				print "第%d个视频 当前网址:%s" % (len(self.write_temp_list), u)
			except Exception, e:
				print "打不开！！！", e.message
				continue

	# 将结果写入数据库临时表
	def write_db_temp(self):
		conn = None
		conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='py', use_unicode=True)
		conn.set_character_set('utf8')
		print "准备写"
		curs = conn.cursor()
		curs.execute('SET NAMES utf8;')
		curs.execute('SET CHARACTER SET utf8;')
		curs.execute('SET character_set_connection=utf8;')
		for l in self.write_temp_list:  # 一条数据
			dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			sql = "insert into ku_aiqiyi_temp (v_vid,v_name,create_time) values ('%s','%s','%s')" % (l[0], l[1], dt)
			print str(l[0]).decode("utf-8"), l[1].encode("utf-8"), l[1].decode("utf-8"), dt
			print sql
			curs.execute(sql)
			print "正在写..."

		curs.close()
		conn.commit()
		conn.close()

		print "写完了"

	# 打开temp,解析json 步骤1
	def parse_json(self):
		global v_default_page
		for line in self.write_temp_list:
			url_temp = r'http://cache.video.qiyi.com/jp/avlist/%d/page/50/?albumId=%d' % (int(line[0]), int(line[0]))
			url = r'http://cache.video.qiyi.com/jp/avlist/%d/%d/50/?albumId=%d' % (
				int(line[0]),
				v_default_page, int(line[0]))
			try:
				html = urllib2.urlopen(url)

				r = html.read()
				j = r.strip()[len(self.__start_with__):]

				json_result = json.loads(j)  # 解析json

				html.close

				if json_result.get("code") != "A00000":  # 获取不到
					continue
				else:
					self.__parse_video__(json_result, line[1], url_temp)

				# 如果结果不止一页,循环出每页信息
				# if v_current_pages < v_total_pages:
				# 	url = r'http://cache.video.qiyi.com/jp/avlist/%d/v_slot/50/?albumId=%d' % (
				# 		int(line[0]), int(line[0]))
				# 	self.parse_loop(url, line[1], v_total_pages)

			except Exception, e:
				print e.message
				continue
		print "解析完了.."

	# 解析每一页 .json_result:每一页的json v_name:名字 url_temp:url模板(不包含第几页)
	def __parse_video__(self, json_result, v_name, url_temp):
		v_info = json_result.get("data")  # dict

		v_page_total = v_info.get("pp")
		print "分页大小:", v_page_total
		v_total = v_info.get("pm")
		current_back_total = v_info.get("pn")
		print "当前返回多少条:", current_back_total
		v_update_slot = v_info.get("pt")
		v_total_pages = int(v_info.get("pgt"))
		v_current_pages = int(v_info.get("pg"))

		data_list = v_info.get("vlist")  # array
		if len(data_list) == 0:
			print "没有数据:"
		print "数据:", data_list
		v_state = u"共%d集,已完结" % v_total
		if v_total == v_update_slot:
			v_state = u"共%d集更新至第%d集" % (v_total, v_update_slot)
		v_actors = u"演员"
		for data in data_list:
			print "正在解析parse_json...", v_name
			write_line = []
			pic = data.get("vpic")
			vurl = data.get("vurl")
			short_name = data.get("shortTitle")
			v_current_slot = data.get("pd")

			write_line.append(vurl)  # 视频地址
			write_line.append(v_name)  # 视频名称
			write_line.append(pic)  # 图片地址
			write_line.append(v_state)  # 视频更新状态
			write_line.append(v_actors)  # 演员
			write_line.append(v_current_slot)  # 第几集
			write_line.append(short_name)  # 名字
			write_line.append(url_temp)  # 解析的url,如果不止一页,需要loop解析
			write_line.append(v_total_pages)  # 总页数

			self.v_slot_info.append(write_line)

	# 对多页循环
	def parse_loop(self):
		for p in self.v_slot_info:
			if int(p[8]) > 1:  # p[8]:总页数.如果页数大于1需要循环解析出每一页
				for i in range(int(p[8]) + 1):
					if i <= 1:
						continue
					current_page = i
					url = p[7].replace("page", i)
					html = urllib2.urlopen(p)
					r = html.read()
					j = r.strip()[len(self.__start_with__):]
					json_result = json.loads(j)  # 解析json
					html.close
					self.__parse_video__(json_result, p[1], p[7])

	def write_db(self):
		conn = None
		conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='py', use_unicode=True)
		conn.set_character_set('utf8')
		print "准备写播放地址..."
		curs = conn.cursor()
		curs.execute('SET NAMES utf8;')
		curs.execute('SET CHARACTER SET utf8;')
		curs.execute('SET character_set_connection=utf8;')
		for l in self.v_slot_info:
			dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			sql = "insert into ku_aiqiyi (v_name,v_vid,v_img,v_state,v_actors,v_current_slot,create_time,short_name) values ('%s','%s','%s','%s','%s','%s','%s','%s')" % (
				l[1], l[0], l[2], l[3], l[4], l[5], dt, l[6])
			print sql
			curs.execute(sql)
			print "播放地址..."

		curs.close()
		conn.commit()
		conn.close()


def run(self):
	demo.generate_url()
	demo.get_html_reg()
	demo.write_db_temp()
	demo.parse_json()
	demo.parse_loop()
	demo.write_db()


if __name__ == "__main__":
	demo = aiqiyi(r"http://list.iqiyi.com/www/category/----------kind---sort-page-1-iqiyi--.html")
	demo.generate_url()
	demo.get_html_reg()
	demo.write_db_temp()
	demo.parse_json()
	demo.parse_loop()
	demo.write_db()
