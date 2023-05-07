function initializeMap(geojson) {
	var map = new google.maps.Map(document.getElementById('mapid'), {
		center: {lat: 37.8, lng: 128},
		zoom: 8
	});

	var tileLayer = new google.maps.ImageMapType({
		getTileUrl: function(tileCoord, zoom) {
			return "https://mt1.google.com/vt/lyrs=m&x=" + tileCoord.x + "&y=" + tileCoord.y + "&z=" + zoom;
		},
		tileSize: new google.maps.Size(256, 256),
		name: "Google Map",
		maxZoom: 18
	});

	map.mapTypes.set('google_map', tileLayer);
	map.setMapTypeId('google_map');

	var geojsonLayer = new google.maps.Data({
		style: function(feature) {
			return {
				strokeWeight: 1,
				strokeOpacity: 1,
				strokeColor: 'black',
				fillOpacity: 0
			};
		}
	});

	geojsonLayer.addGeoJson(geojson);

	geojsonLayer.addListener('click', function(event) {
		var feature = event.feature;
		alert("Name: " + feature.getProperty('SGG_NM') + "\nRisk Level: " + feature.getProperty('risk'));
	});

	geojsonLayer.setMap(map);
}