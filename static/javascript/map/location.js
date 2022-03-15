
const loc = $("#latlon");


$(document).ready(function () {
    const url = new URL(loc.html());
    
    const data = url.pathname.split(',');
    console.log();
    var map = new ol.Map({
        target: 'map',
        layers: [
          new ol.layer.Tile({
            source: new ol.source.OSM()
          })
        ],
        view: new ol.View({
          center: ol.proj.fromLonLat([data[1],data[0]]),
          zoom: url.search.substring(3)
        })
      });

});

