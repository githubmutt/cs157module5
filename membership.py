import webapp2

from google.appengine.ext.webapp import template

import os,re,datetime,sys, calendar,cgi,types

import logging

#from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import urlfetch

from google.appengine.ext import ndb

from datastore import  *

class User ( ndb.Model):
     id  = ndb.StringProperty()
     year = ndb.IntegerProperty()
     fname  = ndb.StringProperty()
     lname  = ndb.StringProperty()


class MembershipHandler(webapp2.RequestHandler):
    def get(self):
#        self.response.headers['Content-Type'] = 'text/html'


        template_values = {       }


#        template = JINJA.ENVIRONMENT.get_template('/templates/membership.html')
#        self.response.out.write( template.render() )

        path = os.path.join(os.path.dirname(__file__), 'templates','membership.html')
        self.response.out.write(template.render(path, template_values))


def Writeln(obj, t):
     obj.response.out.write( t)
     obj.response.out.write( "<br>")

class AcceptHandler(webapp2.RequestHandler):

    def Writeln(self, t):
     self.response.out.write( t + "<br>")


    def post(self):


     fname = cgi.escape(self.request.get('fname'))
     lname = cgi.escape(self.request.get('lname'))
     address = cgi.escape(self.request.get('address'))
     city    = cgi.escape(self.request.get('city'))
     zip    = cgi.escape(self.request.get('zip'))

     Writeln( self, fname )
     Writeln( self , lname )
     Writeln( self , address )
     Writeln( self, city )
     Writeln( self, zip )

     Writeln( self, "--------------"  )

     type    = cgi.escape(self.request.get('type'))
     Writeln( self, type )

#    Store into db ------------------

     year = 2018
  
     playerid = fname + "_" + lname + "_" + str(year )

     
     Writeln( self, playerid)
     logging.info(playerid)
     logging.debug(playerid)

     Writeln( self, "42 = " + str( PT42()  ) )

     p = User()
     p.id = playerid
     p.year = year
     p.fname = fname
     p.lname = lname

     self.response.out.write( p )
     self.response.out.write( "<br>")

     rafael = User( id = playerid , year = 2018, fname = "Rafael" , lname = "Nadal" )
     rafael_key = rafael.put()


#     playerKey = ndb.key(User , str(playerid ) )
#     g = Player.get_by_id( str(playerid) )
     return

     if( g != None):
        Writeln(self, "player exists ")
     else:
         g = datastore.Player( key=playerKey)
         g.fname = fname
         g.lname = lname
         g.city = city
         g.address = address
         g.zip = zip
#        g.put()

         Writeln(self, "player saved ")


# Enter a bunch of members
class MassEnterHandler(webapp2.RequestHandler):

    def get(self):

         print("max integer =  " + str(sys.maxint) )

         Player( year=2017,fname="Pamela",lname="Hoggatt",email="pnhoggatt@hotmail.com",ntrp="F3.0",address="3070 Dibble Court",city="Santa Clara",zip="95051",mtype="RF_",src="PP",id=1484025099).put()
         Player( year=2017,fname="Jacqueline",lname="Kerkhove",email="jkerkhove@gmail.com",ntrp="F4.5",address="755 Santa Paula Ave",city="Sunnyvale",zip="94085",mtype="NRS",src="PP",id=1484025099).put()
         Player( year=2017,fname="Saayaka",lname="Kishino",email="ksh_kishino@hotmail.com",ntrp="F4.5",address="1058 W Remington Dr",city="Sunnyvale",zip="94087",mtype="NRS",src="PP",id=1484102727).put()
         Player( year=2017,fname="Laura ",lname="Fletcher ",email="fletch4him1@mac.com",ntrp="F3.5",address="869 Hilmar Street",city="Santa Clara",zip="95050",mtype="RF",src="PP",id=1484298150).put()

         print("done ")


    def get_(self):
 
       dbList = []

       p = Player(  year = 2018, fname = "Novak" , lname = "Djokovic" , email="novak" , url="gmail.com"),

       dbList.append( p )
       p = Player(  year = 2017, fname = "Novak" , lname = "Djokovic" , email="novak" , url="gmail.com"),
       dbList.append( p )
       p = Player(  year = 2016, fname = "Novak" , lname = "Djokovic" , email="novak" , url="gmail.com"),
       dbList.append( p )

       dbList.put()


class MassEnterHandler_(webapp2.RequestHandler):

    def get(self):

     Player( year="2017",fname="Marie",lname="Fan",email="msfan00@yahoo.com",ntrp="F4.0",address="1297 Weibel Way",city="San Jose",zip="95125",mtype="NRS",src="PP",date="1483840366").put()
     Player( year="2017",fname="Valerie",lname="McCarthy",email="valeriebays@gmail.com",ntrp="F3.0",address="471 Tanoak Drive",city="Santa Clara",zip="95051",mtype="RS",src="PP",date="1480889910").put()


    def get_(self):

     dbList = []

     members = [

       Player(  year = 2018, fname = "Rafael" , lname = "Nadal" , email="Rafa" , url="gmail.com"),
       Player(  year = 2017, fname = "Rafael" , lname = "Nadal" , email="Rafa" , url="gmail.com"),
       Player(  year = 2016, fname = "Rafael" , lname = "Nadal" , email="Rafa" , url="gmail.com"),
       Player(  year = 2015, fname = "Rafael" , lname = "Nadal" , email="Rafa" , url="gmail.com"),

       Player(  year = 2018, fname = "Roger" , lname = "Federer" , email="roger" , url="gmail.com"),
       Player(  year = 2017, fname = "Roger" , lname = "Federer" , email="roger" , url="gmail.com"),
       Player(  year = 2015, fname = "Roger" , lname = "Federer" , email="roger" , url="gmail.com")
     ]


     for row in members:
        row.put() 
        Writeln(self, row)
        print row 



app = webapp2.WSGIApplication([
    ('/memb', MembershipHandler),
    ('/mass', MassEnterHandler),
    ('/accept', AcceptHandler)

], debug=True)

