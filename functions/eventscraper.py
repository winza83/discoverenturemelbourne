#! usr/bin/python

from xml.etree import ElementTree as et
import os

doc = et.parse('/var/www/event/data/output.xml')
root = doc.getroot()

def prInfo(ele):
	subitm = ele.getchildren()
	for k in subitm:
		try:
			print str(k.tag) + ": " + str(k.text)
		except:
			pass
		if len(k._children) > 0:
			prInfo(k)

child = root.getchildren()
n = 0
for i in child:
	print "item " + str(n)
	prInfo(i)
	n += 1
	print ("________________")

"""
title
free entry
url
address
event date
category
tags
"""