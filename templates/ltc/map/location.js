window.onload = prepare

function prepare() {
    if (!document.getElementById) {
        return false;
    }
    var submit = document.getElementById("button");
    submit.onclick = function () {
        clickButton();
    }
}

function clickButton() {
    let input = document.getElementById("location-input").value;
    codeAddress(input);
}

function codeAddress(allAddress) {

    map = new google.maps.Map(document.getElementById("map"), {
        center: {lat: 55.86474, lng: -4.25181},
        zoom: 18,
    });

    infoWindow = new google.maps.InfoWindow();

    // get your location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const pos = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                };
                infoWindow.setPosition(pos);
                infoWindow.setContent("Location found.");
                infoWindow.open(map);
                map.setCenter(pos);
            },
            () => {
                handleLocationError(true, infoWindow, map.getCenter());
            }
        );
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    }

    var geocoder = new google.maps.Geocoder();
    if (geocoder) {
        geocoder.geocode({
                'address': allAddress
            },
            function (results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    map.setCenter(results[0].geometry.location);
                    map.setZoom(16);
                    beachMarker.setPosition(results[0].geometry.location);
                    $('#lng').val(results[0].geometry.location.lng());
                    $('#lat').val(results[0].geometry.location.lat());
                } else {
                    alert("Load the map failed, the reason is " + status);
                }
            });
    }

    // add marker
    var beachMarker = new google.maps.Marker({map: map});
    var find_lat, find_lng;

    find_lat = e.latLng.lat();
    find_lng = e.latLng.lng();

    beachMarker.setPosition(e.latLng);
    $('#lng').val(find_lng);
    $('#lat').val(find_lat);
    alert()
    showWay(position.coords.longitude, find_lng, position.coords.latitude, find_lat);

}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(
        browserHasGeolocation
            ? "Error: The Geolocation service failed."
            : "Error: Your browser doesn't support geolocation."
    );
    infoWindow.open(map);
}

function showWay(longitude1, longitude2, latitude1, latitude2) {
    map.clearOverlays();
    var destinationA = new GLatLng(longitude1, latitude1);
    var destinationB = new GLatLng(longitude2, latitude2);
    var line1 = new GPolyline([destinationA, destinationB], "#C00080", 5, 0.7);
    map.setCenter(destinationB, 14);
    // drawline
    map.addOverlay(line1);

    showIcon(destinationA, " Starting Point! ");
    showIcon(destinationB, " Destination! ");
}

// Points out the starting points and destination icons 
function showIcon(point, contentInfo) {
    var truckIcon = new GIcon(G_DEFAULT_ICON);
    truckIcon.shadow = null;
    truckIcon.iconSize = new GSize(50, 50);
    truckIcon.iconAnchor = new GPoint(25, 25);
    truckIcon.infoWindowAnchor = new GPoint(25, 25);
    var markerOptions = {icon: truckIcon};
    var marker = new GMarker(point, markerOptions);
    map.addOverlay(marker, markerOptions);
    marker.openInfoWindowHtml(contentInfo);
    if (contentInfo != "") {
        GEvent.addListener(marker, " click ", function () {
            marker.openInfoWindowHtml(contentInfo);
        });
    }
}