import webapp2
import logging

import collections
import datetime,re

from google.appengine.ext import ndb
import json   #Python 2.7


import urllib2

from datastore import  *

#from data import *

#from data.dataSC2012 import *

from data.dataSC2013 import *
from data.dataSC2014 import *
from data.dataSC2015 import* 
from data.dataSC2016 import *
from data.dataSC2017 import *
from data.dataSC2018 import *

from data.dataSC2019 import *



class PurgeHandler(webapp2.RequestHandler):
    def get(self):
        YEAR=2018

        self.response.write("PurgeHandler "+str(YEAR)+"*************<br>")

        query = MEMBER.query( MEMBER.year == YEAR).order(MEMBER.lname)
        count=1
        resident=0
        nonresident=0
        for key in query.iter():
            self.response.write( str(count) + ")" )


            if("NR" in key.mtype):
                  nonresident = nonresident + 1
            else:  
                  resident = resident + 1

            self.response.write( key.mtype + " " )
            self.response.write( key.fname + " " + key.lname + "  ")


            self.response.write( "     ")
#            if count%5 == 0:
            self.response.write( "<br>")

#            self.response.write( key.key.delete())
            count = count + 1


        self.response.write( "RES : "+ str(resident) +  " NR: " + str(nonresident) + "  ")


class DataHandler(webapp2.RequestHandler):

   def get (self ):



#       santaclara2012( self )
#       santaclara2013( self )
#       santaclara2014( self )
#       santaclara2015( self )

#       santaclara2016( self )
#        santaclara2017( self )
        santaclara2018( self )
#       santaclara2019( self )





app = webapp2.WSGIApplication(
                                     [

                                      ('/purgesctc', PurgeHandler),
                                      ('/datasctc', DataHandler)

                                     ],
                                     debug=True)
