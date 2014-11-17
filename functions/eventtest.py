#! /usr/bin/python
import urllib as url
import xml.etree.ElementTree as et
import datetime as dt
data = url.urlopen('/var/www/event/data/output.xml')
import cgitb
domdata = et.parse(data)
root = domdata.getroot()

items = root.getchildren()

print "Content-type: text/xml \n"
for itm in items:
	try:
		print "------------------------"
		print itm.find('title').text
		print itm.find('{myEvents}tags').text
		print itm.find("{myEvents}eventDate").text
		itm.find('.//latitude').text +  "," + itm.find('.//longitude').text
	except:
		pass


