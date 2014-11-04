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
#tid = form.getvalue('trainline')
lst = []
method = form.getvalue('meth')
if method == 'stopsNearBy':
	lat = form.getvalue('lat')
	lng = form.getvalue('lng')
	lst = [lat,lng]
if method == 'BND':
	if form.getvalue('mode') == 'train':
		mode = 0
	elif form.getvalue('mode') == 'bus':
		mode = 2
	elif form.getvalue('mode') == 'tram':
		mode = 1
	elif form.getvalue('mode') == 'nightrider':
		mode = 4
	else:
		mode = 3
	stopid = form.getvalue('stopid')
	lst = [mode, stopid, 5]
if method == 'stopsOnLine':
	if form.getvalue('mode') == 'train':
		mode = 0
	elif form.getvalue('mode') == 'bus':
		mode = 2
	elif form.getvalue('mode') == 'tram':
		mode = 1
	elif form.getvalue('mode') == 'nightrider':
		mode = 4
	else:
		mode = 3
	lineid = form.getvalue('lineid')
	lst = [mode, lineid]


print "Content-type: text/plain \n"
print factory.delegator(method,lst)
