import urllib2

o = urllib2.urlopen(r"http://www.goudaitv.com/video/?52709-0-28.html")

r = o.read()

print r