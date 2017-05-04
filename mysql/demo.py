# coding=utf-8
import datetime
import sys

import MySQLdb

reload(sys)
print sys.getdefaultencoding()
sys.setdefaultencoding("utf-8")
print sys.getdefaultencoding()

conn = None
conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='py', use_unicode=True)

conn.set_character_set('utf8')

curs = conn.cursor()
curs.execute('SET NAMES utf8;')
curs.execute('SET CHARACTER SET utf8;')
curs.execute('SET character_set_connection=utf8;')

dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print dt
curs.execute(
	"insert into ku_aiqiyi (v_name,v_vid,v_img,v_state,v_actors,create_time) values ('%s','%s','%s','%s','%s','%s')" % (
		"无间道", "http://www.iqiyi.com/a_19rrh9s4yl.html#vfrm=2-4-0-1",
		"http://pic8.qiyipic.com/image/20170302/a9/4a/a_100033379_m_601_m14_180_236.jpg",
		"共12集全", "主演", dt))
curs.close()
conn.commit()
conn.close()
