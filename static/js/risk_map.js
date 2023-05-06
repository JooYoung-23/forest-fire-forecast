function initializeMap(geojson) {
	var map = L.map('mapid').setView([37.8, 128], 8);

	L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		maxZoom: 18,
		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
			'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		id: 'mapbox/streets-v11',
		tileSize: 512,
		zoomOffset: -1
	}).addTo(map);

	L.geoJSON(geojson, {
		style: function(feature) {
			return {
				weight: 1,
				opacity: 1,
				color: 'black',
				fillOpacity: 0
			};
		},
		onEachFeature: function(feature, layer) {
			layer.on('click', function(e) {
				alert("Name: " + feature.properties.SGG_NM + "\nRisk Level: " + feature.properties.risk);
			});
		}
	}).addTo(map);
}