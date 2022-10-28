#import webapp2
import logging

import collections
import datetime,re

from datetime import datetime
import time


#import requests,idna,urllib3,certifi, chardet
#import requests_toolbelt.adapters.appengine
#import httplib,urllib

#from google.appengine.ext import ndb
import json   #Python 2.7

#from datastore import  *


fmt = '%Y-%m-%d %H:%M:%S %Z%z'

#print( loc.strftime(fmt ) )
t = time.time()



print time.strftime("%b %d %Y %H:%M:%S", time.gmtime(t))
print time.strftime("%b %d %Y %H:%M:%S", time.localtime(t))
#print( time.localtime() );


