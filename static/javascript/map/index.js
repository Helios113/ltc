let map, infoWindow;

function initMap() {

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

}
// # Will handle the location error and pop-up message
function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(
        browserHasGeolocation
            ? "Error: The Geolocation service failed."
            : "Error: Your browser doesn't support geolocation."
    );
    infoWindow.open(map);
}