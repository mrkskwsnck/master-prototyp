/*
Copyright (C) 2020  Markus Kwaśnicki

This file is part of the prototype.

This prototype is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This prototype is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this prototype.  If not, see <https://www.gnu.org/licenses/>.
*/

var map = null;

function mapSetup() {
    map = L.map('map').fitWorld();

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
            + ', <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
        maxZoom: 19,
        detectRetina: true
    }).addTo(map);
    
    L.control.scale().addTo(map)

    markWifiCounter();
}

function toLocalPhenomenonTime(phenomenonTime) {
    var utcPhenomenonTime = new Date(phenomenonTime);
    var tzOffset = (new Date()).getTimezoneOffset() * 60000;    // Timezone offset in milliseconds
    var localPhenomenonTime = (new Date(utcPhenomenonTime - tzOffset)).toISOString().slice(0, -1);
    return localPhenomenonTime;
}

function onEachWifiCounter(feature, layer) {
    // Does this feature have a property named result?
    if (feature.properties && feature.properties.result) {
        var phenomenonTime = toLocalPhenomenonTime(feature.properties.phenomenonTime);
        var popupContent = '<div><b>PAX Counter</b></div><div>Anzahl: <span class="result">' + feature.properties.result
            + '</span></div><div>Zeitstempel: <span class="phenomenonTime">' + phenomenonTime + '</span></div>';
        layer.bindPopup(popupContent);
    }
}

function markWifiCounter() {
    // Get the Locations from the SensorThings server
    axios.get('http://sensorhub:8080/v1.0/Locations?$expand=Things/Datastreams/Observations($orderby=phenomenonTime%20desc)', {
        params: {
            /*
             * Due to CORS, param keys with a starting $-sign don't seem to work at all
             * See https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors/CORSMissingAllowOrigin
             */
        }
    }).then(function(success) {

        // Convert the Locations into GeoJSON Features
        var geoJsonFeatures = success.data.value.map(function(location) {
            return {
                type: 'Feature',
                geometry: location.location,
                properties: {
                    phenomenonTime: location.Things[0].Datastreams[0].Observations[0].phenomenonTime,
                    result: location.Things[0].Datastreams[0].Observations[0].result
                },
            };
        });

        // Create a GeoJSON layer, and add it to the map
        var geoJsonLayerGroup = L.geoJSON(geoJsonFeatures, {
            // Change the default marker to a circle
            pointToLayer: function(geoJsonPoint, latlng) {
                return L.circleMarker(latlng);
            },
            onEachFeature: onEachWifiCounter
        });
        geoJsonLayerGroup.addTo(map);

        // Zoom in the map so that it fits the Locations
        map.fitBounds(geoJsonLayerGroup.getBounds());
    });
}
