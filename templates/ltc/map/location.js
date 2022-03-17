const loc = $("#latlon");

const isLink = $("#link");

$(document).ready(function () {
    if (isValidHttpUrl(isLink.html())) {
        isLink.href = isLink.html();
    } else if (loc.html()) {
        const url = new URL(loc.html());
        const data = url.pathname.split(",");
        console.log();
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
    }
});

function isValidHttpUrl(string) {
    let url;

    try {
        url = new URL(string);
    } catch (_) {
        return false;
    }

    return url.protocol === "http:" || url.protocol === "https:";
}