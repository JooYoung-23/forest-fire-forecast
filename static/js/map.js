let historicalOverlay;

function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 8,
    center: { lat: 37.823415370646885, lng: 128.2391451745438 },
    styles: [
        {
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#ebe3cd"
                }
            ]
        },
        {
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#523735"
                }
            ]
        },
        {
            "elementType": "labels.text.stroke",
            "stylers": [
                {
                    "color": "#f5f1e6"
                }
            ]
        },
        {
            "featureType": "administrative",
            "elementType": "geometry.stroke",
            "stylers": [
                {
                    "color": "#c9b2a6"
                }
            ]
        },
        {
            "featureType": "administrative.land_parcel",
            "elementType": "geometry.stroke",
            "stylers": [
                {
                    "color": "#dcd2be"
                }
            ]
        },
        {
            "featureType": "administrative.land_parcel",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#ae9e90"
                }
            ]
        },
        {
            "featureType": "landscape.natural",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#dfd2ae"
                }
            ]
        },
        {
            "featureType": "poi",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#dfd2ae"
                }
            ]
        },
        {
            "featureType": "poi",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#93817c"
                }
            ]
        },
        {
            "featureType": "poi.park",
            "elementType": "geometry.fill",
            "stylers": [
                {
                    "color": "#a5b076"
                }
            ]
        },
        {
            "featureType": "poi.park",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#447530"
                }
            ]
        },
        {
            "featureType": "road",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#f5f1e6"
                }
            ]
        },
        {
            "featureType": "road.arterial",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#fdfcf8"
                }
            ]
        },
        {
            "featureType": "road.highway",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#f8c967"
                }
            ]
        },
        {
            "featureType": "road.highway",
            "elementType": "geometry.stroke",
            "stylers": [
                {
                    "color": "#e9bc62"
                }
            ]
        },
        {
            "featureType": "road.highway.controlled_access",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#e98d58"
                }
            ]
        },
        {
            "featureType": "road.highway.controlled_access",
            "elementType": "geometry.stroke",
            "stylers": [
                {
                    "color": "#db8555"
                }
            ]
        },
        {
            "featureType": "road.local",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#806b63"
                }
            ]
        },
        {
            "featureType": "transit.line",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#dfd2ae"
                }
            ]
        },
        {
            "featureType": "transit.line",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#8f7d77"
                }
            ]
        },
        {
            "featureType": "transit.line",
            "elementType": "labels.text.stroke",
            "stylers": [
                {
                    "color": "#ebe3cd"
                }
            ]
        },
        {
            "featureType": "transit.station",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#dfd2ae"
                }
            ]
        },
        {
            "featureType": "water",
            "elementType": "geometry.fill",
            "stylers": [
                {
                    "color": "#b9d3c2"
                }
            ]
        },
        {
            "featureType": "water",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#92998d"
                }
            ]
        }
        ],
        });

    const imageBounds = {
    north: 38.61614978034236,
    south: 37.01963991670794,
    east: 129.3610087713474,
    west: 127.09315231004376,
    };

    historicalOverlay = new google.maps.GroundOverlay(
        "../static/images/slope_gw.png",
        imageBounds
    );
    historicalOverlay.setMap(map);
	putLayerOnMap(map, '../static/data/Gangwon_regions.geojson');
}

window.initMap = initMap;

function putLayerOnMap(map, pathOfGeoJson) {
    var xhr = new XMLHttpRequest();

    xhr.open('GET', pathOfGeoJson, true);
    xhr.onload = function() {    
        if (xhr.status === 200) {
            var geojson = JSON.parse(xhr.responseText);
            console.log(geojson)

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
                var nameElement = document.getElementById('name');
                var riskElement = document.getElementById('risk');

                nameElement.innerHTML = feature.getProperty('SGG_NM');
                riskElement.innerHTML = feature.getProperty('risk');

                var infoBox = document.getElementById('intro');
                infoBox.style.display = 'block';

                window.location.href = '#intro';
            });

            geojsonLayer.setMap(map);
        } else {
            console.log('Failed to load Gangwon_regions file');
        }
    };

    xhr.send();
}