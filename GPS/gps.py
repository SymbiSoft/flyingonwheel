#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#Author: alvayang <alvayang@tabex.org>
#Last Change: 
#Description: 

import positioning
import appuifw
import sys
import e32
import time


def writelog(data):
    if data:
	try:
            file('E:\\gpslog.log', 'a').write('%s|%s|%s\n' % \
                    (str(time.time()),str(data['position']['latitude']), \
                        str(data['position']['longitude'])))
        except Exception, e:
            sys.stdout.write("exception happend:" + str(e))

def quit():
    app_lock.signal()

def not_allowed():
    appuifw.note("请通过选项选择退出.".decode('utf-8'), 'info')

appuifw.app.title = u"GPS Logger"
app_lock = e32.Ao_lock()
appuifw.app.menu = [("退出在这里面".decode('utf-8'), quit)]
positioning.select_module(positioning.default_module())
positioning.set_requestors([{'type':'service','format':'application','data':'position'}])
positioning.position(course=1,satellites=1, callback=writelog,\
        interval=5000000, partial=0)
appuifw.app.exit_key_handler = not_allowed
app_lock.wait()

