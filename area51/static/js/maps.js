function initialize() {
    /* position University Of Patras */
    var latlng = new google.maps.LatLng(38.289230, 21.785369);

    var mapOptions = {
        center: latlng,
        scrollWheel: false,
        zoom: 14
    };

    var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
    $.get('/api/event_list', function(event_list) {
        a = eval(event_list);
        var a_len = a.length;
        for (var i = 0; i < a_len; i++) {
            $.each(a[i].fields, function(key, value) {
                if (key == 'position') {
                   var pos = value.split(',')
                   var location = new google.maps.LatLng(pos[0], pos[1]);
                   var marker = new google.maps.Marker({
                       position: location,
                       map: map,
                   });
                }
            });
        }
    });
};
google.maps.event.addDomListener(window, 'load', initialize);
