#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#Author: iamsk <skxiaonan@gmail.com>
#Last Change: 2010-04-04
#Description: mark current position and post it to flyingonwheel.appspot.com
#Notice: your phone must have the 'Location' (GPS data /position) application on, 
#and receive satalite data in order to make this script work. (can be problematic indoors).
#Latitute: 纬度, Longitute: 经度

import sys
import time
import urllib
import httplib
import e32
import positioning
import appuifw
import e32dbm

DB_FILE = u"E:\\flyingonwheel.db"
MARK_URL = "http://flyingonwheel.appspot.com/mark"

def postPosition(data):
    """
        post data to flyingonwheel.appspot.com
    """
    if data:
        db = e32dbm.open(DB_FILE, "r")
        name = db[u"name"]
        password = db[u"password"]
        db.close()
        address_name, address_info = flyer_input()
        appuifw.note(u"Posting position information ...", 'info')
        latitude = str(data['position']['latitude'])
        longitude = str(data['position']['longitude'])
        params = urllib.urlencode([('flyer_name', '%s' % name), ('password', '%s' % password), ('point', '%s, %s' % (latitude, longitude)), ('name', '%s' % address_name), ('point_info', '%s' % address_info), ])
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = httplib.HTTPConnection("flyingonwheel.appspot.com")
        try:
            conn.request("POST", "/mark", params, headers)
        except:
            conn.close()
            appuifw.note(u"Could not posting information", 'info')
        else:
            conn.close()
            appuifw.note(u"Position Information Posted", 'info')

def getPosition():
    """
        Get GPS co-ordinates
    """
    appuifw.note(u"Getting Current Position...", 'info')
    positioning.select_module(positioning.default_module())
    positioning.set_requestors([{'type': 'service', 'format': 'application', 'data': 'position'}])
    appuifw.note(u"Retrieving GPS co-ordinates ...", 'info')
    try:
        result = positioning.position(course=1, satellites=1)
    except:
        appuifw.note(u"Could not retrieve GPS co-ordinates", 'info')
    else:
        appuifw.note(u"GPS co-ordinates retrieved", 'info')
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
    appuifw.note(u"Exit isn't here", 'info')

def writeLog(data):
    """
        write the log
    """
    if data:
        try:
            file('E:\\gpslog.log', 'a').write('%s|%s|%s\n\n' % (str(time.ctime()), str(data['position']['latitude']), str(data['position']['longitude'])))
        except:
            appuifw.note(u"Writing log error", 'info')
        else:
            appuifw.note(u"Log writed", 'info')

def mark():
    """
        starts here
    """
    appuifw.note(u"Start getPosition ...", 'info')
    data = getPosition()
    postPosition(data)
    writeLog(data)
    appuifw.note(u"End postPosition ...", 'info')

def setting():
    name = appuifw.query(u"Type your Name: ", "text")
    password = appuifw.query(u"Type your Password: ", "code")
    if name and password:
        db = e32dbm.open(DB_FILE, "cf")
        db[u"name"] = name
        db[u"password"] = password
        db.close()
    else:
        appuifw.note(u"Cancel!", 'info')

def flyer_input():
    address_name = appuifw.query(u"Type address Name: ", "text")
    address_info = appuifw.query(u"Type address Description: ", "text")
    return address_name, address_info
    
if __name__ == '__main__':
    appuifw.app.title = u"Flying on Wheel"
    app_lock = e32.Ao_lock()
    appuifw.app.menu = [(u"Setting", setting), (u"Start Mark", mark), (u"Exit", quit)]
    appuifw.app.exit_key_handler = not_here
    app_lock.wait()
