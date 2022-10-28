from google.appengine.ext import db

from google.appengine.ext import ndb

import datetime

#KOTOSHI = 2019

# UPDATING INSTRUCTIONS one file each on GAE/PAIR side
#  datastore.py    Change GGTC_KOTOSHI
#  environment.inc change KOTOSHI

SCTC_KOTOSHI = 2019

GGTC_KOTOSHI = 2020

class _ClubDay( ndb.Model):
     fname  = ndb.StringProperty()    # Sam
     lname  = ndb.StringProperty()    # Jones
     email  = ndb.StringProperty()    # sam.jones@gmail.com
     gender  = ndb.StringProperty()    # M/W
     ntrp    = ndb.StringProperty()    # 4.0
     member  = ndb.StringProperty()    # Y/N

class CLUBDAY( ndb.Model):
     fname  = ndb.StringProperty()    # Sam
     lname  = ndb.StringProperty()    # Jones
     email  = ndb.StringProperty()    # sam.jones@gmail.com
     gender  = ndb.StringProperty()    # M/W
     ntrp    = ndb.StringProperty()    # 4.0
     member  = ndb.StringProperty()    # Y/N
     potluck    = ndb.StringProperty()    # Y/N
     extra   = ndb.StringProperty()    # Y/N



class MEMBERSHIP( ndb.Model):
     year = ndb.IntegerProperty()     # 2018
     fname  = ndb.StringProperty()    # Sam
     lname  = ndb.StringProperty()    # Jones
     address  = ndb.StringProperty()  # 131 Memorial Way
     city  = ndb.StringProperty()     # Santa Clara
     zip  = ndb.StringProperty()      # 95124
     phone  = ndb.StringProperty()    # (408) 800-7646
     email  = ndb.StringProperty()    # sam.jones@gmail.com
     ntrp  = ndb.StringProperty()     # M4.0

     src     = ndb.StringProperty()    # Paypal or Check (PP, CHK)

     help  = ndb.StringProperty()     # CTRB (club day,tournaments,refreshments,Board)
     other  = ndb.StringProperty()    # Other _____
     ip  = ndb.StringProperty()       # server IP address


class GGTC( MEMBERSHIP ):
     pass


class TWILIGHT( MEMBERSHIP ):
     done     = ndb.StringProperty()    # done or blank


class GENUSSF:
   def __init__ ( self,year, fname,lname,address,city,zip , email, phone,ntrp, help,other,ip,   unix , date):
      self.year = year
      self.fname = fname
      self.lname = lname
      self.address = address
      self.city = city
      self.zip = zip

      self.email   = email
      self.phone   = phone
      self.ntrp    = ntrp


      self.help = help
      self.other = other
      self.ip = ip


      self.unix    = unix   # is actually the key
      self.date    = date

      if( help  == None): self.help  = ""
      if( other == None): self.other = ""


#
#  for Santa Clara Tennis Club
#

class MEMBER( MEMBERSHIP ):
#    id  = ndb.StringProperty()

     mtype  = ndb.StringProperty()    # RS, RF, RF_, NRS, NRF, NRF_
#    custom  = ndb.StringProperty()    # holds pending information (done or not )

     zknt     = ndb.IntegerProperty(default=0)     # count of family_ 
     ztra     = ndb.StringProperty()     # custom

class PENDING( MEMBER):
     done     = ndb.StringProperty()    # done or blank

     @classmethod
#    convert PENDING or WAIT object into MEMBER object
     def toMEMBER(self, g ):
       print("convert toMEMBER")

       m = MEMBER( key = ndb.Key(MEMBER, g._entity_key.id() ))
       m.fname = g.fname
       m.lname = g.lname
       m.address = g.address
       m.city = g.city
       m.zip = g.zip
       m.mtype = g.mtype

       m.src = g.src 
       if( isinstance(g , WAIT) ): m.src = m.src + "_"

       m.year = g.year
       m.email = g.email
       m.phone = g.phone
       m.ntrp = g.ntrp
       m.zknt = 0         # should be 0 at creation ( additional family members)
       m.ztra = g.ztra    # contains extra volunteer stuff i.e. captain/team, volunteer
       m.put()
       print( m )
       g.done="done"
       g.put()
       return m


class WAIT( PENDING):

     @classmethod
     def get_one( self):
       try:
         return self.query().order(-WAIT.created).get()
       except IndexError:
         raise ModelException("No records")


     @classmethod
     def pop(self, YEAR ):
#  Get the first one in the waitlist
       query = WAIT.query( WAIT.year == YEAR)
       if query.count() == 0:
         print("WAIT.pop() : empty ")
         return None
       
       s=[]
       for q in query:
          s.append( q._entity_key.id() )

       s.sort( ) # ascending order  or reverse = True 
       r = WAIT.get_by_id( s[0]   )

       return r

     @classmethod
     def search( self , YEAR):
#      keys = WAIT.query( WAIT.year == YEAR).fetch(keys_only = True ).order(WAIT.created)
#      return self.query().fetch(1)[0]
       query = WAIT.query( WAIT.year == YEAR).order(WAIT.created)
       print( query.count() )
       print( dir(query) )


       if query.count() > 0:
        entity = query.get()
        print( entity.fname + " " + entity.lname + " " + str(entity.created )  )
        keyID = ndb.Key(WAIT, int(entity.created))
        return int(entity.created) # keyID
       else:
        print(" WAIT list empty")
        return None

     @classmethod
     def toMember( entity ):
        print("convert to MEMBER ")
#       self.response.write( q.fname + " " + q.lname  + " " + str( q.created ) )
        print(entity)        
        print(entity.fname ) # + " " + entity.lname )
        print(entity.lname ) # + " " + entity.lname )
        print(entity.address ) # + " " + entity.lname )


class TRASH( PENDING ):
     pass

class PREVIOUS( PENDING ):
     pass


class GENUS:
   def __init__ ( self,year, fname,lname,address,city,zip , email, phone,ntrp,mtype,src, zknt,ztra ,unix,date ):
      self.year = year
      self.fname = fname
      self.lname = lname
      self.address = address
      self.city = city
      self.zip = zip

      self.email   = email
      self.phone   = phone

      self.ntrp    = ntrp
      self.mtype    = mtype
      self.src    = src

      self.zknt    = zknt    # Family member count
      self.ztra    = ztra    # hold extra data ( Renewal, volunter...)

      self.unix    = unix
      self.date    = date


