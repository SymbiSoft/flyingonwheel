import MultipartPostHandler, urllib2, cookielib

latitude = str('23.34')
longitude = str('34.45')
file = 'logo.jpg'

cookies = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies), MultipartPostHandler.MultipartPostHandler)
params = { 'point': '%s, %s' % (latitude, longitude), "picblob": open(file, "rb") }
answer = opener.open("http://flyingonwheel.appspot.com/mark_test", params)
print answer.code
