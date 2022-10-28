import webapp2
import logging

import collections
import datetime,re, random,time

from google.appengine.ext import ndb
import json   #Python 2.7


import urllib2
from google.appengine.api import urlfetch

from datastore import  *

import urllib   # maybe not right , sleepy 9/26/19

import sc

# to send JSON dta to SCTC
#import requests # https://gist.github.com/thepacketgeek/6691361


def TABLE( obj)  :

 self = obj


 self.response.write("drop table SFO; <br>")

 self.response.write("  CREATE TABLE `SFO` (                 <br>" )
 self.response.write("  `_id` int(10) NOT NULL AUTO_INCREMENT,                 <br>")
 self.response.write("  `year` int(10) DEFAULT NULL,                 <br>")
 self.response.write("  `fname` varchar(31) DEFAULT NULL,                 <br>" )
 self.response.write("  `lname` varchar(31) DEFAULT NULL,                 <br>" )
 self.response.write("  `address` varchar(31) DEFAULT NULL,                 <br>" )
 self.response.write("  `city` varchar(31) DEFAULT NULL,                 <br>" )
 self.response.write("  `zip` varchar(31) DEFAULT NULL,                 <br>" )
 self.response.write("  `email` varchar(31) DEFAULT NULL,                 <br>" )
 self.response.write("  `phone` varchar(31) DEFAULT NULL,                 <br>" )
 self.response.write("  `ntrp` varchar(31) DEFAULT NULL,                 <br>" )
 self.response.write("  `src` varchar(31) DEFAULT NULL,                 <br>" )
 self.response.write("  `help` varchar(31) DEFAULT NULL,                 <br>")
 self.response.write("  `other` varchar(31) DEFAULT NULL,                 <br>")
 self.response.write("  `ip` varchar(31) DEFAULT NULL,                 <br>")
 self.response.write("  `unix` varchar(31) DEFAULT NULL,                 <br>")

 self.response.write("  PRIMARY KEY (`_id`)                 <br>")
 self.response.write(");                 <br>")


def Q( r ):

     if r == None: r=""

     return '"' + str(r) + '", '

# bring in db from SF

class  JSON_FROM_SCTCHandler( webapp2.RequestHandler):
   def get (self ):
      url =  "http://www.sctennisclub.org/membership/json"
      response = urllib.urlopen(url)
      data = json.loads(response.read() )

      for d in data:
        print( d )
        self.response.write( d )
        self.response.write("<br>")
        date = d['date']
        m = MEMBER(key=ndb.Key( MEMBER , str( date ) ))
        m.year = d['year']
        m.fname = d['fname']
        m.lname = d['lname']
        m.address = d['address']
        m.city = d['city']
        m.zip = d['zip']
        m.ntrp = d['gender']+d['ntrp']

        m.email = d['email']+ "@" + d['url']

        m.mtype = d['mtype']
        m.zknt = 0
        m.ztra = ""

        m.put();

class ConvertHandler(webapp2.RequestHandler):
   def get (self ):
        self.response.write("Convert Handler <br>")
        query = ndb.gql("select * from GGTC order by -__key__ ")
        result = query.fetch(10)
        for q in result:
          _UNIX = int(  q.key.id()  )
          self.response.write( str(_UNIX) + " " + q.fname + " " + q.lname + "<br>")      


   def _get (self ):

        self.response.write("Convert Handler <br>")
        query = GGTC.query()
        query = query.filter(GGTC.year == 2019)
        q_reverse = query.order( -GGTC.key)

        self.response.write("Last 10 Members <br>" )
        r = q_reverse.fetch(10)
        for q in r:
          _UNIX = int(  q.key.id()  )
          self.response.write( str(_UNIX) + " "  + q.fname + " " + q.lname  + "<br>")      

        return


#        for q in result:
#          _UNIX = int(  q.key.id()  )
#          self.response.write( str(_UNIX) + " " + q.fname + " " + q.lname + "<br>")      

class JSONHandler(webapp2.RequestHandler):
   def get (self ):

#     URL to get JSON data

      url =  "http://www.sfmongoldata.appspot.com/short"
#     result = urlfetch.fetch(url)
#     scraped = result.content
#     self.response.write( scraped )


#      j = json.loads( scraped )

      response = urllib.urlopen(url)
      data = json.loads(response.read() )

#     print data
      for m in data:

       fname = m['fname']
       lname = m['lname']
       year  = m['year']
       address = m['address']
       city    = m['city']
       email   = m['email']
       url    =  m['url']
       zip     = m['zip']
       phone   = m['phone']
       ntrp    = m['ntrp']

       ip     = m['ip']

       date    = m['date']
       src     = m['src']
       other   = m['other']
       help    = m['help']


       D =  str(year) + "/" + str(date) + " : " + fname + " " + lname  + " " + address + " " + city + " " + zip + " " + phone + "  " + ntrp 
       D = D + " " + email + " <-> " + url 
       D = D + " " + ip + " " + str(src) + " " + str(other) + " " + str(help)


#      self.response.write( D + "<br>" )

#      m = GGTC(key=ndb.Key( GGTC , str( date ) ))
       m = MEMBER(key=ndb.Key( MEMBER , str( date ) ))
       m.fname = fname
       m.lname = lname
       m.address = address
       m.city = city
       m.zip  = zip

       m.year = year
       m.email = email + " @ " + url + " <----"

       print m.email  + "<--------"
       self.response( m.email + "  < ---------- ")

       m.phone = phone
       m.ntrp = ntrp
       m.ip = ip

       m.help = help
       m.other = other

#  if MEMBER class (SCTC)
       m.mtype = "RF"
       m.zknt = 0
       m.ztra = "Z"


       m.put()


       date = datetime.datetime.now() 
       date = date.strftime('%s')


       m = PENDING(key=ndb.Key( PENDING , str( date ) ))
       m.fname = "Roger"
       m.lname = "Okamoto"
       m.address = "1233 Sierra Ave"
       m.city = "San Jose"
       m.zip  = "95126"
       m.year = 2019
       m.ntrp = "M3.5"
       m.email = m.phone = m.ip = ""
#       m.put()

       date  = datetime.datetime.now() 
       date = date.strftime('%s')
       m = WAIT(key=ndb.Key( WAIT , str( date ) ))
       m.fname = "Roger"
       m.lname = "Okamoto"
       m.address = "1233 Sierra Ave"
       m.city = "San Jose"
       m.zip  = "95126"
       m.year = 2019
       m.ntrp = "M3.5"
       m.email = m.phone = m.ip = ""
#       m.put()


class GAEDumpHandler(webapp2.RequestHandler):
   def get (self ):
         self.response.write("# SFO -> GAE Dump  Handler <br>")
         YEAR = 2019

#        q = GGTC.query(GGTC.year = 2019 , GGTC.lname > "O" )
#        q1 = GGTC.query( GGTC.lname > "B" , GGTC.lname < "O" , GGTC.key )

         
#         q2 = GGTC.query().order(GGTC.lname, -GGTC.fname)
         q = GGTC.query()
         q = q.filter( GGTC.year == 2019 )

         q = q.order( -GGTC.key  )

         results  = q.fetch(15)

         obj=[]
         SPACE = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
         self.response.write( SPACE + "sfo=[]<br>" )
         for key in results:

             year  = str(key.year)
             fname = key.fname 
             lname = key.lname
             address = key.address
             city    = key.city
             email   = key.email
             zip     = str(key.zip)
             phone   = key.phone
             ntrp    = key.ntrp
             _id = int(  key.key.id()  )

             self.response.write( "sfo.append(GGTC( " )

             p = GGTC(
               id = key.key.id(),
               year = 2021,
               fname = key.fname,
               lname = key.lname,
               address = key.address,
               city = key.city,
               zip = key.zip,
               phone = key.phone,
               email = key.email,
               ntrp = key.ntrp,
               src = key.src,
               help = key.help,

               other = key.other,
               ip = key.ip

             )
             obj.append( p )
             self.response.write( "(" + str(_id) + ","  + Q(year) + Q(fname)  + Q(lname)  +  Q(address) )   
             self.response.write(  Q(city)  + Q(email)  + Q(zip) )   

             self.response.write( ")<br>" )   


         self.response.write( obj )
         r = ndb.put_multi( obj )

         self.response.write( "<p> results <p> ")
         self.response.write( r )

class MYSQLDumpHandler(webapp2.RequestHandler):
# Write to a file 
   def get (self ):

         self.response.write("SFO -> MYSQL t Handler <br>")
         YEAR = 2019
         q = GGTC.query()
         q = q.filter( GGTC.year == 2019 )         
         q = q.order( -GGTC.key )         
         results = q.fetch(20)


         TABLE( self )

         self.response.write("insert into SFO ( year, fname, lname, address,city,zip ,email, phone, ntrp, help, other, ip,unix) <br>")
         self.response.write("values  <br>")      

         for k in results:

            fname = k.fname
            lname = k.lname
            addr = k.address
            city  = k.city
            email = k.email
            zip   =  k.zip
            phone = k.phone
            ntrp  = k.ntrp

            help  = k.help
            other = k.other
            ip    = k.ip


            self.response.write( '(' )

            unix = k.key.id()  

            self.response.write(  Q(YEAR) +  Q(fname)  + Q(lname) + Q(addr)  +  Q(city) + Q(zip) + Q(email)  + Q(phone) + Q(ntrp) + Q(help) + Q(other) + Q(ip) )
            self.response.write( '"' + str(unix) + '"' )

            self.response.write( "), <br>")

def createJSON( self, result ):

         obj = []
         for key in result:

#             d={}   # must be new dictionary, otherwise just last one counts
             d=collections.OrderedDict()    # must be new dictionary, otherwise just last one counts


             d['year']= key.year
             d['fname']= key.fname 
             d['lname']= key.lname
             d['address']= key.address
             d['city']= key.city
             d['email']= key.email
             d['zip']= key.zip
             d['phone']= key.phone
             d['ntrp']= key.ntrp

             d['src']= key.src
             d['help']= key.help
             d['other']= key.other
             d['ip']= key.ip

             dt = int(  key.key.id()  )
             d['date']= dt


             obj.append(d)

#        payload = sorted( obj , key = lambda k: k['date'], reverse=True)
#        j=json.dumps( payload )
         j=json.dumps( obj )

         return j




def getJSON( self ,result) :


         obj = []
         for key in result:

#             d={}   # must be new dictionary, otherwise just last one counts
             d=collections.OrderedDict()    # must be new dictionary, otherwise just last one counts


             d['year']= key.year
             d['fname']= key.fname 
             d['lname']= key.lname
             d['address']= key.address
             d['city']= key.city
             d['email']= key.email
             d['zip']= key.zip
             d['phone']= key.phone
             d['ntrp']= key.ntrp

             d['src']= key.src
             d['help']= key.help
             d['other']= key.other
             d['ip']= key.ip

             dt = int(  key.key.id()  )
             d['date']= dt


             obj.append(d)

#        payload = sorted( obj , key = lambda k: k['date'], reverse=True)
#        j=json.dumps( payload )
         j=json.dumps( obj )
         self.response.write( j )

class ReadSFDataHandler(webapp2.RequestHandler):
   def get (self ):

      self.response.write("ReadSFDataHandler")
      url =  "http://www.sfmongoldata.appspot.com/datasf"
      response = urllib.urlopen(url)
      data = json.loads(response.read() )
      for m in data:

       fname = m['fname']
       lname = m['lname']
       year  = m['year']
       address = m['address']
       city    = m['city']
       email   = m['email']
       url    =  m['url']
       zip     = m['zip']
       phone   = m['phone']
       ntrp    = m['ntrp']

       ip     = m['ip']

       date    = m['date']
       src     = m['src']
       other   = m['other']
       help    = m['help']


       D =  str(year) + "/" + str(date) + " : " + fname + " " + lname  + " " + address + " " + city + " " + zip + " " + phone + "  " + ntrp 
       D = D + " " + email + " <-> " + url 
       D = D + " " + ip + " " + str(src) + " " + str(other) + " " + str(help)


       self.response.write( D + "<br>" )

       m = GGTC(key=ndb.Key( GGTC , str( date ) ))
       m.fname = fname
       m.lname = lname
       m.address = address
       m.city = city
       m.zip  = zip

       m.year = year
       m.email = email + " @ " + url + " <----"

       m.phone = phone
       m.ntrp = ntrp
       m.ip = ip

       m.help = help
       m.other = other

#      m.put()


class SFDataHandler(webapp2.RequestHandler):
   def get (self ):
         YEAR = 2019
         query = GGTC.query( )
         query = query.filter( GGTC.year == YEAR)
         query = query.filter( GGTC.lname > "P")
         query = query.order(  GGTC.lname)

#         query = query.filter( GGTC.lname < "D")
#        query = query.order( GGTC.lname)
         result = query.fetch(20)

         getJSON ( self, result)

def QUOTE( r):
     return "' "+ r + "'"

class SendToSCTCHandler(webapp2.RequestHandler):
   def get (self ):

#    sc.sendtosantaclara(self, 2017,23232,"Naomi H","Osaka","2300 Birch Lane ","Miami,FL", "naomi.osaka@wta.com", "W8.0", 94023 ,"(408) 232-3223")

# THIS USES LIBRARY TO SEND TO SCTENNISCLUB.ORG
     sc.sendtosantaclara(self, 2017,1001,"Sheena","Lee","300 Geary Blvd","San Francisco", "sheena.leea@gmaila.com", "W3.0", 94121 ,"(415) 933-1114")

# THIS USES LIBRARY TO SEND TO SCTENNISCLUB.ORG

class SendLastHandler(webapp2.RequestHandler):
   def get (self ):
#         YEAR = 2018
#         query = GGTC.query( )
#         query = query.filter( GGTC.year == YEAR)
#         query = query.order( -GGTC.key)
#        result = query.fetch(1)

#        obj = []
#         print( result )
#         print( dir(result) )
         obj.append( d )
         #print( d )
         jds = json.dumps( obj )         
         self.response.headers['Content-Type'] = 'application/json'
         self.response.write( jds)



         url = "http://www.sctennisclub.org/accept/accept.php"
         url = "http://localhost/~roger/sc/accept/accept.php"


         req = urllib2.Request( url )

         return

         req.add_header('Content-Type', 'application/json')
         
         data = createJSON( self, result )

         print( json.dumps(data) )
         response = urllib2.urlopen( req, json.dumps(data)  )        

         print "*"*45 + "<br>"
         print response
         print "*"*45 + "<br>"


#         urllib2.urlopen( url , urllib.urlencode( json  ) )

#        getJSON ( self, result)

class ShortHandler(webapp2.RequestHandler):
   def get (self ):

         YEAR = 2019
         query = GGTC.query( )
         query = query.filter( GGTC.year == YEAR)
         query = query.order( -GGTC.key)
         result = query.fetch(10)

         getJSON ( self, result)

class LongHandler(webapp2.RequestHandler):
   def get (self ):
         YEAR = 2019
         query = GGTC.query( )
         query = query.filter( GGTC.year == YEAR)
         query = query.order( GGTC.lname)
         result = query.fetch(20)
 
         getJSON ( self, result)

class RedirectHandler(webapp2.RequestHandler):
   def get (self ):

      url = "http://www.sctennisclub.org"
      url = "www.sctennisclub.org/accept/json.php";


      url = "http://www.sctennisclub.org/accept/current";

      self.redirect(url);


app = webapp2.WSGIApplication(
                                     [

#                                     ('/convert', ConvertHandler),
                                      ('/convert', JSONHandler),    # bring in db from SF

                                      ('/fromsctc', JSON_FROM_SCTCHandler),    # bring in db from SF

                                      ('/dump1', GAEDumpHandler),
                                      ('/dump2', MYSQLDumpHandler),

# ---------------------------------------- 
                                      ('/sendlast', SendLastHandler),

                                      ('/sendsctc', SendToSCTCHandler),



                                      ('/redirect', RedirectHandler),


# ----------------------------------

                                      ('/sfdata', SFDataHandler),
                                      ('/readsf', ReadSFDataHandler),

# get either last 10 or everyone
                                      ('/short', ShortHandler),
                                      ('/long', LongHandler)



                                     ],
                                     debug=True)

