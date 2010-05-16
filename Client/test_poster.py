import urllib2
import urllib
import httplib

url = "http://flyingonwheel.appspot.com/mark_test"

latitude = str('23.34')
longitude = str('34.45')

file = 'D:\logo.jpg'
params = urllib.urlencode([('point', '%s, %s' % (latitude, longitude))])
file_object = open(file, 'r')
jtlContent = file_object.read()
headers = {"Content-type":"multipart/form-data;","Accept": "text/plain"}
conn =httplib.HTTPConnection("flyingonwheel.appspot.com")
finalUrl=url+'?'+params
print finalUrl
conn.request("POST", finalUrl, jtlContent, headers)
response = conn.getresponse()
print ("result deal info:",response.status, response.reason,response.read())

"""
# test_client.py
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2

# Register the streaming http handlers with urllib2
register_openers()

# Start the multipart/form-data encoding of the file "DSC0001.jpg"
# "image1" is the name of the parameter, which is normally set
# via the "name" parameter of the HTML <input> tag.

# headers contains the necessary Content-Type and Content-Length
# datagen is a generator object that yields the encoded parameters
datagen, headers = multipart_encode({"image1": open("D:\photo.txt")})

# Create the Request object
request = urllib2.Request("http://localhost:5000/upload_image", datagen, headers)
# Actually do the request, and get the response
print urllib2.urlopen(request).read()
"""