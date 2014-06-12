function initialize() {
    var mapOptions = {
        /* Initial Position: University Of Patras */
        center: new google.maps.LatLng(38.289230, 21.785369),
        scrollWheel: true,
        zoom: 14
    };

    /* Create the map object */
    var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

    /* Map Bounds */
    bounds = new google.maps.LatLngBounds();

    /* Parsing the api and adding all the available pins */
    $.get('/api/event_list', function(event_list) {
        var a = eval(event_list);
        var a_len = a.length;
        if (a_len == 0) {
            /* Bailing out when empty */
            return;
        }
        for (var i = 0; i < a_len; i++) {
            if (a[i].fields.hasOwnProperty('position')) {
                /* Determine position */
                var pos = a[i].fields['position'].split(',');
                if(typeof(pos[0]) === 'undefined' || typeof(pos[1]) === 'undefined') {
                    /* Bailing out when wrong coordinates */
                    continue;
                }
                var coords = new google.maps.LatLng(pos[0], pos[1]);

                /* Determine title */
                if (a[i].fields.hasOwnProperty('title')) {
                    tl = a[i].fields['title'];
                } else {
                    tl = ""
                }

                /* Creating the marker */
                var marker = new google.maps.Marker({
                    position: coords,
                    map: map,
                    title: tl
                });

                /*
                 * Adding click event with description to the marker. We are wrapping
                 * it in a function to avoid the "closure in a loop" JS problem.
                 */
                (function clf(marker, ev) {
                    /* Determine description */
                    var infowindow;
                    if (ev.fields.hasOwnProperty('description')) {
                        infowindow = new google.maps.InfoWindow({
                            content: "<p>" + ev.fields['description'] + "</p>" +
                            "<p><strong>Created: </strong>" + ev.fields['date_of_creation'] + "</p>" +
                            "<p><a href='/e/" + ev['pk'] + "'>Event page</a></p>"
                        });
                    } else {
                        infowindow = new google.maps.InfoWindow({
                            content: ""
                        });
                    }

                    google.maps.event.addListener(marker, 'click', function() {
                        map.setZoom(14);
                        map.setCenter(marker.getPosition());
                        infowindow.open(map, marker);
                    });
                })(marker, a[i]);

                /* We need this to make all the markers visible */
                bounds.extend(marker.getPosition());
            }
        }
        /* and finally actually fitting the bounds */
        map.fitBounds(bounds);
    });
};
google.maps.event.addDomListener(window, 'load', initialize);
