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
#stations
#reqstr = factory.delegator("POI",['0', '-37.28443363091711', '143.97789001464844', '-38.92683159077551', '146.32896423339844', '1', '300'])
#data = factory.getData(reqstr)

form = cgi.FieldStorage()
refered = os.environ['REQUEST_URI']

#lines
def getLines():
#	reqstrf = 'http://timetableapi.ptv.vic.gov.au/v2/mode/0/stop/1071/departures/by-destination/limit/200?devid=1000050&signature=5FFCE774F541E9585F328CA3E81A5D858A36D3F5'
#	flin = factory.getData(reqstrf)
	line = json.load(open('/var/www/event/data/trainlines.json'))
#	line = dict()
#	for i in range(len(flin.values()[0])):
#		name = flin.values()[0][i]['platform']['direction']['line']['line_name']
#		line[name] = flin.values()[0][i]['platform']['direction']['line']['line_id']
	return line

def getStations(type, id):
	reqstr = factory.delegator("stopsOnLine", [type, id])
	return reqstr


