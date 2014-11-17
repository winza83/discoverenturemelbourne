var map = [];
var markers = [];
var infowin;
var poi = '';
var linedata = {};
var stname = [];
var loc = [];
var datatemp;
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
			if (xmlhttp.response.match('http:')) {
				document.getElementById('reqstr').value = xmlhttp.response;
				getData();
			}
		}
	}
}

function getRoute() {
	initialize();
	allinput = document.getElementsByTagName('input');
	for (i = 0; i < allinput.length; i++) {
		if (allinput[i].type == 'checkbox') {
				loc[0] = new google.maps.Marker({position: poi, map: map[0]});
				if (allinput[i].checked == true) {
					linenum = allinput[i].value.split("|")[2];
					mode = allinput[i].value.split("|")[1];
					var addr = "http://124.190.54.81/event/functions/getlines.py?&mode=" + mode + "&linenum=" +linenum;
					if (mode == 'trains') {
						var addr = "http://124.190.54.81/event/functions/getlines.py?&mode=" + mode + "&linenum='" +linenum + "'";
						map[0].data.loadGeoJson(addr);
					}
					else {
						map[0].data.loadGeoJson(addr);
					}
				}
			}
	}
}

function stopsOnRoute() {
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
					if (!document.getElementById(lineid)) {
						linedata[linenum] = data['values'][i]['platform']['direction']['line']['line_name'];
						document.getElementById('route').innerHTML += "<input onchange='clearOthers(" + lineid + ")' type='checkbox' id='" + lineid
						 + "' value = '" + lineid + "|" + ttype + "|" + linenum + "'/>" + ttype + "-" + linedata[linenum] +
						 "<br />";
					}
				}
				xmlhttp.response = '';
			}
			else {
//						data = JSON.parse(xmlhttp.response);
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

function clearOthers(checkitem) {
	items = document.getElementsByTagName('input');
	for (i = 0; i < items.length; i++) {
		if (items[i].type ==  'checkbox') {
			items[i].checked = false;
		}
	}
	document.getElementById(checkitem).checked = true;
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
	else if (transtype == "train")  {
		icon = 'http://124.190.54.81/MTApp/train.png';
	}
	else {
		icon = 'http://124.190.54.81/MTApp/pt.png';
	}


	markers.push(new google.maps.Marker({
		position: new google.maps.LatLng(lat, lng),
		icon: icon,
		size: new google.maps.Size(15, 15),
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
		infowin.open(map[0], this);
		if (stopid != null) {
			getRequest("http://124.190.54.81/event/functions/adaptor.py?meth=BND&mode=" + transtype + "&stopid=" + stopid);
			}
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

function getEvents() {
	addr = 'http://124.190.54.81/event/data/output.xml';
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.open('GET',addr, true);
	xmlhttp.send();
	xmlhttp.onreadystatechange=function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			if (xmlhttp.response.match('http:')) {
				document.getElementById('data').value = '';
				parser = new DOMParser();
				datatemp = parser.parseFromString(xmlhttp.response, 'text/xml');
				datalst = datatemp.getElementsByTagName('item');

				for (i = 0; i < datalst.length; i++) {
					lat = datalst[i].getElementsByTagName('latitude')[0].innerHTML;
					lng = datalst[i].getElementsByTagName('longitude')[0].innerHTML;
					title = datalst[i].getElementsByTagName('title')[0].innerHTML;
					plotMap('event',lat,lng, title,null);
				}
			}
		}
	}
}