function initialize() {
    /* event page map initialization */
    var position = $('#position').text();
    var pos = position.split(',');
    var location = new google.maps.LatLng(pos[0], pos[1]);
    var mapOptions = {
        center: location,
        scrollWheel: true,
        zoom: 15
    };
    var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
    var marker = new google.maps.Marker({
        position: location,
        map: map
    });
    $('#position').hide();
}

google.maps.event.addDomListener(window, 'load', initialize);
