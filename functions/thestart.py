#! /usr/bin/python
import sys
sys.path.append('/var/www/MTApp/')
import PTVfactory as P
import cgi
import cgitb
import stations_lines as stations_lines
import os
import subprocess

googleKey = 'your google key'
baseurl = "http://timetableapi.ptv.vic.gov.au"
key = 'your ptv api key'
devid = your ptv dev id
factory = P.Trans(googleKey, key, devid)

host = (subprocess.Popen(['curl', 'ifconfig.me'], stdout = subprocess.PIPE).communicate()[0])
ip = host.replace("\n","")
print "Content-type: text/html \n"
print "<!DOCTYPE html>"
print """
	<head>
		<title>Events and Transport</title>
		<script type="text/javascript">
"""
print "var ip = '" + str(ip) + "';"
print """</script>
		<script type="text/javascript" src="../../jquery/jquery-2.0.3.js"></script>
		<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false&libraries=drawing"></script>
		<script type="text/javascript" src="../../jquery/jquery-ui-1.10.3.custom/js/jquery-ui-1.10.3.custom.min.js"></script>
		<script type="text/javascript" src="utils.js">
		</script>
		<style>
			#mapper {
				width: 70%;
				height: 500px;
				float: right;
			}
			body {
				background-color: #000000;
			}
			#reqstr, #data {
				width: 300px;
				background-color: #E7CFB4;
				display: block;
			}

			#data {
				height: 100px;
			}

			#route {
				color: white;
				float: left;
				width: 240px;
			}


			#info {
				width: 100px;
				height: 50px;
			}
		</style>
	</head>
"""
print "<body onload='initialize()'>"

print "<div id='mapper'></div>"
#1. enter train line
#2. show events
#3. show cafes/restaurants
lines = stations_lines.getLines()
print "<form id='lines'>"
#print "<input value='locate me' id='myloc' type='button' onclick='getLoc()' /><br />"
print "<input value='Set location' id='setloc' type='button' onclick='setLoc()' /><br />"
print "<input value='Get nearest transport' id='gettrans' type='button' onclick='getStations()' /><br />"
print "<input type='button' value='Stops on Selected Route' onclick='stopsOnRoute()'>"
print "<input type='button' value='Get Related Route' onclick='getRoute()'>"
print "<input type='button' value='Plot events' onclick='getEvents()'>"
print "<input id='reqstr' type='text' />"
print "<textarea id='data' rows='1'>"
print "</textarea>"
print "</form>"
print "<ul id='route'></ul><br />"
print "</body>"
print "</html>"
