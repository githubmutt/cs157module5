import webapp2
import logging

import collections,time
import datetime,re,os,cgi,string,types

from google.appengine.ext import ndb
import json   #Python 2.7

from datastore import  *

from google.appengine.ext import db

from google.appengine.ext.webapp import template

import data

# module to send data to sctennisclub.org
# call sc.sendtosantaclara(self,year, unix, fname, lname, address, city, email, ntrp, zip, phone  ):
from sc import *

# UPDATING INSTRUCTIONS one file each on GAE/PAIR side
# on GAE side
#  datastore.py    Change GGTC_KOTOSHI

# on PHP side
#  environment.inc change KOTOSHI
#   glist.php   change thee lines
#<a style="text-decoration:none; font-size:19px;" onclick=JYEAR(2019) >2019</a>
#&nbsp;
#<a style="text-decoration:none; font-size:20px;" onclick=JYEAR(2020) >2020</a>


# bigwilly
# Subtact 7 hours
# https://timestamp.online/article/how-to-convert-timestamp-to-datetime-in-python
def LOCALTIME( unix):
      return time.strftime("%b %d %Y %I:%M %p", time.localtime( unix - 7*60*60 ))


# Handle a post of a year, then return members of that year
# for GGTC just have to worry about Members (no Pending,Wait)
def DEBUG(sobj, text):
      pass
#     sobj.response.write( text )
#     sobj.response.write( "<br>" )


def ERROR(sobj, text):
     sobj.response.write( "<center>")
     sobj.response.write( "<h2>")
     sobj.response.write( text )
     sobj.response.write("<br>")
     sobj.response.write( "</h2>")
     sobj.response.write( "</center>")


def TRASHCAN( sourceKEY):
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

      print( sourceKEY.delete()  )
      print( t.put()  )



# GGTC Membership  -- keep separate from SCTC to prevent accidental clashing
class PurgeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("PurgeHandler <br>")
        YEAR=2019


#        db.delete(GGTC.query(GGTC.year == YEAR )  )
#        ndb.Model.query(GGTC.year == YEAR).deleteAll()

        query = GGTC.query( GGTC.year == YEAR)
        count=1
        for key in query.iter():
            self.response.write( key.fname + " " + key.lname + "  ")
            self.response.write( key.key.delete())
            self.response.write( "     ")
            if count%5 == 0:
              self.response.write( "<br>")

            count = count + 1
#            self.response.write( key.key)
#            self.response.write( dir(key.key)    )
#            self.response.write( dir(key)    )


# GET members for current year
class GetGGTCHandler(webapp2.RequestHandler):

    def get(self,id=None):

         YEAR = GGTC_KOTOSHI-1;
         if( id == "previous"):
            YEAR =  GGTC_KOTOSHI-1
         elif(id == "past"):
            YEAR =  GGTC_KOTOSHI-2

       
         print("GetGGTCHandler for " + str(YEAR) )
         print("id =  " + id )

         query = GGTC.query( GGTC.year >= YEAR)
         obj = []
         for key in query.iter():

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

             print("\n " );
             print("\n " );
             print("\n " );
             print( dir ( key.key.id ) )
             print( key.key.id )
             print( key.key.id()  )
             dt = int(  key.key.id()  )
             d['date']= dt


#             d['date'] = datetime.datetime.now() 

             obj.append(d)

# SORT by lname ( last name )
#        payload = sorted( obj , key = lambda k: k['lname'])
         payload = sorted( obj , key = lambda k: k['date'], reverse=True)

#DUMP JSON DATA
         j=json.dumps( payload )
#        j=json.dumps( obj )

#         self.response.headers['Content-Type'] = 'application/json'
#         self.response.send_header("Access-Control-Allow-Origin", "*")
#         self.response.write("Access-Control-Allow-Origin *")


#         self.response.write("Access-Control-Allow-Origin: *\r\n")
#         self.response.write( "Content-Type: application/json\r\r\n\n")

# https://stackoverflow.com/questions/46111354/set-header-access-control-allow-origin-with-python-print


#         print("Access-Control-Allow-Origin: *\r\n")
#         print( "Content-Type: application/json\r\n\r\n")
# https://stackoverflow.com/questions/31212992/how-to-enable-cors-on-google-app-engine-python-server
         self.response.headers['Access-Control-Allow-Origin']  = '*';
         self.response.write( j )



# THIS IS THE ULTIMATE ONE
# post a year and get that year's members
# unknown if this actually works!
class GGTCHandler(webapp2.RequestHandler):

# Receive JSON POST (just the year )
    def post(self):

         print("received POST ")
         print self.request.body

         j = json.loads(self.request.body)

         self.result( j )


    def result(self , jdata):

         YEAR = jdata['year']
         print("GGTC membership data for " +  str(YEAR)   )

         query = GGTC.query( GGTC.year == YEAR)
         keys = GGTC.query( GGTC.year == YEAR )

         obj = []

         for k in keys:
#            unix = int( k.id() )
             print k.key.id(), k.year, k.fname,k.lname,k.address



# https://cloud.google.com/appengine/docs/standard/python/ndb/queries
         for k in keys:

             d=collections.OrderedDict()    # must be new dictionary, otherwise just last one counts

             d['year']= k.year
             d['fname']= k.fname 
             d['lname']= k.lname
             d['address']= k.address
             d['city']= k.city
             d['email']= k.email
             d['zip']= k.zip
             d['phone']= k.phone
             d['ntrp']= k.ntrp
             unix = k.key.id()  # key.unix
             d['date']= unix    # key.unix
             obj.append(d)

# SORT by lname ( last name )
         payload = sorted( obj , key = lambda k: k['lname'])

         print("POST -> result \n")
#         for key in obj2:
#           print key 
#           print "\n"

         jds=json.dumps( payload )

         print( "-"*45 )
         print( payload )
         print( jds )
         print( "-"*45 )


         self.response.headers['Content-Type'] = 'application/json'
         self.response.write( jds )
#        return j

class AdminHandler(webapp2.RequestHandler):
     def get(self, id=None):

        YEAR=GGTC_KOTOSHI
        if id != None :
         YEAR = int(id)

# PUT TIME CONSTRAINT SO NOT EVERY TWILIGHT PERSON SHOWS UP (people who don't complete  membership signup) 
        minute = 60
        hour =   60*minute
        day =   24*hour
        month = 30*day
        year  = 12*month

        unix_now = int( time.time() )
        unix_before = unix_now - 24*hour

        print("*"*30)
        print( "YEAR = " + str(YEAR)  )
        print( unix_now ,unix_before)
        print("NOW = " +   LOCALTIME(unix_now)   )
        print("CUT OFF = " +   LOCALTIME( unix_before )  )
        print("*"*30)


# Get TWILIGHT Members
        keys = TWILIGHT.query( TWILIGHT.year == YEAR, TWILIGHT.done != "done").fetch(keys_only = True)
#       q = q.order( -GGTC.key  )
#       obj = []
#       d=collections.OrderedDict()
        TwilightList = []


        for k in keys:
          if( int(k.id()) > unix_before):
               p = TWILIGHT.get_by_id( k.id () )
#              print( "Twilight(" + str(k.id()) + ") " + p.fname + " " + p.lname + " " + str(p.ip)  )
               unix = int( k.id() ) 
      
               g = GENUSSF(p.year ,p.fname, p.lname , p.address , p.city, p.zip, p.email , p.phone, p.ntrp , p.help, p.other, p.ip,unix ,LOCALTIME(unix) )
               TwilightList.append(g)


        TwilightList.sort(key=lambda x: x.unix, reverse=True)



# Get GGTC Members 
        query = GGTC.query( GGTC.year == YEAR)
        query = query.order( GGTC.lname)

        MemberList = []
        for key in query.iter():
           unix = int( key.key.id() )
           g = GENUSSF( key.year ,key.fname, key.lname ,key.address , key.city,key.zip, key.email ,key.phone, key.ntrp , key.help, key.other, key.ip, unix ,LOCALTIME(unix) )
           MemberList.append( g)


#       MemberList.sort(key=lambda x: x.lname, reverse=False)

        SERVER = os.environ["HTTP_HOST"] 

        template_values = {
                         'TITLE'  :  SERVER ,
                         'KOTOSHI' : GGTC_KOTOSHI,
                         'KYONEN'  : GGTC_KOTOSHI-1,
                         'OTOTOSHI' : GGTC_KOTOSHI-2,
                         'DIR'  :  "adminsf",
                         'YEAR'  :  YEAR,

#                        'COLOR_TWILIGHT'  :  "#2AA2C7",
                         'COLOR_TWILIGHT'  :  "#A2C7AA",
                         'COLOR_GGTC'      :  "#80bfff",

                         'TwilightList' : TwilightList,
                         'MemberList' : MemberList
        }

        path = os.path.join(os.path.dirname(__file__), 'templates','adminsf.html')
        self.response.out.write(template.render(path, template_values))

class ModifyHandler(webapp2.RequestHandler):

     def post(self, id=None):
           print("ModifyHandler (POST)" )
           _POST = cgi.escape(self.request.get('MODIFY'))

           try:
            key,model = _POST.split(",")
            print( key, model)
           except:
               ERROR(self, "WHOOPS: Select someone ")
               return

           self.modify( key, model )


           DEBUG( self, "ModifyHandler")
           DEBUG( self, key )
           DEBUG( self, model )


     def modify(self,KEY,MODEL):

#          Edit either a Member or Pending model
           DEBUG( self, KEY )
           DEBUG( self,  MODEL)

           if ( MODEL == "GGTC"):
                print("deal with GGTC ")
                m = GGTC.get_by_id( str(KEY) )
           elif ( MODEL == "TWILIGHT"):
                print("deal with TWILIGHT ")
                m = TWILIGHT.get_by_id( str(KEY) )
           else:
                print("ERROR: not GGTC OR TWILIGHT")

           if( m == None):
                print(self, " Whoops " + MODEL + " = None" )
                DEBUG(self, " Whoops " + MODEL + " = None" )

                return
 

#           print(m.fname + " " + m.lname + " " + m.address + " " + m.address )

           unix = int( int(KEY) )

           g= GENUSSF( m.year ,m.fname, m.lname ,m.address , m.city, m.zip ,m.email , m.phone, m.ntrp , m.help, m.other, m.ip, unix ,LOCALTIME(unix)  )


           template_values = {
                         'YEAR' : m.year,
                         'Model': MODEL,
                         'TITLE'  :  "Modify Member",
                         'DIR'  :  "modifysf",
                         'Member' : g
             }


           path = os.path.join(os.path.dirname(__file__), 'templates','adminsf_modify.html')
           self.response.out.write(template.render(path, template_values))


     def get(self, id=None):
           print("ModifyHandler" )

class ActionHandler(webapp2.RequestHandler):
     def post(self, id=None):

       _DEL = cgi.escape(self.request.get('_DELETE'))
       _EDIT = cgi.escape(self.request.get('_EDIT'))
       _ADD = cgi.escape(self.request.get('_ADD'))

       _MODEL = cgi.escape(self.request.get('Model'))
       _UNIX = cgi.escape(self.request.get('unix'))

       print(_DEL , _EDIT , _ADD )
       print(_MODEL + "(" + _UNIX + ")" )

       title = ""

       _fname = cgi.escape(self.request.get('fname'))
       _lname = cgi.escape(self.request.get('lname'))
       _address = cgi.escape(self.request.get('address'))
       _city = cgi.escape(self.request.get('city'))
       _zip = cgi.escape(self.request.get('zip'))

       _phone = cgi.escape(self.request.get('phone'))
       _email = cgi.escape(self.request.get('email'))
       _ntrp = cgi.escape(self.request.get('ntrp'))

       _ip = cgi.escape(self.request.get('ip'))

       _help = cgi.escape(self.request.get('help'))
       _other = cgi.escape(self.request.get('other'))


#      mtype = cgi.escape(self.request.get('mtype'))

       note= ""
       g = keyID = "" 

# MODEL has to be from goldengatetennisclub database
       if( _MODEL == "GGTC"):
            g =  ndb.Key(GGTC, _UNIX).get()
            keyID =  ndb.Key(GGTC, _UNIX)
            print("GGTC: " + str(g) )
       elif(_MODEL == "TWILIGHT"):
            g =  ndb.Key(TWILIGHT, _UNIX).get()
            keyID =  ndb.Key(TWILIGHT, _UNIX)
            print("TWILIGHT: " + str(g) )
       else:
            self.response.write(" Cant find!!! <br>")
            return

# do the ACTION

#      EDIT 
       if(re.search("Edit", _EDIT) ):
            title = "EDIT"
            print( _EDIT)

            if( g != None):
                g.fname = _fname
                g.lname = _lname
                g.address = _address
                g.city = _city
                g.ntrp = _ntrp
                g.zip = _zip
                g.email = _email

                g.help = _help
                g.other = _other

                note = "MODIFIED " + g.fname + " " + g.lname
                g.put()

#      ADD
#      only a TWILIGHT class needs to be added to database
       elif( re.search("Add",_ADD) ):
            if _MODEL == "TWILIGHT" :
              title = "ADD"


              if( _help  == None ): _help= ""
              if( _other == None ): _other= ""

              p = GGTC(
                   id = _UNIX,             
                   year= g.year,         #g.year,
                   fname = _fname,      #g.fname,
                   lname = _lname,      #g.lname,
                   address  = _address, #g.address,
                   city  = _city,       #g.city,
#                  done  = "",
                   zip  = _zip,        #g.zip,
                   phone  = _phone,     #g.phone,
                   email  = _email,     #g.email,
                   ntrp  = _ntrp,       #g.ntrp,
 
                   src = g.src,

                   help = _help,        #_help,        #g.help,
                   other = _other,      #_other       #g.other
                   ip  = _ip,       #g.ntrp,


                   )

              print( p )
              p.put()
              TRASHCAN( keyID )

              _MODEL = "GGTC"
              print( _ADD)




#      DELETE 
       elif( re.search("Delete" , _DEL) ):
            note = "DELETED " + g.fname + " " + g.lname
            TRASHCAN( keyID)   


       template_values = {

                          'TITLE': title,

                          'NOTE': note,

                          'FNAME': _fname,
                          'LNAME': _lname,

                          'ADDRESS': _address,
                          'CITY': _city,
                          'ZIP': _zip,
                          'PHONE': _phone,
                          'NTRP': _ntrp,
                          'EMAIL': _email,
                          'MTYPE': "---",
                          'COUNT': "---",

#                         'YEAR' : m.year,
                          'MODEL': _MODEL,
                          'UNIX': _UNIX,

#                         'DIR'  :  "modify",
#                         'Member' : g
             }




       path = os.path.join(os.path.dirname(__file__), 'templates','admin_action.html')
       self.response.out.write(template.render(path, template_values))


class TwilightHandler(webapp2.RequestHandler):

   def post(self):

      print("Twilight Handler \n ")
      print self.request.body
      o = self.request.body
      j = json.loads(self.request.body)


#     now =  datetime.datetime.now().strftime("%s")      
#     print ("now = " + str( now ) )

#     unix = j['timestamp']
      unix = j['custom']

      dt =   time.strftime("%b %d %Y %H:%M:%S", time.localtime( unix  ))
      print( "TWILIGHT time " +   str(unix)+ " is " +  str(dt) )

      p = TWILIGHT(
          id = str(unix),             
          year= j['year'],
          fname = j['fname'],
          lname = j['lname'],
          address  = j['address'],
          city  = j['city'],
          done  = "",
          zip  = j['zip'],
          phone  = j['phone'],
          email  = j['email'],
          ntrp  = j['ntrp'],

          src = "PP",

          other = j['other'],
          help = j['help'],


          ip = j['ip'],

#
#          mtype  = j['mtype'],
#          src  = j['src'],
#          zknt = j['zknt'],         # primary member 
#          ztra = str(j['ztra'])     # volunteer
#
         )

      print( p )
      p.put()


import logging,os

#import cloudstorage
#import cloudstorage as gcs

from google.appengine.api import app_identity

class WriteHandler(webapp2.RequestHandler):

   def get(self):

      self.response.write("Write Handler \n ")
      print("Write Handler \n ")


      for key in os.environ :
        self.response.write( key + " => " + str(os.environ[key]) + "<br>" )

#      print("BUCKET_NAME " + str(os.environ['BUCKET_NAME'])  )


#      bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name() )

#      self.response.write("BUCKET NAME: " + str(bucket_name) )

app = webapp2.WSGIApplication(
                                     [
#GET HANDLERS

                                      ('/(current)', GetGGTCHandler),   # current YEAR, return Members
                                      ('/(previous)', GetGGTCHandler),   # current YEAR, return Members


# POST Handlers
                                      ('/ggtc', GGTCHandler),   # POST YEAR, return Members


                                      ('/twilight', TwilightHandler),  # Pending handler

                                      ('/purgesf', PurgeHandler),   # delete database

                                      ('/adminsf', AdminHandler),   # delete database
                                      ('/adminsf/([\d]*)', AdminHandler),


                                      ('/modifysf', ModifyHandler),
                                      ('/_actionsf', ActionHandler),

                                      ('/writesf', WriteHandler),


                                     ],
                                     debug=True)
