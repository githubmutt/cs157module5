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

# ndb.Key(YourModel, id).get().
# queryset=Photo.query(Photo.id.IN(photoid_list))

class AddressHandler(webapp2.RequestHandler):

   def post(self):

#      param = self.request.get("cal")
#      print('PARAM = ' + param )

      print('AddressHandler (POST)')

#      address  = self.request.body
      address = json.loads(self.request.body)

      print(address)      
      self.result( address )


   def result(self, addr):


      ADDR = addr['address']

      YEAR = SCTC_KOTOSHI

      print( "search for " + ADDR + " in year " + str(YEAR) + "\n")

      query = MEMBER.query( MEMBER.address == ADDR ,   MEMBER.year == YEAR , MEMBER.mtype.IN( ["RF","NRF"]) , MEMBER.zknt <= 2 )


      name = mtype = date = " "
      found = "NO"
      print("start query ... ")
      for key in query.iter():
             name = key.fname + " " + key.lname
             mtype = key.mtype
             address = key.address
             date  =  int(key.key.id())    # main member identifier (stored in the key id )
             count =  key.zknt 
             found = "YES"
             print( "*"*10 + "  " + "FOUND ADDRESS MATCH" + "   " + "*"*10 )
             print( str(key.year) + " " + name + " " + mtype + " " + str(date)  + " (" + str(count) + ")" )

      payload = { "found" : "no"  }
      if found == "YES":
        payload = { "found": "yes" , "address": address , "name" : name , "mtype": mtype , 'key' : date ,'year': YEAR}


      jds = json.dumps(payload)

      print( "-"*45 )
      print( payload )
      print( jds )
      print( "-"*45 )

      self.response.headers['Content-Type'] = 'application/json'
      self.response.write( jds )
#      return  jds  




# Send out members 
class GetYearHandler(webapp2.RequestHandler):

    # NEW June 24, 2019  try to renew members of year has to be a get
    def get(self ,id=None):

       print("GetYearHandler: get ")
       print self.request.body

       j = json.loads(self.request.body)
       YEAR = int( j['year'] )

    def post(self ):

# receive a year, return members for that year

        print("GetYearHandler() : received POST request")
        print self.request.body
        j = json.loads(self.request.body)
        self.result( j )

#        return
    def result( self, jdata):

        YEAR = int( jdata['year'] )
        print("SCTC for membership year " + str(YEAR)  )

        query = MEMBER.query( MEMBER.year == YEAR).order(MEMBER.lname)
        obj = []

        for key in query.iter():

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
        print("JSON Data")
        self.response.headers['Content-Type'] = 'application/json'
        j=json.dumps(obj)
        self.response.write( j  )


class GetMembersHandler(webapp2.RequestHandler):

    def get(self ,id=None):

        YEAR = 2019
        if( id == "kyonen"):
            YEAR =  2018
        elif(id == "otoshi"):
            YEAR =  2017

        print(" Membership for " + str(YEAR)  )

        obj = []

#-----------------------------------------------
# PUT THIS ALL BACK IN
#
        try:
           query = WAIT.query( WAIT.year == YEAR)   # .order(Wait.lname)
           for key in query.iter(limit=30):
             d=collections.OrderedDict()    # must be new dictionary, otherwise just last one counts
             d['year']= key.year
             d['fname']= key.fname
             d['lname']= key.lname
             d['address']= key.address
             d['city']= key.city
             d['email']= key.email
             d['ntrp']= key.ntrp
             d['mtype']=   key.mtype
             d['date']=   int(key.key.id())
             d['status']=   "WAIT"

             obj.append(d)
        except:
            print("NO WAIT class (likely sfmongoldata")

#-----------------------------------------------

# https://cloud.google.com/appengine/docs/standard/python/ndb/queries
#       YEAR = 2018

        query = MEMBER.query( MEMBER.year == YEAR).order(MEMBER.lname)
#        query = MEMBER.query( MEMBER.year == YEAR)

        query1 = MEMBER.query( MEMBER.year == YEAR)
        query = query1.order( MEMBER.lname )


# https://cloud.google.com/appengine/docs/standard/python/ndb/queries
#       for key in query.iter(limit=30):
        for key in query.iter():

             d=collections.OrderedDict()    # must be new dictionary, otherwise just last one counts

             d['year']= key.year
             d['fname']= key.fname
             d['lname']= key.lname
             d['address']= key.address
             d['city']= key.city
             d['email']= key.email
             d['ntrp']= key.ntrp
             d['mtype']=   key.mtype
             d['date']=   int(key.key.id())
             d['status']=   "MEMBER"

#             print("*"*30 + "\n")            
#             print( key )
#             print( key.key )
#            print( key.key.get() )
#             print("\n"+"-"*30 + "\n")            

             obj.append(d)

# DUMP JSON data 
        j=json.dumps(obj)
        self.response.write( j  )

     
    def senddata(self, year ):

        query = MEMBER.query( MEMBER.year > year)
        obj = []


# https://cloud.google.com/appengine/docs/standard/python/ndb/queries
        for key in query.iter():

             d=collections.OrderedDict()    # must be new dictionary, otherwise just last one counts

             d['year']= key.year
             d['fname']= key.fname
             d['lname']= key.lname
             d['address']= key.address
             d['city']= key.city
             d['email']= key.email
             d['mtype']=   key.mtype
             obj.append(d)

# DUMP JSON data 
#       j=json.dumps(obj)
        j=json.encode(obj)

        self.response.content_type = 'application/json'
        self.response.write( j  )

#       self.response.out.write( j  )


senddata = {}
senddata["message"] = 'Testing Tester'

response_template = 'The message sent was:\n){0}'


# Handle a post of a year, then return members of that year

class POSTHandler(webapp2.RequestHandler):

# Receive JSON
    def post(self):

         message = "OK "
#         self.response.headers['Content-Type'] = 'text/plain'
#         self.response.write(response_template.format(message ))
 
         print("received POST ")
         print self.request.body
         o = self.request.body
         j = json.loads(self.request.body)


         year = j['year']

         query = MEMBER.query( MEMBER.year > year)
         obj = []

# https://cloud.google.com/appengine/docs/standard/python/ndb/queries
         for key in query.iter():

             d=collections.OrderedDict()    # must be new dictionary, otherwise just last one counts

             d['year']= key.year
             d['fname']= key.fname
             d['lname']= key.lname
             d['address']= key.address
             d['city']= key.city
             d['email']= key.email
             d['mtype']=   key.mtype
             obj.append(d)

#        print(obj)
         j=json.dumps(obj)

# https://varunver.wordpress.com/2013/05/20/python-post-json-data-curl-equivalent-in-python-using-urllib2/

         url = 'http://localhost:8080/data' 
         print("POSTING data to " + url )
         req = urllib2.Request( url , j,  headers={'Content-type': 'application/json', 'Accept': 'application/json'} )

         print( req )
         inspect( req )

#         response = urllib2.urlopen(req)
#         the_page = response.read()
#         print the_page


#         self.redirect('http://localhost:8080/data') 
# DUMP JSON data 



#         req = urllib2.Request('http://localhost:8080/post/create') 

#         req = urllib2.Request('http://localhost:8080/post/create') 
#         req.add_header('Content-Type','application/json')

#         response = urllib2.urlopen(req , j )

#        self.response.write( j  )


#         fname = j['fname']
#         lname = j['lname']
#         address = j['address']
#         city = j['city']

#         zip = j['zip']
#         ntrp = j['ntrp']
#         mtype = j['mtype']
#         code = j['code']


#        txt_url_values = urllib.urlencode(senddata)
#        txturl = 'http://localhost:10080'
#        result = urllib.urlopen(txturl, txt_url_values)
#        self.redirect('http://localhost:10080') 


#        self.response.out.write( "NOSJ"  )        
#        con = self.request.get("message")
#        self.response.write(con)

def hello():
   print "hello"

# Transfer from PENDING to Member
# Transfer from Twilight to GGTC
class TransferHandler(webapp2.RequestHandler):
   def post(self,id=None):
       print( "TransferHandler (POST) ")
       print self.request.body
       key = json.loads(self.request.body)
       print("Incoming KEY = " + str(key) )

       self.result(key['key'])

   def result(self,key):


#      EITHER ONE
#      sfmongoldata.appspot.com
#      scmongoldata.appspot.com
#      
       SERVER = os.environ["HTTP_HOST"] 

       print( "search for key " + str(key) + " in " + SERVER  )

       print( "searching = " + str(SERVER.find("scmongoldata.appspot.com")) )
       print( "searching = " + str(SERVER.find("sfmongoldata.appspot.com")) )


       if( SERVER.find("scmongoldata.appspot.com") != -1):
          self.toMEMBER( key)
       elif( SERVER.find("sfmongoldata.appspot.com")  != -1):
          self.toGGTC( key )
       else:
          print("LOCALHOST \n")
#   HAVE to comment out one of these, whether testing GGTC or SCTC (MEMBER)
#         self.toGGTC( key )
          self.toMEMBER( key )


#  transfer from TWILIGHT to GGTC model
   def toGGTC( self,  KEY):

        print("Golden Gate Tennis Club (SCTC)  key=" + str(KEY)    )

        p = TWILIGHT.get_by_id( str(KEY) )
        if( p == None):
          print("NOT FOUND" )
          return

        print( p )
        if( len(p.done)  > 0 ):
          print("ALREADY DONE" )
          return

#       Make into a GGTC object
        m = GGTC(key=ndb.Key( GGTC , str( KEY ) ))
        m.fname = p.fname
        m.lname = p.lname
        m.address = p.address
        m.city = p.city
        m.zip = p.zip

        m.year = p.year
        m.email = p.email
        m.phone = p.phone
        m.ntrp = p.ntrp
        m.ip = p.ip

        m.help = p.help
        m.other = p.other

        m.done="done"      # done

        
        p.done="done"
        print( "TRANSFER ") 
        print( p )
        print( "to"  )
        print( m )

        r1=p.put()
        r2=m.put()

        print("results of p.put =" + str(r1)  )
        print("results of m.put =" + str(r2)  )

        print("FINISHED"  )

# TRANSFER from PENDING to MEMBER or WAIT class
   def toMEMBER(self,KEY):

        print("Santa Clara Tennis Club (Member)")
        print("looking for PENDING  KEY=" + str(KEY) )

        p = PENDING.get_by_id( str(KEY) )
        if( p == None):
          print("NOT FOUND" )
          return
    
        print( p )
        if( len(p.done)  > 0 ):
          print("ALREADY DONE" )
          return

        print("converting PENDING to MEMBER")
        PENDING.toMEMBER( p )
        print("converting done")        
        p.done="done"
        p.put()
 

        # WAS a new MEMBER created?  Check for a WAIT object
        MYEAR = p.year
        if( isinstance( p ,MEMBER)):
           print("Check if someone to pop off the WAIT list")
           w = WAIT.pop(MYEAR)
           if( w != None):
                 print( "WAIT object")
                 print(w)
                 print("someone to pop off waitlist")
                 WAIT.toMEMBER( w )
                 TRASHCAN ( w )
        else:
          print("not a MEMBER instance")
          print(m)
          print("*"*17)




   def get(self,id=None):

        print("Transfer Handler \n ")

        KEY = int(id)

        g = PENDING.get_by_id( str(KEY) )
        if( g == None):
          print("KEY " + str(KEY) + " not found \n")
          print("return " )
          return
   

#       Make into a MEMBER

        memberKey = ndb.Key(MEMBER, str(KEY) )
#        h = MEMBER.get_by_id( str(dateKey) )

        h = MEMBER( key = memberKey )
        h.fname = g.fname
        h.lname = g.lname
        h.address = g.address
        h.city = g.city
        h.zip = g.zip
        h.mtype = g.mtype
        h.src = g.src

        h.year = g.year
        h.email = g.email
        h.phone = g.phone
        h.ntrp = g.ntrp

        h.zknt = g.zknt    # should be 0
        h.ztra = g.ztra    # contains extra date i.e. captain/team, volunteer

        print( "TRANSFER " + str(KEY) + " " + str(h.year) + " " + h.fname + " " + h.lname + " " + h.address + " " + h.city + " " + h.zip)
        h.put()
        g.done="done"  
        g.put()

        print("DONE")



class PendingHandler(webapp2.RequestHandler):

   def post(self):

      print("Pending Handler ************************* \n ")
      print("Pending Handler ************************* \n ")

      print self.request.body
      o = self.request.body
      j = json.loads(self.request.body)


#     now =  datetime.datetime.now().strftime("%s")      
#     print ("now = " + str( now ) )

      unix = j['timestamp']

#      print("x"*10)
#      print( unix.localtime() )
#      print( unix.time() )
#      print( time.ctime( unix ) )
#      print("x"*10)


      dt =   time.strftime("%b %d %Y %H:%M:%S", time.localtime( unix  ))
      print( "PENDING time " +   str(unix)+ " is " +  str(dt) )

      p = PENDING(
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
          mtype  = j['mtype'],
          src  = j['src'],          # WAIT for waitlist

          zknt = j['zknt'],         # primary member 
          ztra = str(j['ztra'])     # volunteer

         )

      print( p )
      p.put()

#  print WAIT LIST
#      query = WAIT.query( WAIT.year == YEAR)  #.order(MEMBER.lname)
#      for key in query.iter():
#           print( key.year, key.fname, key.lname )






# Equivalent to AJAX call to allow non-residents to enter
class AJAXHandler(webapp2.RequestHandler):
   def get(self):

# Calculate if we can add non-residents
#      add  = [None]*1
#      add.append("yes")
#      j = json.dumps( add )
#      print( j )
      obj = []
      d=collections.OrderedDict()
      d['results'] = "yes"
      obj.append(d)
      j = json.dumps(obj)
      self.response.content_type = 'application/json'
      self.response.write( j )
      print( j )



#    params = urllib.urlencode( {'address' : 'yes' })
#    headers = { 'Content-type": "application/x-www-form-urlencoded',"Accept": "text/plain"  }

#
#    url = "http://localhost:8080/test"
#    payload = { 'address': '372 Forbes'}
#    content = {'content-type' : 'application/json' }

#    j=json.dumps(payload)
#    self.response.write( j  )



#    requests_toolbelt.adapters.appengine.monkeypatch() 

#    r = requests.post( url  ,  headers = content , data=json.dumps(payload)     )
#    print(url)
#    print(r)


# Find address in dB
# NOT USED
class AddressHandler_(webapp2.RequestHandler):

   address =  ""

   def post(self):

      print self.request.body
      self.address = self.request.body


      j = json.loads(self.request.body)
 
      print ( j )

      print('AddressHandler')

      address = j['address'] 

      YEAR = 2018

      print( "search for " + address + "in year " + str(YEAR) + "\n")

      query = MEMBER.query( MEMBER.address == address ,   MEMBER.year == YEAR , MEMBER.mtype.IN( ["RF","NRF"]) ,MEMBER.zknt <= 2 )

      name = mtype = date = " "
      found = "NO"
      for key in query.iter():
             name = key.fname + " " + key.lname
             mtype = key.mtype
             date =  int(key.key.id())

             found = "YES"
             print( "*"*10 + "  " + "FOUND ADDRESS MATCH" + "   " + "*"*10 )
             print( str(key.year) + " " + name + " " + mtype + " " + str(key.zknt)   )


      print("sending back response ")

      payload = { "found" : "no"  }
#      if found == "YES":
#        payload = { "found": "yes" , "address": address , "name" : name , "mtype": mtype , 'key' : date ,'year': YEAR}
#       payload = { "found" : "yes"  }

#      self.response.write( payload )
#      print(payload)
#      jds = json.dumps(payload)

class DistributionHandler(webapp2.RequestHandler):
   def post(self):
      print("DistributionHandler(POST)")

      jdata = json.loads(self.request.body)
      print("Distribution YEAR ")
      print(jdata)
      print("Distribution YEAR")
      self.result( jdata )

   def get( self ):
      print("Distribution GET ")
    

   def result(self, jdata):
         YEAR = jdata['year']

         RES   = 0
         NON   = 0
         WAITLIST  = 0

         query = WAIT.query( WAIT.year == YEAR)
         for key in query.iter():
                 WAITLIST += 1

         query = MEMBER.query( MEMBER.year == YEAR)

         pattern = 'NR'
         r = re.compile( pattern ,re.IGNORECASE )

         for key in query.iter():


             if( re.search(pattern,key.mtype) ):
                 NON += 1
             else:
                 RES += 1

#            print("MTYPE = " + str(key.mtype) + " " + str(RES) + "/" + str(NON) + "   " + key.fname + "  " + key.lname )


         obj = []
         d=collections.OrderedDict()          

         print("RESIDENTS = " + str(RES) + " NONRESIDENTS = " + str(NON) )
         d[ "majority"] =  "no"

         if( RES - NON >=2 ):
          d[ "majority"] =  "yes"

         d[ "residents"] =  RES
         d[ "nonresidents"] = NON
         d[ "wait"] = WAITLIST


         obj.append(d)

# DUMP JSON data 
#         j=json.dumps(obj)
         j=json.dumps(d)
         self.response.write( j  )


class MajorityHandler(webapp2.RequestHandler):
   def get(self):

# Get number of residents/non-residents         
         YEAR = SCTC_KOTOSHI    # year set in datastore.py
         RES   = 0
         NON   = 0
         query = MEMBER.query( MEMBER.year == YEAR)

         pattern = 'NR'
         r = re.compile( pattern ,re.IGNORECASE )
         for key in query.iter():

             if( re.search(pattern,key.mtype) ):
                 NON += 1
             else:
                 RES += 1


         obj = []
         d=collections.OrderedDict()          

         print("RESIDENTS = " + str(RES) + " NONRESIDENTS = " + str(NON) )
         d[ "majority"] =  "no"

         if( RES - NON >=2 ):
          d[ "majority"] =  "yes"

         d[ "residents"] =  RES
         d[ "nonresidents"] = NON


         obj.append(d)

         print("majority = " + str(d["majority"]) )
         print("residents = " + str(d["residents"]) )
         print("nonresidents = " + str(d["nonresidents"]) )



# DUMP JSON data 
         j=json.dumps(obj)
         self.response.write( j  )

# ---------------------------------------------------
def Loader( theCLASS, unix,year,fname,lname,address,city,done,zip,phone,email,ntrp,mtype,src,_zknt,_ztra):


#    print(type( WAIT ))
#    if ( type(WAIT) == WAIT):
#        print("yes "*12 )

    _zknt=0
    _ztra=""
    if( theCLASS == "WAIT" ):
       print("WAIT class ")
       p = WAIT(id= str(unix),year= year,fname= fname,lname= lname, address=address,city= city, done=done,zip= zip ,
           phone= phone,email= email, ntrp=ntrp, mtype= mtype , src=src, zknt=_zknt, ztra=_ztra )     # volunteer
       p.put()
    elif( theCLASS == "PENDING"):
       p = PENDING(id= str(unix),year= year,fname= fname,lname= lname, address=address,city= city, done=done,zip= zip ,
           phone= phone,email= email, ntrp=ntrp, mtype= mtype , src=src, zknt=_zknt, ztra=_ztra )     # volunteer
       p.put()
    elif( theCLASS == "MEMBER"):
       p = MEMBER(id= str(unix),year= year,fname= fname,lname= lname, address=address,city= city, zip= zip ,
           phone= phone,email= email, ntrp=ntrp, mtype= mtype , src=src, zknt=_zknt, ztra=_ztra )     # volunteer
       p.put()


class LoadPendingHandler(webapp2.RequestHandler):
   def post(self):
      j = json.loads(self.request.body)
      unix = j['timestamp']
      dt =   time.strftime("%b %d %Y %H:%M:%S", time.localtime( unix  ))
      print( "PENDING time " +   str(unix)+ " is " +  str(dt) )
      Loader( "PENDING" ,str(unix) , j['year'] , j['fname'], j['lname'],j['address'],j['city'],"", j['zip'],j['phone'],j['email'], j['ntrp'], j['mtype'], "PP" , "zknt",  str(j['ztra']) )


class LoadMemberHandler(webapp2.RequestHandler):
   def post(self):
      j = json.loads(self.request.body)
      unix = j['timestamp']
      dt =   time.strftime("%b %d %Y %H:%M:%S", time.localtime( unix  ))
      print( "MEMBER time " +   str(unix)+ " is " +  str(dt) )
      Loader( "MEMBER" ,str(unix) , j['year'] , j['fname'], j['lname'],j['address'],j['city'],"", j['zip'],j['phone'],j['email'], j['ntrp'], j['mtype'], "PP" , "zknt",  str(j['ztra']) )

class LoadWaitHandler(webapp2.RequestHandler):
   def post(self):

      print("Wait Handler (used for testing) ************* \n ")

      print self.request.body
      o = self.request.body
      j = json.loads(self.request.body)

      unix = j['timestamp']
      dt =   time.strftime("%b %d %Y %H:%M:%S", time.localtime( unix  ))

      print( "WAIT time " +   str(unix)+ " is " +  str(dt) )
      Loader( "WAIT" ,str(unix) , j['year'] , j['fname'], j['lname'],j['address'],j['city'],"", j['zip'],j['phone'],j['email'], j['ntrp'], j['mtype'], "WAIT_" , "zknt",  str(j['ztra']) )



# WaitHandler is identical to PendingHandler except for WAIT datastore (instead of PENDING)
class LoadWaitHandler_(webapp2.RequestHandler):

   def post(self):

      print("Wait Handler (used for testing) ************* \n ")

      print self.request.body
      o = self.request.body
      j = json.loads(self.request.body)

      unix = j['timestamp']
      dt =   time.strftime("%b %d %Y %H:%M:%S", time.localtime( unix  ))
      print( "WAIT time " +   str(unix)+ " is " +  str(dt) )

      p = WAIT(
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
          mtype  = j['mtype'],
          src  = "WAIT_" , # j['src'],

          zknt = j['zknt'],         # primary member 
          ztra = str(j['ztra'])     # volunteer

         )

      print( p )
      p.put()


app = webapp2.WSGIApplication(
                                     [

                                      ('/year', GetYearHandler),

# GET Handlers
                                      ('/address', AddressHandler),
                                      ('/majority', MajorityHandler),

                                      ('/distribution', DistributionHandler),


                                      ('/(kotoshi)', GetMembersHandler),
                                      ('/(kyonen)',  GetMembersHandler),
                                      ('/(otoshi)',  GetMembersHandler),

# POST HANDLERS
                                      ('/post', POSTHandler),


                                      ('/pending', PendingHandler),


                                      ('/transfer', TransferHandler),
                                      ('/transfer/([\d]*)', TransferHandler),


                                      ('/ajax', AJAXHandler),

#                                     FOR TESTING -- put directly into PENDING/MEMBER/WAIT 
                                      ('/loadPending', LoadPendingHandler),  
                                      ('/loadWait', LoadWaitHandler),   
                                      ('/loadMember', LoadMemberHandler), 
#                                     FOR TESTING -- put directly into PENDING/MEMBER/WAIT 

                                     ],
                                     debug=True)
