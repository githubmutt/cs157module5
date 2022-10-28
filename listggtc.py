

import webapp2    # Python 2.7
import json   #Python 2.7

from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

import os,re,cgi,string,types
from  datetime import datetime,timedelta

import collections,time


from datastore import *

 
class GENERIC:
   def __init__ ( self,year, fname,lname,email, unix):
      self.year = year
      self.fname = fname
      self.lname = lname
      self.email   = email
      self.unix   = unix


class QUEUE(GENERIC):
      pass


def LOCALTIME( unix):

#    t = (2019,2,21,0,0,0,0,0 ,0 )

#    t = time.mktime(t)
#    print(time.strftime("%b %d", time.gmtime( t) ) )
#    print( time.strftime("%b %d %Y %I:%M %p", time.gmtime(t)  ))

     return time.strftime("%b %d %Y %I:%M %p", time.localtime( float(unix)  ))


     return "time"
#     return time.strftime("%b %d %Y %I:%M %p", time.localtime( unix - 7*60*60 ))


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
              g = GENERIC( key.year ,key.fname, key.lname ,key.address , key.city, key.email , key.ntrp , key.mtype, key.src, date_local , date_unix)
              MemberList.append(g)


        MemberList.sort(key=lambda x: x.lname, reverse=False)
        template_values = {
                         'TITLE'  :  "SCTC ROSTER",
                         'DIR'  :  "members",
                         'KOTOSHI'    :  SCTC_KOTOSHI,
                         'KYONEN'    :  SCTC_KOTOSHI-1,
                         'OTOTOSHI'  :  SCTC_KOTOSHI-2,
                         'MemberList' : MemberList
             }

        path = os.path.join(os.path.dirname(__file__), 'templates','members.html')
        self.response.out.write(template.render(path, template_values))

class EmailHandler( webapp2.RequestHandler):
     def get(self, id=None):

        YEAR=2019
        query = GGTC.query( GGTC.year >= YEAR) #.order(GGTC.lname)


        self.response.write( "fname, lname, email ,year <br>")

        MemberList=[]


        for key in query.iter():

           unix = key.key.id() 
#          self.response.write(unix )
#          self.response.write("<br>" )

           g = QUEUE( key.year ,key.fname , key.lname ,key.email,unix)


           MemberList.append(g)


#  SORT before ouput
#       MemberList.sort(key=lambda x: x.lname, reverse=False)
#       SORT by time-stamp  newest date and ascendding
        MemberList.sort(key=lambda x: x.unix, reverse=True)

#       MemberList.sort(key=lambda x: x.lname, reverse=False)

#       Change this if so desired - or just keep and catch anyone else (after March 6 )
        t = (2018,1,1,0,0,0,0,0 ,0 )  # Feb 21 is the last cut-off (RO)
        lastTime = int(time.mktime(t))

#       Not needed anymore --- this was to catch consecutive names  
        fname=lname=""
        count=1
        for m in MemberList:
           fname = fname.rstrip()
           lname = lname.rstrip()

           _name = fname+lname
           name_ = m.fname + m.lname

#          actual timestamp when player signed up
           berkeleyTime  =  LOCALTIME( m.unix)

#          if( _name != name_ ):
#          do the comparison


           if( int(m.unix) > int(lastTime)   ):
             self.response.write( m.fname + " , " + m.lname + " , " + m.email + " , " + str(count) + " , " + str(berkeleyTime)  +"<br>")  

#          not needed
           fname = m.fname
           lname = m.lname
           count = count + 1

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

                                      ('/emailsf', EmailHandler),
                                      ('/emailsf/([\d]*)', EmailHandler)


                                     ],
                                      debug=True)
