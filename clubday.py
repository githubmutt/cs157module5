import webapp2
import logging

import collections,time
import datetime,re,os,cgi,random

from datetime import date

from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

import json   #Python 2.7

from datastore import  *
from google.appengine.api import mail

class G:
   def __init__ ( self, fname,lname, email, gender,ntrp, member, unix ,potluck):
       self.fname = fname
       self.lname = lname
       self.email = email
       self.gender= gender
       self.ntrp = ntrp
       self.member = member
       self.date = LOCALTIME(unix)
       self.unix = unix
       self.potluck = potluck

def mailer( self, fname,lname, email, ntrp , member):
   try:
         mail.send_mail( sender="Roger <tennis.mutt@gmail.com>",
                        to = "Tennis Mutt <tennis.mutt@gmail.com>",
                        subject = "October Club Day (" + fname + " " + lname + ")",
                        body =   "October Club Day \n" +
                                 fname + " " + lname + "\n" +          
                                 ntrp + "\n" +
                                 email + "\n" +
                                 "GGTC Member: " + member  
                          )

         print("MAIL: " + user + " logged in (" + self.request.url + ")" )

   except:
           print("EXCEPTION email!!")


# bigwilly
# Subtact 7 hours
# https://timestamp.online/article/how-to-convert-timestamp-to-datetime-in-python
def LOCALTIME( unix):
      return time.strftime("%b %d %Y %I:%M %p", time.localtime( unix - 7*60*60 ))

class EnterClubDayHandler(webapp2.RequestHandler):
   
    def post(self ,id=None):
        print("EnterClubDayHandler ( POST )")
 
        print self.request.body
        o = self.request.body
        j = json.loads(self.request.body)

#     now =  datetime.datetime.now().strftime("%s")      
        n =  int(time.time())
        print( n )

        c = CLUBDAY(
          id = str(int(n)),             
          fname = j['fname'],
          lname = j['lname'],
          email = j['email']+"@"+j['url'],
          gender = j['gender'],
          ntrp = j['gender']+j['ntrp'],
          member = j['member'],

          potluck = j['potluck'],
          extra = "" # j['extra']

 
         )

        print( c )
        c.put()

#       mailer( self, j['fname'],j['lname'], j['email']+"@"+j['url'],  j['gender']+j['ntrp'] ,  j['member'] )


class ClubDayHandler(webapp2.RequestHandler):

     def get(self ,id=None):
        print("ClubDayHandler")


        obj = []

        cutoff =  str(datetime.date(2019,7,20) )
        p = "%Y-%m-%d"       # 2018-12-01
        opoch =  time.mktime(time.strptime(cutoff,p) )
        opoch =  int( opoch )

        query = CLUBDAY.query( ).order(CLUBDAY.ntrp) 


#       self.response.write("CLUB DAY JSON HANDLER")


        print("before query.iter ")
        for key in query.iter(limit=80):

#            key.lname = key.lname.replace("'", "\'")

#           print("COMPARE:" + str(key.key.id()) + " to " + str(opoch) )
#            self.response.write("COMPARE:" + str(key.key.id()) + " to " + str(opoch) + "<br>")

             if( int(key.key.id()) < opoch):                          
                  print("SKIP "+ key.fname + " " +key.lname )
                  continue


#            print("COLLECTION: " + key.fname + " " + key.lname )
#            self.response.write("<br>")
#            self.response.write("COLLECTION: " + key.fname + " " + key.lname )
             print("\nCOLLECTION: " + key.fname + " " + key.lname )


             d=collections.OrderedDict()    # must be new dictionary, otherwise just last one counts


             d['fname'] = key.fname
             d['lname'] = key.lname
             d['email'] = key.email
             d['ntrp']  = key.ntrp
             d['member'] = key.member
             d['potluck'] = key.potluck
             d['extra'] = key.extra     # if ever needed
             d['unix']  = key.key.id()


             obj.append(d)

             
#       print(obj)
        print("JSON dump ")

        j = json.dumps( obj) 
        self.response.write ( j )
#       print( j )


class DataHandler(webapp2.RequestHandler):

     def get(self ,id=None):
        print("DataHandler")

        ClubData=[]
        ClubData.append(["Chester", "Nimitz" , "ches.nimitz@navy.gov","M", "M4.0", "Y",int( time.time() + random.randint(10,2000 ))   ] )
        ClubData.append(["Jim", "Lovell" , "jim.lovell@nasa.gov","M", "M4.0", "Y",int( time.time() + random.randint(10,2000 ))   ] )
        ClubData.append(["William", "Halsey" , "bill.halsey@navy.gov","M", "M4.0", "Y",int( time.time() + random.randint(10,2000 ))   ] )

        ClubData.append(["Dwight", "Eisenhower" , "ike@army.gov", "M", "M4.0", "N",int( time.time() + random.randint(10,2000 ))   ] )


        print( ClubData )
#        for  i,v in enumerate(ClubData):
#         self.response.write( v )

        for v in ClubData:

         c = CLUBDAY( id= str(  int(v[6]) ), fname=v[0],lname=v[1],email=v[2],gender=v[3],ntrp=v[4]  , member=v[5] )
         self.response.write( c )
         self.response.write( "<br>" )
         print( c )
#        c.put()

class AdminHandler(webapp2.RequestHandler):

     def get(self ,id=None):
        print("ClubDay Admin Handler")
        self.response.write("ClubDay Admin Handler")



        obj = []
        d=collections.OrderedDict()

#       keys = ClubDay.query(ClubDay.year == YEAR ).fetch(keys_only = True)
        query = CLUBDAY.query( CLUBDAY.fname != "" )



#       query = ClubDay.query( ).order(ClubDay.lname) #.order(Reverse=True)
#        query = ClubDay.query( ).order( ClubDay.unix) #.order(Reverse=True)

        ClubDayList=[]
        self.response.write("go")

        for key in query.iter():
           unix = int( key.key.id( ))
           g = G(  key.fname, key.lname, key.email, key.gender, key.ntrp, key.member, unix ,key.potluck)
           ClubDayList.append( g )
#          print( key.fname + " " + key.lname + " " + key.email + " " + key.gender + key.member + " " + str(unix) )
#           self.response.write( key.fname + " " + key.lname + " " + key.email + " " + key.gender + key.member + " " + str(unix) )
#           self.response.write( key.fname + " " + key.lname + " " + key.email + " " +  key.gender + " " + str(unix) )
#           self.response.write("<br>")


        ClubDayList.sort( key=lambda x: x.unix , reverse=True)
        template_values = {
                         'TITLE'  :  "Club Day",
                         'ClubDayList' : ClubDayList

        }

        path = os.path.join(os.path.dirname(__file__), 'templates','clubday.html')
        self.response.out.write(template.render(path, template_values))

# manage_edit
class EditHandler(webapp2.RequestHandler):

     def post(self ):
        print("ClubDay Edit Handler")

        _POST = cgi.escape(self.request.get('MODIFY'))

        try :
          key,model = _POST.split(",")
        except:
          self.response.write("EXCEPTION: select something ")
          return

        print( key, model)

        self.modify( key, model )

     def modify(self,KEY,MODEL):
        print( KEY, MODEL)

        m = CLUBDAY.get_by_id(  str(KEY)   )
        if (m == None) :
           print(" Whoops " + MODEL + " = None")
           return

        print(m.fname + " " + m.lname + " " + m.ntrp + " " + m.email )
        unix = int( int(KEY) )
        g= G( m.fname, m.lname , m.email ,m.gender, m.ntrp, m.member, unix, m.potluck)
# potluck,extra


        template_values = {
                      'TITLE'  :  "Modify Member",

                      'YEAR' : 2019, #m.year,
                      'Model': MODEL,

                      'DIR'  :  "modify",
                      'Member' : g
             }


        path = os.path.join(os.path.dirname(__file__), 'templates','clubday_modify.html')
        self.response.out.write(template.render(path, template_values))

class ActionHandler(webapp2.RequestHandler):

     def post(self , id=None):
       _DEL = cgi.escape(self.request.get('_DELETE'))
       _EDIT = cgi.escape(self.request.get('_EDIT'))

       _MODEL = cgi.escape(self.request.get('Model'))
       _UNIX  = cgi.escape(self.request.get('unix'))


       fname = cgi.escape(self.request.get('fname'))
       lname = cgi.escape(self.request.get('lname'))

       ntrp = cgi.escape(self.request.get('ntrp'))
       email = cgi.escape(self.request.get('email'))

       member = cgi.escape(self.request.get('member'))

       potluck = cgi.escape(self.request.get('potluck'))   

       print(_DEL , _EDIT  )
       print(_MODEL + "(" + _UNIX + ")" )
       print( fname + " " + lname + " " + ntrp + " " + email + " " + member + " " + potluck)

       if( _MODEL != "CLUBDAY"):
            self.response.write("Incorrect Model " + _MODEL)
            return

#      Proceeding
       title = note = ""

       g = ndb.Key(CLUBDAY , _UNIX).get()
       keyID = ndb.Key( CLUBDAY , _UNIX).get()

       if( re.search("Delete", _DEL)):
         title = "ClubDay Deleted"
         note = "DELETED " + g.fname + " " + g.lname
         g.key.delete()
#         keyID.key.delete()

#      delete and  pass through to template

       elif( re.search("Edit", _EDIT)):
             title = "ClubDay Edit"
             if( g != None):

                g.fname = fname
                g.lname = lname
                g.ntrp = ntrp
                g.email = email
                g.member = member
                g.potluck = potluck

                note = "MODIFIED " + g.fname + " " + g.lname
#               self.response.write("MODIFIED " + g.fname + " " + g.lname + " M=" + g.member + "<br>")
                g.put()

       template_values = {

                          'TITLE': title,
                          'NOTE': note,
                          'FNAME': fname,
                          'LNAME': lname,
                          'NTRP': ntrp,
                          'EMAIL': email,
                          'MEMBER': member,
                          'POTLUCK': potluck,

                          'MODEL': _MODEL,
                          'UNIX': _UNIX,

       }

#      self.response.write("template called ")
       path = os.path.join(os.path.dirname(__file__), 'templates','clubday_action.html')
       self.response.out.write(template.render(path, template_values))

class CopyHandler(webapp2.RequestHandler):

     def get(self ):
        self.response.write("Club Day Copy Handler <br>")

        query = ClubDay.query( ).order(ClubDay.ntrp) 

        for key in query.iter(limit=80):
             c = CLUBDAY(
                 id = str(key.key.id()),             
                 fname = key.fname,
                 lname = key.lname,
                 email = key.email,
                 gender = key.gender,
                 ntrp = key.ntrp,
                 member = key.member
             )
             self.response.write(c)
             self.response.write("<br>")
             print(c)
             self.response.write(" skipping copying ")
#            c.put()

class TransferHandler(webapp2.RequestHandler):
     def get(self ):
        transfer=[]


#        transfer.append(["Grace","Man","gmanfrk@yahoo.com","W","W3.0","Y","1538458523"] )
#        transfer.append(["Eric","Yanagi","eric.yanagi@Gmail.com","M","M4.0","Y","1538458574"] )
#        transfer.append(["Willa","Polk","Willapolk@Yahoo.com","W","W3.5","Y","1538527655"] )
#        transfer.append(["Sumedh","Inamdar","sinamdar@gmail.com","M","M3.5","Y","1538951391"] )
#        transfer.append(["Henry","Brodkin","henrybrodkin@sbcglobal.net","M","M3.5","Y","1539632241"] )
#        transfer.append(["Mike","Chin","mike.spcr@Gmail.com","M","M4.0","N","1539690136"] )
#        transfer.append(["Sarah","Papazoglakis","iris286@yahoo.com","W","W3.0","Y","1540071928"] )
#        transfer.append(["Malinda","Lennihan","linda@lennihan.com","W","W3.0","Y","1540072004"] )
#        transfer.append(["Audrey","Chien ","Audreyylc@aol.com","W","W3.5","N","1540272472"] )
#        transfer.append(["Michael","French","mjjfrench@gmail.com","M","M3.5","Y","1540436715"] )
#        transfer.append(["Julia","Pinces","jkpinces@gmail.com","W","W4.0","N","1540437059"] )
#        transfer.append(["Tracy","Vo","tracy.thu.vo@Gmail.com","W","W3.5","Y","1540441983"] )
#        transfer.append(["Henry","Soong","h.soong@gmail.com","M","M4.0","N","1540594667"] )
#        transfer.append(["Lily","Lew","Lily_lew@Yahoo.com","W","W3.0","N","1540613245"] )
#        transfer.append(["Andrew","Chung","andrewchung95@gmail.com","M","M3.5","N","1541376643"] )
#        transfer.append(["Gypsy Rose","Lee","gypsy.rose.lee@yahoo.com","W","W3.5","Y","1545209797"] )
#        transfer.append(["Virginia","Lee","Gini@Gmail.com","W","W3.5","Y","1545513784"] )
#        transfer.append(["Jimmy","Lee","jimmy.lee@Gmail.com","M","M3.5","Y","1545514000"] )
#        transfer.append(["firuz","dumlu","mfdumlupinar@gmail.com","M","M4.5","N","1546021841"] )
        transfer.append(["Tim","Xue","timxue1@gmail.com","M","M4.5","Y","1546553091"] )


        for v in transfer:
          c = CLUBDAY( id= str(  int(v[6]) ), fname=v[0],lname=v[1],email=v[2],gender=v[3],ntrp=v[4]  , member=v[5] )      
          self.response.write( c )
          self.response.write( "<br>" )
          print( c)
          c.put()

class EmailHandler(webapp2.RequestHandler):
     def get(self ):
        self.response.write("ClubDay Handler <br>")

        query = CLUBDAY.query( ).order(CLUBDAY.ntrp) 

        query = CLUBDAY.query( )

        cutoff =  str(datetime.date(2019,1,1) )
        p = "%Y-%m-%d"       # 2018-12-01
        opoch =  time.mktime(time.strptime(cutoff,p) )
        opoch =  int( opoch )

        for key in query.iter():
           if( int(key.key.id()) < opoch):                          
                  print("SKIP "+ key.fname + " " +key.lname )
                  continue

           self.response.write(  key.fname + " , " + key.lname + " , " + key.email + " , " + key.ntrp + " <br>" )

#           self.response.write(  key.fname + " " +  key.lname + " , " + key.email + "<br")


class _TransferHandler(webapp2.RequestHandler):

     def get(self ):
        self.response.write("Transfering Handler <br>")

        self.response.write("transfer = [] <br>")
        query = CLUBDAY.query( )
        for key in query.iter():
            self.response.write("\t transfer.append(")

            self.response.write('\t["' + key.fname+ '","' + key.lname + '","')
            self.response.write( key.email+ '","' +  key.gender + '","' + key.ntrp + '","' + key.member + '","')

            self.response.write( key.key.id() +  '"]  )')
            self.response.write(  "<br>" ) 



app = webapp2.WSGIApplication(
                                    [


                                      ('/enter', EnterClubDayHandler),
                                      ('/clubday', ClubDayHandler),

                                      ('/dataclubday', DataHandler),
                                      ('/clubdaycopy', CopyHandler),

                                      ('/clubdaytransfer', TransferHandler),

                                      ('/manage', AdminHandler),
                                      ('/manage_edit', EditHandler),
                                      ('/manage_action', ActionHandler),

                                      ('/emailcd', EmailHandler)

                                     ],
                                     debug=True)
