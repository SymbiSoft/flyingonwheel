#-*- coding: utf-8 -*-
#Author: iamsk <skxiaonan@gmail.com>
#Last Change: 2010-05-16
#Description: mark current position and post it to flyingonwheel.appspot.com
#Notice: your phone must have the 'Location' (GPS data /position) application on, 
#and receive satalite data in order to make this script work. (can be problematic indoors).
#Latitute: 纬度, Longitute: 经度

import sys
import os
sys.path.append('e:\\data\\python')
import time
import urllib
import urllib2
import cookielib

import e32
import positioning
import appuifw
import e32dbm
import camera
import key_codes
from graphics import Image

import MultipartPostHandler

DB_FILE = 'e:\\flyingonwheel.db'
MARK_URL = 'http://flyingonwheel.appspot.com/mark'
file_pic = 'e:\\photo.jpg'
photo_taked = False

def de_cn(x):
    return x.decode("utf-8")

def en_cn(x):
    return x.encode("utf-8")

def viewfinder(img):
    """
        handled by camera.take_photo, use for showing current pic
    """
    canvas.blit(img)

def shoot():
    """
        shoot a pic and save it
    """
    camera.stop_finder()
    photo = camera.take_photo(size = (640, 480))
    w, h = canvas.size
    canvas.blit(photo, target = (0, 0, w, h), scale = 1)
    photo.save('e:\\photo.jpg')
    photo_taked = True

def takePhoto():
    """
        take a photo
    """
    photo_taked = False
    camera.start_finder(viewfinder)
    canvas.bind(key_codes.EKeySelect, shoot)

def postPosition(data):
    """
        post data to flyingonwheel.appspot.com
    """
    if data:
        # Read the name and password from db
        db = e32dbm.open(DB_FILE, "r")
        name = db[u"name"]
        password = db[u"password"]
        db.close()
        address_name, address_info = flyer_input()
        appuifw.note(u"Posting position information ...", "info")
        latitude = str(data['position']['latitude'])
        longitude = str(data['position']['longitude'])
        file_data = open(file_pic, 'rb')
        try:
            cookies = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies), MultipartPostHandler.MultipartPostHandler)
            params = { 'flyer_name': '%s' % name, 'password': '%s' % password, 'point': '%s, %s' % (latitude, longitude), 'name': '%s' % en_cn(address_name), 'point_info': '%s' % en_cn(address_info), "picblob": file_data }
            answer = opener.open(MARK_URL, params)
            if answer.code == 200:
                appuifw.note(u"Position Information Posted", "info")
            else:
                appuifw.note(u"Please check your network", "info")
        except:
            appuifw.note(u"Could not posting information", "info")

def getPosition():
    """
        Get GPS co-ordinates
    """
    appuifw.note(u"Getting Current GPS...", "info")
    positioning.select_module(positioning.default_module())
    positioning.set_requestors([{'type': 'service', 'format': 'application', 'data': 'position'}])
    appuifw.note(u"Retrieving GPS co-ordinates ...", "info")
    try:
        result = positioning.position(course=1, satellites=1)
    except:
        appuifw.note(u"Could not retrieve GPS co-ordinates", "info")
    else:
        appuifw.note(u"GPS co-ordinates retrieved", "info")
    return result
    
def quit():
    """
        Change exit to here
    """
    app_lock.signal()
    
def not_here():
    """
        bind Exit button to this
    """
    appuifw.note(u"Exit isn't here", "info")

def writeLog(data):
    """
        write the log
    """
    if data:
        try:
            file('e:\\gpslog.log', 'a').write('%s|%s|%s\n\n' % (str(time.ctime()), str(data['position']['latitude']), str(data['position']['longitude'])))
        except:
            appuifw.note(u"Writing log error", "info")
        else:
            appuifw.note(u"Log writed", "info")

def mark():
    """
        mark starts here
    """
    appuifw.note(u"Start mark ...", "info")
    data = getPosition()
    takePhoto()
    e32.ao_sleep(3)
    if photo_taked:
        postPosition(data)
        writeLog(data)
        appuifw.note(u"End mark", "info")
    else:
#        e32.ao_sleep(7)
        postPosition(data)
        writeLog(data)
        appuifw.note(u"End mark", "info")
    canvas.blit(photo)

def setting():
    """
        setting the name and password
    """
    name = appuifw.query(u"Type your Name: ", "text")
    password = appuifw.query(u"Type your Password: ", "code")
    if name and password:
        db = e32dbm.open(DB_FILE, "cf")
        db[u"name"] = name
        db[u"password"] = password
        db.close()
    else:
        appuifw.note(u"Cancel!", "info")

def flyer_input():
    """
        input the address name and the address description
    """
    address_name = appuifw.query(u"Type address Name: ", "text")
    address_info = appuifw.query(u"Type address Description: ", "text")
    return address_name, address_info

if __name__ == '__main__':
    appuifw.app.body = canvas = appuifw.Canvas()
    appuifw.app.title = u"Flying on Wheel"
    photo = Image.open("e:\\data\\python\\bg.jpg")
    canvas.blit(photo)
    app_lock = e32.Ao_lock()
    appuifw.app.menu = [(u"Setting", setting), (u"Start Mark", mark), (u"Exit", quit)]
    appuifw.app.exit_key_handler = not_here
    app_lock.wait()
