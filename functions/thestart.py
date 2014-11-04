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
		var poi = '';
		var linedata = {};
		var stname = [];
		var loc = [];

		function initialize() {
			linedata = {};
			infowin = null;
			var myOptions = {
				center:  new google.maps.LatLng(-37.85, 145.05),
				zoom: 9,
				mapTypeId: google.maps.MapTypeId.ROADMAP
			};
			map[0] = new google.maps.Map(document.getElementById("mapper"), myOptions);

		}

		function getStations() {
			document.getElementById('route').innerHTML = '';
			if (loc.length != 0) {
				sendpos = [loc[0].getPosition().lat(), loc[0].getPosition().lng()];
				var addr = "http://124.190.54.81/event/functions/adaptor.py?meth=stopsNearBy&lat=" + sendpos[0] + "&lng=" +sendpos[1];
				getRequest(addr);
			}
		}

		function getRequest(addr) {
			var xmlhttp = new XMLHttpRequest();
			xmlhttp.open('GET',addr, true);
			xmlhttp.send();
			xmlhttp.onreadystatechange=function() {
				if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
					document.getElementById('reqstr').value = xmlhttp.response;
					getData();
				}
			}
		}

		function showRoute() {
			allinput = document.getElementsByTagName('input');
			for (i = 0; i < allinput.length; i++) {
				if (allinput[i].type == 'checkbox') {
						initialize();
						loc[0] = new google.maps.Marker({position: poi, map: map[0]});
						if (allinput[i].checked == true) {
							lineid = allinput[i].value.split("|")[0];
							mode = allinput[i].value.split("|")[1];
							var addr = "http://124.190.54.81/event/functions/adaptor.py?meth=stopsOnLine&mode=" + mode + "&lineid=" +lineid;
							getRequest(addr);
						}
					}
			}
			//
			//	alert(linenum);
			//}

		}

		function getData() {
			var addr = document.getElementById('reqstr').value;
			var xmlhttp = new XMLHttpRequest();
			xmlhttp.open('GET',addr, true);
			xmlhttp.send();
			xmlhttp.onreadystatechange=function() {
				if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
					if ((document.getElementById('reqstr').value).match('nearme')
					|| (document.getElementById('reqstr').value).match('stops-for-line')) {
						document.getElementById('data').value = xmlhttp.response;
						displayOnMap();
					}
					else if (document.getElementById('reqstr').value.match('destination')) {
						data = JSON.parse(xmlhttp.response);
						for (i = 0; i < data['values'].length; i++) {
							linenum = data['values'][i]['platform']['direction']['line']['line_number'];
							lineid = data['values'][i]['platform']['direction']['line']['line_id'];
							ttype = data['values'][i]['platform']['direction']['line']['transport_type'];
							linenumtype = linenum + "|" + ttype;
							if (linenum in linedata == false) {
								linedata[linenum] = data['values'][i]['platform']['direction']['line']['line_name'];
								document.getElementById('route').innerHTML += "<input type='checkbox' id='" + linenum
								 + "' value = '" + lineid + "|" + ttype + "'/>" + ttype + "-" + linedata[linenum] + "<br />";
							}
						}
						xmlhttp.response = '';
					}
					else {
						data = JSON.parse(xmlhttp.response);
					}
				}
			}
		}

		function displayOnMap() {
			initialize();
			stname = []
			data = JSON.parse(document.getElementById('data').value);
			if (document.getElementById('reqstr').value.search('nearme') > 0) {
				dataone = [];
				for (i = 0; i < data.length; i++) {
					dataone[i] = data[i]['result'];
				}
				data = dataone;
			}
			for (i = 0; i < data.length; i++) {
				lat = data[i]['lat'];
				lng = data[i]['lon'];
				stname.push(data[i]['location_name']);
				transtype = data[i]['transport_type'];
				stopid = data[i]['stop_id'];
				plotMap(transtype, lat, lng, stname[i], stopid);
			}

			map[0].setCenter(loc[0].getPosition());
			map[0].setZoom(13);
		}

		function plotMap(transtype, lat, lng, name, stopid) {
			loc[0] = new google.maps.Marker({position: poi, map: map[0]});
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

			contentStr = '<div id="info">' + name + '</div>';
			infowin = new google.maps.InfoWindow({content: contentStr});
			infowin.setPosition(event.latLng);
				//infowin.open(map[0], this);
				getRequest("http://124.190.54.81/event/functions/adaptor.py?meth=BND&mode=" + transtype + "&stopid=" + stopid);
			});

		}

		function getLoc() {
			navigator.geolocation.getCurrentPosition(
				function(pos) {
					a = pos.coords.latitude;
					b = pos.coords.longitude;
					origin = new google.maps.Marker({position: new google.maps.LatLng(a, b) });
					origin.setMap(map[0]);
				}
			);

		}

		function setLoc() {
			loc = [];
			google.maps.event.addListener(map[0], 'click', function(event) {
				poi = event.latLng;
				if (typeof(loc[0]) !== "undefined")  {
					for (var i = 0; i < loc.length; i++)
						loc[0].setMap(null);
				}
				loc[0] = new google.maps.Marker({position: poi, map: map[0]});
				map[0].setCenter(poi);
				map[0].setZoom(16);
			});
			}



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
				display: none;
			}

			#data {
				height: 100px;
			}

			#route {
				color: white;
				float: left;
				width: 150px;
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
print "<input type='button' value='getRoute' onclick='showRoute()'>"
print "<input id='reqstr' type='text' />"
print "<textarea id='data' rows='1'>"
print "</textarea>"
print "</form>"
print "<ul id='route'></ul><br />"
print "</body>"
print "</html>"