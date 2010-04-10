import urllib2, urllib, sys
import appuifw

url = "http://flyingonwheel.appspot.com/mark_test"
latitude = str('23.34')
longitude = str('34.45')

params = urllib.urlencode([('point', '%s, %s' % (latitude, longitude))])

req = urllib2.Request(url)
try:
    fd = urllib2.urlopen(req, params)
except:
    appuifw.note(u"Could not posting information", 'info')
else:
    appuifw.note(u"Position Information Posted", 'info')

while 1:
    data = fd.read(1024)
    if not len(data):
        break
#    sys.stdout.write(data)
