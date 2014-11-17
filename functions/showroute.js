
xmlhttp = new XMLHttpRequest();
xmlhttp.open('GET','http://124.190.54.81/event/data/busroute.geojson', true);
xmlhttp.send();
data = JSON.parse(xmlhttp.response);