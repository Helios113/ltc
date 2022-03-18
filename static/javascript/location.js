const loc = $("#latlon");

const isLink = $("#link");

$(document).ready(function () {
    if (isValidHttpUrl(isLink.html())) {
        isLink.href = isLink.html();
    }
    const url = new URL(loc.html());
    const data = url.pathname.split(",");
    var map = new ol.Map({
        target: "map",
        layers: [
            new ol.layer.Tile({
                source: new ol.source.OSM(),
            }),
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat([data[1], data[0]]),
            zoom: url.search.substring(3),
        }),
    });
    var layer = new ol.layer.Vector({
        source: new ol.source.Vector({
            features: [
                new ol.Feature({
                    geometry: new ol.geom.Circle(
                        ol.proj.fromLonLat([data[1], data[0]]),
                        200 / url.search.substring(3)
                    ),
                }),
            ],
        }),
    });
    map.addLayer(layer);
});
map.addLayer(layer);
function isValidHttpUrl(string) {
    let url;

    try {
        url = new URL(string);
    } catch (_) {
        return false;
    }

    return url.protocol === "http:" || url.protocol === "https:";
}
