# -*- coding: utf-8 -*-

import logging
from datetime import date
import datetime
import time
import re
import os
import hashlib

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from appengine_utilities import sessions
from google.appengine.api import memcache
from functools import wraps

logging.getLogger().setLevel(logging.DEBUG)

def requires_admin(method):
    """
        Check admin
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        is_admin = users.is_current_user_admin()
        if not is_admin:
            self.redirect(users.create_login_url(self.request.uri))
            return
        else:
            return method(self, *args, **kwargs)
    return wrapper

class MarkedPoint(db.Model):
    """
        The Point's infomation
    """
    name = db.StringProperty()
    point = db.GeoPtProperty()
    point_info = db.StringProperty()
    flyer_name = db.StringProperty()
    picblob = db.BlobProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    
    @property
    def id(self):
        return str(self.key().id())    

class Flyer(db.Model):
    """
        The Flyer's Infomation
    """
    name = db.StringProperty()
    password = db.StringProperty()
    address = db.StringProperty()
    flag = db.BooleanProperty()
    date = db.DateTimeProperty(auto_now_add=True)

def matchdateformat(stringdate):
    """
        Match the string format(0000-00-00)
    """
    p = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    if p.search(stringdate):
        return True
    else:
        return False

def stringtodate(stringdate):
    """
        Format the string date to date type(0000-00-00)
    """
    time_format = "%Y-%m-%d"
    tempstart = time.strptime(stringdate, time_format)
    dateformat = datetime.datetime(*tempstart[:3])
    return dateformat

class Mark(webapp.RequestHandler):
    """
        Mark the point
    """
    def get(self):
        """
            Error Infomation: Not allowed
        """
        pass
    def post(self):
        """
            Catch the post which come from the flyer who update the points
        """
        name = self.request.get("flyer_name")
        password = self.request.get("password")
        if checkRight(name, password):
            markedpoint = MarkedPoint(date=datetime.datetime.now() + datetime.timedelta(hours = 8))
            markedpoint.name = self.request.get("name")
            markedpoint.point = self.request.get("point")
            markedpoint.point_info = self.request.get("point_info")
            markedpoint.flyer_name = name
            # you can choice upload a pic or not
            tempblob = self.request.get("picblob")
            if tempblob:
                markedpoint.picblob = tempblob
            markedpoint.put()
            self.response.out.write('True')
        else:
            self.response.out.write('False')

class Mark_test(webapp.RequestHandler):
    """
        Mark the point, just test which for develop new function
    """
    @requires_admin
    def get(self):
        """
            The form of the point
        """
        template_values = {
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/mark_test.html')
        self.response.out.write(template.render(path, template_values))
    @requires_admin
    def post(self):
        """
            Catch the post which come from the flyer who update the points
        """
        markedpoint = MarkedPoint(date=datetime.datetime.now() + datetime.timedelta(hours = 8))
        markedpoint.name = self.request.get("name")
        markedpoint.point = self.request.get("point")
        markedpoint.point_info = self.request.get("point_info")
        markedpoint.flyer_name = self.request.get("flyer_name")
        # you can choice upload a pic or not
        tempblob = self.request.get("picblob")
        if tempblob:
            markedpoint.picblob = tempblob
        markedpoint.put()
        self.redirect('/mark_test')

class Marks(webapp.RequestHandler):
    """
        list of the one flyer's points
    """
    def get(self):
        """
            show the points which days to view
        """
        self.sess = sessions.Session(writer="cookie")
        keyname = 'flyer_name'
        if keyname in self.sess:
            # format the date
            startdate = self.request.get("startdate")
            enddate = self.request.get("enddate")
            if startdate == None or startdate == '' or not matchdateformat(startdate):
                startdate = date.today()
            else:
                # format the startdate
                startdate = stringtodate(startdate)
            if enddate == None or enddate == '' or not matchdateformat(enddate):
                enddate = date.today() + datetime.timedelta(days = 1)
            else:
                # format the enddate
                enddate = stringtodate(enddate)
            # select the flyer's points
            flyer_name = self.sess[keyname]
            markedpoints = db.GqlQuery ("SELECT * FROM MarkedPoint WHERE date > :1 AND date < :2 AND flyer_name = :3 ORDER BY date DESC", startdate, enddate, flyer_name)
            template_values = {
                'startdate': startdate.strftime("%Y-%m-%d"),
                'enddate': enddate.strftime("%Y-%m-%d"),
                'flyer_name': flyer_name,
                'markedpoints': markedpoints,
            }
            path = os.path.join(os.path.dirname(__file__), 'templates/marks.html')
            self.response.out.write(template.render(path, template_values))
        else:
            template_values = {
            }
            path = os.path.join(os.path.dirname(__file__), 'templates/welcome.html')
            self.response.out.write(template.render(path, template_values))

class Index(webapp.RequestHandler):
    """
        The main page of all flyer
    """
    def get(self):
        """
            show the points which days to view
        """
        self.sess = sessions.Session(writer="cookie")
        keyname = 'flyer_name'
        if keyname in self.sess:
            # format the date
            startdate = self.request.get("startdate")
            enddate = self.request.get("enddate")
            if startdate == None or startdate == '' or not matchdateformat(startdate):
                startdate = date.today()
            else:
                # format the startdate
                startdate = stringtodate(startdate)
            if enddate == None or enddate == '' or not matchdateformat(enddate):
                enddate = date.today() + datetime.timedelta(days = 1)
            else:
                # format the enddate
                enddate = stringtodate(enddate)
            # select the flyer's points
            flyer_name = self.sess[keyname]
            markedpoints = db.GqlQuery ("SELECT * FROM MarkedPoint WHERE date > :1 AND date < :2 AND flyer_name = :3 ORDER BY date DESC", startdate, enddate, flyer_name)
            template_values = {
                'startdate': startdate.strftime("%Y-%m-%d"),
                'enddate': enddate.strftime("%Y-%m-%d"),
                'flyer_name': flyer_name,
                'markedpoints': markedpoints,
            }
            path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
            self.response.out.write(template.render(path, template_values))
        else:
            template_values = {
            }
            path = os.path.join(os.path.dirname(__file__), 'templates/welcome.html')
            self.response.out.write(template.render(path, template_values))

def flyer_error(flyer_error):
    """
        The error page
    """
    template_values = {
        'flyer_error': flyer_error,
    }
    path = os.path.join(os.path.dirname(__file__), 'templates/error.html')
    return template.render(path, template_values)

def checkRight(name, password):
    """
        Check the post right
    """
    md5password = hashlib.md5()
    md5password.update(password)
    password = md5password.hexdigest()
    f = db.GqlQuery ("SELECT * FROM Flyer where name = :1 AND password = :2 AND flag = :3", name, password, True)
    if f.count() == 1:
        return True
    else:
        return False

class Login(webapp.RequestHandler):
    """
        Login and save the session
    """
    def get(self):
        """
            Login form
        """
        template_values = {
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/flyer_login.html')
        self.response.out.write(template.render(path, template_values))
    def post(self):
        """
            Catch the post from login
        """
        name = self.request.get("name")
        password = self.request.get("password")
        if checkRight(name, password):
            self.sess = sessions.Session(writer="cookie")
            keyname = 'flyer_name'
            self.sess[keyname] = name
            self.redirect('/')
        else:
            flyer_error = "Login Error, Please correct the Name&Password, Thanks~"
            template_values = {
                'flyer_error': flyer_error,
            }
            path = os.path.join(os.path.dirname(__file__), 'templates/error.html')
            self.response.out.write(template.render(path, template_values))

class Logout(webapp.RequestHandler):
    """
        Logout and clear the session
    """
    def get(self):
        self.sess = sessions.Session(writer="cookie")
        self.sess.delete()
        self.redirect('/')

class Flyer_register(webapp.RequestHandler):
    """
        Flyer Manage
    """
    def get(self):
        """
            The form of Flyer_rigister
        """
        f = db.GqlQuery ("SELECT * FROM Flyer")
        template_values = {
            'flyers_count': f.count()+1,
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/flyer_register.html')
        self.response.out.write(template.render(path, template_values))
    def post(self):
        """
            Save the flyer
        """
        flyer_name = self.request.get("name")
        flyer_password = self.request.get("password")
        flyer_repassword = self.request.get("repassword")
        tempflyers = db.GqlQuery ("SELECT * FROM Flyer where name = :1", flyer_name)
        # Check the passwd and the repasswd
        if flyer_password != flyer_repassword:
            flyer_error = "The password & repassword are not the same, Please correct it, Thanks~"
            template_values = {
                'flyer_error': flyer_error,
            }
            path = os.path.join(os.path.dirname(__file__), 'templates/error.html')
            self.response.out.write(template.render(path, template_values))
        # Look for registered or not
        elif tempflyers.count() >= 1:
            flyer_error = "This name has been registered, Please choice another one, Thanks~"
            template_values = {
                'flyer_error': flyer_error,
            }
            path = os.path.join(os.path.dirname(__file__), 'templates/error.html')
            self.response.out.write(template.render(path, template_values))
        # Save the flyer
        else:
            flyer = Flyer(date=datetime.datetime.now() + datetime.timedelta(hours = 8))
            md5password = hashlib.md5()
            md5password.update(flyer_password)
            flyer.name = flyer_name
            flyer.password = md5password.hexdigest()
            flyer.flag = True
            flyer.put()
            flyer_success = "Good Luck!, You have been registered, Have a good travel~<br/><a href='/login'>Login</>"
            template_values = {
                'flyer_success': flyer_success,
            }
            path = os.path.join(os.path.dirname(__file__), 'templates/success.html')
            self.response.out.write(template.render(path, template_values))

class Error404(webapp.RequestHandler):
    """
        If flyer enter a page which is not be found, will come here
    """
    def get(self):
        flyer_error = "You have enter a bad url which is not be found, Please check your url~"
        template_values = {
            'flyer_error': flyer_error,
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/error.html')
        self.response.out.write(template.render(path, template_values))

class Admin(webapp.RequestHandler):
    """
        The admin control
    """
    @requires_admin
    def get(self):
        """
            Get the list of flyers
        """
        tempflyers = db.GqlQuery ("SELECT * FROM Flyer")
        template_values = {
            'flyers': tempflyers,
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/admin.html')
        self.response.out.write(template.render(path, template_values))
    @requires_admin
    def post(self):
        """
            Manage the flyers
        """
        flyer_name = self.request.get("name")
        choice = self.request.get("choice")
        tempflyers = db.GqlQuery ("SELECT * FROM Flyer where name = :1", flyer_name)
        tempflyer = tempflyers[0]
        if choice == "toTrue":
            tempflyer.flag = True
            tempflyer.put()
        elif choice == "toFalse":
            tempflyer.flag = False
            tempflyer.put()
        else:
            tempflyer.delete()
        self.redirect('/admin')

class Points(webapp.RequestHandler):
    """
        Show the points
    """
    @requires_admin
    def get(self):
        # formate the date
        startdate = self.request.get("startdate")
        enddate = self.request.get("enddate")
        if startdate == None or startdate == '' or not matchdateformat(startdate):
            startdate = date.today()
        else:
            # format the startdate
            startdate = stringtodate(startdate)
        if enddate == None or enddate == '' or not matchdateformat(enddate):
            enddate = date.today() + datetime.timedelta(days = 1)
        else:
            # format the enddate
            enddate = stringtodate(enddate)
        markedpoints = db.GqlQuery ("SELECT * FROM MarkedPoint WHERE date > :1 AND date < :2 ORDER BY date DESC", startdate, enddate)
        template_values = {
            'startdate': startdate.strftime("%Y-%m-%d"),
            'enddate': enddate.strftime("%Y-%m-%d"),
            'flyer_name': 'admin', # because the base.html control the date_select's show or not
            'markedpoints': markedpoints,
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/points.html')
        self.response.out.write(template.render(path, template_values))

class Image(webapp.RequestHandler):
    """
        image for showing
    """
    def get(self, id):
        id = int(id)
        mp = MarkedPoint.get_by_id(id)
        image = mp.picblob
        self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.out.write(image)

application = webapp.WSGIApplication([
  ('/image/(?P<id>[0-9]+)/', Image),
  ('/mark', Mark),
  ('/mark_test', Mark_test),
  ('/marks', Marks),
  ('/points', Points),
  ('/', Index),
  ('/login', Login),
  ('/logout', Logout),
  ('/register', Flyer_register),
  ('/admin', Admin),
  ('.*', Error404),
], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
