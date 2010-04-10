import urllib2, urllib, sys
import appuifw
import httplib

url = "http://flyingonwheel.appspot.com/mark_test"
latitude = str('23.34')
longitude = str('34.45')

params = urllib.urlencode([('point', '%s, %s' % (latitude, longitude))])
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
conn = httplib.HTTPConnection("flyingonwheel.appspot.com")
#req = urllib2.Request(url)
try:
    conn.request("POST", "/mark", params, headers)
except:
    conn.close()
    appuifw.note(u"Could not posting information", 'info')
else:
    conn.close()
    appuifw.note(u"Position Information Posted", 'info')

#while 1:
#    data = fd.read(1024)
#    if not len(data):
#        break
#    sys.stdout.write(data)
