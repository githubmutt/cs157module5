

import webapp2    # Python 2.7
import json   #Python 2.7

from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

import os,re,cgi,string,types
from  datetime import datetime,timedelta

import collections


from datastore import *

 
class GENERIC:
   def __init__ ( self,year, fname,lname,address,city,email, ntrp,mtype,src, unix,date ):
      self.year = year
      self.fname = fname
      self.lname = lname
      self.address = address
      self.city = city
      self.email   = email
      self.ntrp    = ntrp
      self.mtype    = mtype
      self.src    = src
      self.date    = date
      self.unix    = unix

class QUEUE(GENERIC):
      pass


def  Abbreviate( city ):

             if( re.search("clara",city, re.IGNORECASE)): city = "SC"
             elif( re.search("jose", city, re.IGNORECASE)): city ="SJ"
             elif( re.search("mountain", city, re.IGNORECASE)): city ="MV"
             elif( re.search("sunny", city, re.IGNORECASE)): city ="SU"
             elif( re.search("altos", city, re.IGNORECASE)): city ="LA"
             elif( re.search("altos", city, re.IGNORECASE)): city ="LA"
             elif( re.search("cup", city, re.IGNORECASE)): city ="CU"
             elif( re.search("monte", city, re.IGNORECASE)): city ="MS"
             elif( re.search("milpitas", city, re.IGNORECASE)): city ="MP"
             elif( re.search("redwood", city, re.IGNORECASE)): city ="RWC"
             elif( re.search("fremont", city, re.IGNORECASE)): city ="FMT"
             elif( re.search("scotts", city, re.IGNORECASE)): city ="SV"
             elif( re.search("gato", city, re.IGNORECASE)): city ="LG"

             elif( re.search("campb", city, re.IGNORECASE)): city ="CMB"

             elif( re.search("millbrae", city, re.IGNORECASE)): city ="MilB"

             elif( re.search("menlo", city, re.IGNORECASE)): city ="MPk"
             elif( re.search("belmont", city, re.IGNORECASE)): city ="Belm"
             elif( re.search("saratoga", city, re.IGNORECASE)): city ="SRT"
             elif( re.search("palo", city, re.IGNORECASE)): city ="PA"

             elif( re.search("dublin", city, re.IGNORECASE)): city ="DB"
             elif( re.search("morgan", city, re.IGNORECASE)): city ="MH"

             elif( re.search("cameron", city, re.IGNORECASE)): city ="CPk"

             elif( re.search("bruno", city, re.IGNORECASE)): city ="SB"

             elif( re.search("burling", city, re.IGNORECASE)): city ="BG"

             return city


class MemberHandler( webapp2.RequestHandler):
     def get(self, id=None):

        YEAR=SCTC_KOTOSHI
        if id != None :
         YEAR = int(id)

        print( "YEAR = " + str(YEAR)  )


        query = MEMBER.query( MEMBER.year == YEAR) #.order(Member.lname)

        obj = []
        d=collections.OrderedDict()

        MemberList = []

#             print( key.key.id()  )
#            the keyID is the date signed up
#            t = datetime.datetime.fromtimestamp( key.key.id()) + timedelta(hours=5)
#            dt = t.strftime("%Y-%m-%d %H:%M:%S")
#            print( str(g.year) + " " + g.fname + " " + g.lname )


        for key in query.iter():

              date_unix = int(key.key.id() )

              t = datetime.datetime.fromtimestamp( date_unix  ) + timedelta(hours=5)
              date_local = t.strftime("%m-%d %Y")

              city = Abbreviate(key.city)
              g = GENERIC( key.year ,key.fname, key.lname ,key.address , city, key.email , key.ntrp , key.mtype, key.src, date_local , date_unix)
              MemberList.append(g)


        MemberList.sort(key=lambda x: x.lname, reverse=False)
        template_values = {
                         'TITLE'  :  "SCTC ROSTER",
                         'DIR'  :  "members",
                         'KOTOSHI'    :  SCTC_KOTOSHI,
                         'KYONEN'    :  SCTC_KOTOSHI-1,
                         'OTOTOSHI'  :  SCTC_KOTOSHI-2,

                         'COLOR_STRIP'      :  "#ffccff",
                         'COLOR_SCTC'      :  "#ffccff",

                         'MemberList' : MemberList





             }

        path = os.path.join(os.path.dirname(__file__), 'templates','members.html')
        self.response.out.write(template.render(path, template_values))

class EmailHandler( webapp2.RequestHandler):
     def get(self, id=None):
        pass



class QueueHandler( webapp2.RequestHandler):
     def get(self, id=None):

        YEAR=2018
        if id != None :
         YEAR = int(id)

        query = PENDING.query( PENDING.year == YEAR)
        obj = []
        d=collections.OrderedDict()

        MemberList = []
        for key in query.iter():

             print( key.key.id()  )
#            the keyID is the date signed up
             t = int( key.key.id())
             date_unix = datetime.datetime.fromtimestamp( t  ) + timedelta(hours=-7)

             date_local = date_unix.strftime("%%m-%d-%Y %H:%M:%S")
             date_local = date_unix.strftime("%H:%M %m-%d-%Y")
             RES = "<sup>&#149;</sup>"; 

             RES = "*"
#             g = QUEUE( key.year ,key.fname+RES, key.lname ,key.address , key.city, key.email , key.ntrp , key.mtype, key.src,dt+RES)
             g = QUEUE( key.year ,key.fname , key.lname ,key.address , key.city, key.email , key.ntrp , key.mtype, key.src, t , date_local+RES)
             MemberList.append(g)

        MemberList.sort(key=lambda x: x.unix, reverse=True)
        template_values = {
                         'TITLE'  :  "SCTC PENDING QUEUE",
                         'DIR'  :  "queue",
                         'OTOTOSHI'  :  2016,
                         'KYONEN'    :  2017,
                         'KOTOSHI'    :  2018,
                         'MemberList' : MemberList
             }

        path = os.path.join(os.path.dirname(__file__), 'templates','members.html')
        self.response.out.write(template.render(path, template_values))





class PendingHandler( webapp2.RequestHandler):
     def get(self, id=None):


        YEAR=2018
        if id != None :
         YEAR = int(id)

        query = PENDING.query( PENDING.year == YEAR)
        obj = []
        d=collections.OrderedDict()

        MemberList = []
        for key in query.iter():

#            t = datetime.datetime.fromtimestamp( key.date) + timedelta(hours=5)
             t = int( key.key.id() )
             t = datetime.datetime.fromtimestamp( t) + timedelta(hours=5)
             dt = t.strftime("%Y-%m-%d %H:%M:%S")

             RES = ""; 
             if( key.done == "done"):
                 RES = "*"; 

             g = GENERIC( key.year ,key.fname, key.lname ,key.address , key.city, key.email , key.ntrp ,key.mtype, key.src ,dt+RES )
             MemberList.append(g)


        MemberList.sort(key=lambda x: x.fname, reverse=True)
        template_values = {
                         'TITLE'  :  "SCTC ROSTER (Pending members)",
                         'DIR'  :  "pending",
                         'OTOTOSHI'  :  2016,
                         'KYONEN'    :  2017,
                         'KOTOSHI'    :  2018,
                         'MemberList' : MemberList
             }

        path = os.path.join(os.path.dirname(__file__), 'templates','members.html')
        self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication(
                                     [
                                      ('/members', MemberHandler),
                                      ('/members/([\d]*)', MemberHandler),

                                      ('/queue', QueueHandler),
                                      ('/queue/([\d]*)', QueueHandler),

                                      ('/email', EmailHandler),
                                      ('/email/([\d]*)', EmailHandler),


                                      ('/plist', PendingHandler),
                                      ('/plist/([\d]*)', PendingHandler),


                                     ],
                                      debug=True)
