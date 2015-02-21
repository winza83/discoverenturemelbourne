addr = "https://api.foursquare.com/v2/venues/explore?client_id=HNJCPQZN3AXL4QG3ZDUW3POMPFOMUA432F4IKTLUP3RXKWEF&client_secret=BRDNLNHXOVOOORNDM30HBN3W5VRXMT5EMTFKZSOCHHD2QV5J&v=20130815&ll=-37.86387695214252,145.08092567324638&radius=1000&query=food";

xmlhttp = new XMLHttpRequest();
xmlhttp.open('GET',addr, true);
xmlhttp.send();


	data = JSON.parse(xmlhttp.responseText);
	venues = [];

	for (var i = 0; i < data['response']['groups'][0]['items'].length; i++) {
		venues.push(data['response']['groups'][0]['items'][i]['venue']['name']);
	}


//if (xmlhttp.readyState == 4 and xmlhttp.status == 200) {

	data = JSON.parse(xmlhttp.responseText);
	venues = [];

	for (var i = 0; i < data['response']['groups'][0]['items'].length; i++) {
		venues.push(data['response']['groups'][0]['items'][i]['venue']['name']);
	}

//}