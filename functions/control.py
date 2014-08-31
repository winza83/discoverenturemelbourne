#! /usr/bin/python
import sys
sys.path.append('/var/www/MTApp/')
import PTVfactory as P
import cgi
import cgitb
import stations_lines as stations_lines
import os

googleKey = 'AIzaSyDejfQWInSUrLPFX8iTFQ0fBm62RdKPLNo'
baseurl = "http://timetableapi.ptv.vic.gov.au"
key = '29246674-a96c-11e3-8bed-0263a9d0b8a0'
devid = 1000050
factory = P.Trans(googleKey, key, devid)


print "Content-type: text/html \n"
print "<!DOCTYPE html>"
print """
	<head>
		<title>Events and Transport</title>
		<script type="text/javascript" src="../../jquery/jquery-2.0.3.js"></script>
		<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false&libraries=drawing"></script>
		<script type="text/javascript" src="../../jquery/jquery-ui-1.10.3.custom/js/jquery-ui-1.10.3.custom.min.js"></script>
		<script type="text/javascript">
		var map = [];
		var markers = [];
		var infowin;
		var stname = [];
		function initialize() {
			var myOptions = {
				center:  new google.maps.LatLng(-37.85, 145.05),
				zoom: 9,
				mapTypeId: google.maps.MapTypeId.ROADMAP
			};
			map[0] = new google.maps.Map(document.getElementById("mapper"), myOptions);

		}

		function getStations() {
			var lineid = document.getElementsByTagName('option')[document.getElementById("trainline").selectedIndex].value;
			var xmlhttp = new XMLHttpRequest();
			var addr = 'http://124.190.54.81/event/functions/test.py?trainline=' + lineid;
			xmlhttp.open('GET',addr, true);
			xmlhttp.send();
			xmlhttp.onreadystatechange=function() {
				if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
					document.getElementById('reqstr').value = xmlhttp.response;

				}
			}
		}

		function getData() {
			var addr = document.getElementById('reqstr').value;
			var xmlhttp = new XMLHttpRequest();
			xmlhttp.open('GET',addr, true);
			xmlhttp.send();
			xmlhttp.onreadystatechange=function() {
				if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
					document.getElementById('data').value = xmlhttp.response;

				}
			}
		}

		function displayOnMap() {
			initialize();
			var data = JSON.parse(document.getElementById('data').value);
			for (i = 0; i < data.length; i++) {
				lat = data[i]['lat'];
				lng = data[i]['lon'];
				stname.push(data[i]['location_name']);
				transtype = data[i]['transport_type'];
				plotMap(transtype, lat, lng, stname[i]);

			}
		}

		function clearMap() {
			map[0] = new google.maps.Map(document.getElementById("mapper"), myOptions);
		}

		function plotMap(transtype, lat, lng, name) {
			icon = '';

			if (transtype == "nightrider" || transtype == "bus") {
				icon = 'http://124.190.54.81/MTApp/bus.png';
			}
			else if (transtype == "tram") {
				icon = 'http://124.190.54.81/MTApp/tram.png';
			}
			else if (transtype == "train") {
				icon = 'http://124.190.54.81/MTApp/train.png';
			}

			var image = {
				url: icon,
				size: new google.maps.Size(20, 20),
				origin: new google.maps.Point(0, 0),
				anchor: new google.maps.Point(0, 0),
				scaledSize: new google.maps.Size(20,20)
			};

			markers.push(new google.maps.Marker({
				position: new google.maps.LatLng(lat, lng),
				icon: image,
				map: map[0]
			}));
    		markers[markers.length - 1].setMap(map[0]);

			marker = markers[markers.length - 1];

			google.maps.event.addListener(marker, 'click', function(event) {
			if (infowin != null) {
				infowin.close();
			}
			infowin = new google.maps.InfoWindow({content: name});
			infowin.setPosition(event.latLng);
			infowin.open(map[0], this);
			});
		}

		</script>
		<style>
			#mapper {
				width: 60%;
				height: 500px;
				float: right;
			}
			body {
				background-color: #000000;
			}
			#reqstr, #data {
				width: 400px;
				background-color: #E7CFB4;
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
print "<select id=\"trainline\" onchange=\"getStations();\">"
for i in lines:
	print "<option value='" + str(lines[i])+"'>" + i + "</option>"
print "</select><br />"
print "<input id='reqstr' type='text' />"
print "<input id='getdata' value='get data' type='button' onclick='getData()' /><br />"
print "<textarea id='data' rows='10'>"
print "</textarea>"
print "<input id='showOnMap' value='show on map' type='button' onclick='displayOnMap();' /><br />"


print "</form>"

print "</body>"
print "</html>"
