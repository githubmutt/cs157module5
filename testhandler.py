import webapp2
import logging

import collections,time
import datetime,re,os

#import requests,idna,urllib3,certifi, chardet
#import requests_toolbelt.adapters.appengine
#import httplib,urllib

from google.appengine.ext import ndb
import json   #Python 2.7

from datastore import  *

# to fix cupertinoustateams   *******
from google.appengine.api import urlfetch
# to fix cupertinoustateams   *******

def LOCALTIME( unix):
      return time.strftime("%D ", time.localtime( unix - 7*60*60 ))


# Club Day bug
class TestHandler( webapp2.RequestHandler):

   def get(self):
      print("TestHandler")

      YEAR=2019
      query = CLUBDAY.query( CLUBDAY.fname != "" )
      for key in query.iter():
           unix = int( key.key.id( ))
           self.response.write( key.fname )

#          g = G(  key.fname, key.lname, key.email, key.gender, key.ntrp, key.member, unix ,key.potluck)


      return



class TestHandler_8(webapp2.RequestHandler):

   def post(self):
       print("TestHandler (POST)" )
       jdata = json.loads(self.request.body)

       print(" ******** " )
       print( jdata['year'] )
       print(" ******** " )

       self.result( jdata['year'] )

   def result( self, YEAR):
       print("RESULT: year = " + str(YEAR) );
       query = GGTC.query( GGTC.year == YEAR)
       obj = []
       for key in query.iter():
             d=collections.OrderedDict()    # must be new dictionary, otherwise just last one counts
             d['year']= key.year
             d['fname']= key.fname 
             d['lname']= key.lname
             obj.append(d)

       payload = sorted( obj , key = lambda k: k['lname'])
       j=json.dumps( payload )

       print( j )
       self.response.write( j )

   def get(self):

#       self.response.write( dir(os.environ) )

       self.response.write( os.environ["HTTP_HOST"] )

       self.response.write( "<p><br>")
       self.response.write( "<p><br>")

#      self.response.write( os.environ )


class TestHandler__(webapp2.RequestHandler):

   def get(self):
         print("TestHandler --- GET")
         idx = "113"   # Cupertino Sports Center
         url = "https://www.ustanorcal.com/organization.asp?id=" + idx

         url = "https://www.ustanorcal.com/organization.asp?id=113"

         url = "https://www.sfgate.com"
         url = "https://www.marthastewart.com/"
         url = "https://www.ustanorcal.com/playermatches.asp?id=100472"


         try:
            result = urlfetch.fetch(url)
            print("OK for " + url )
            if result.status_code == 200:
                self.response.write( result.content)
            else:
                self.response.status_code = result.status_code
         except urlfetch.Error:
            logging.exception("caught exception fetching url ")


#         result = urlfetch.fetch(url)
#         scraped = result.content
         pass


   def post(self):
      data = json.loads(self.request.body)
      print( data )      
      self.result( data )

   def result(self, data ):
      print("result " )

      YEAR = int(  data["year"] )

      query = Member.query( Member.year == YEAR).order(Member.lname)
      obj = []


      for key in query.iter(limit=3):

             d=collections.OrderedDict()    # must be new dictionary, otherwise just last one counts

             d['year']= key.year
             d['fname']= key.fname
             d['lname']= key.lname
             d['address']= key.address
             d['city']= key.city
             d['email']= key.email
             d['mtype']=   key.mtype
             d['date']=   int(key.key.id())
             obj.append(d)

# DUMP JSON data 

      jds=json.dumps(obj)

      payload1 = { "residents" : 123  }
      payload2 = { "nonresidents": 120 }

      print( payload1)
      print( payload2)
      print( obj)

      self.response.headers['Content-Type'] = 'application/json'

      self.response.write( payload1  )
#      self.response.write( payload2  )
#      self.response.write( jds  )

def TRASHER( g):

      print(" TRASHER " )
      unix = g.key.id()

      print("unix = " + str( unix )  )

      trashKey = ndb.Key(TRASH,str(unix))
      t = TRASH( key = trashKey)

      t.year = g.year
      t.fname = g.fname
      t.lname = g.lname
      t.address = g.address
      t.city = g.city
      t.zip = g.zip
      t.phone = g.phone
      t.email= g.email
      t.ntrp = g.ntrp

      t.mtype= " "    # g.mtype
      t.src  = " "    # g.src
      t.mtype = " "   # g.mtype
      t.zknt = 0   # g.zknt
      t.ztra = "  "   # g.ztra


      print( " this is the trash object ")
      print(  t )
      print( "*"*25)

      # ADD the trashcan object
      print( t.put()  )

      # Delete the original object
      print("* "*5+" ENTITY KEY "+ "* "*16 )
      sourceKEY = g._entity_key
      print( sourceKEY  )      
#     print( dir(g )  )
      print("-"*32)

      print(" deleting ... " )
      print( sourceKEY.delete() )
      print(" done ... " )




def TRASHCAN( sourceKEY):

      print( sourceKEY )
      g =  sourceKEY.get()

      print( "Deleting " + str(g) ) 

      unix = g.key.id() 
      print( unix )

      trashKey = ndb.Key(TRASH,str(unix))
      t = TRASH( key = trashKey)
      t.year = g.year

      t.fname = g.fname
      t.lname = g.lname
      t.address = g.address
      t.city = g.city
      t.zip = g.zip
      t.phone = g.phone
      t.email= g.email
      t.ntrp = g.ntrp

      t.mtype= " "    # g.mtype
      t.src  = " "    # g.src
      t.mtype = " "   # g.mtype
      t.zknt = 0   # g.zknt
      t.ztra = "  "   # g.ztra

      print("deleting " )
      print( sourceKEY )

      print( sourceKEY.delete()  )

      print("putting into trash can" )
      print( t.put()  )


app = webapp2.WSGIApplication(
                                     [

                                      ('/test', TestHandler)      

                                     ],
                                     debug=True)
