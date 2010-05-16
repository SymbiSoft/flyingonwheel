# Copyright (c) 2006 Jurgen Scheible
# image upload to URL

import httplib


def upload_image_to_url():
    
    filename = 'D:\logo.jpg'
    picture = file(filename).read()

    conn = httplib.HTTPConnection("www.mobilenin.com")
    conn.request("POST", "/pys60/php/upload_image_to_url.php", picture)
    print "upload started ..."
    response = conn.getresponse()
    remote_file = response.read()
    conn.close()
    print remote_file


upload_image_to_url()
