#! /usr/bin/python
import sys
sys.path.append('/var/www/MTApp/')
import PTVfactory as P
import json
import urllib as url
import cgi
import cgitb
cgitb.enable()
import os

googleKey = 'AIzaSyDejfQWInSUrLPFX8iTFQ0fBm62RdKPLNo'
baseurl = "http://timetableapi.ptv.vic.gov.au"
key = '29246674-a96c-11e3-8bed-0263a9d0b8a0'
devid = 1000050
factory = P.Trans(googleKey, key, devid)
form = cgi.FieldStorage()
refered = os.environ['REQUEST_URI']
tid = form.getvalue('trainline')
method = 'stopsOnLine'
print "Content-type: text \n"

print factory.delegator(method,[0,tid])

