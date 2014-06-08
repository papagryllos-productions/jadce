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
        for (var i = 0; i < a_len; i++) {
            if (a[i].fields.hasOwnProperty('position')) {
                /* Determine position */
                var pos = a[i].fields['position'].split(',');
                if(typeof(pos[0]) === 'undefined' || typeof(pos[1]) === 'undefined') {
                    continue;
                }
                var coords = new google.maps.LatLng(pos[0], pos[1]);

                /* Determine title */
                if (a[i].fields.hasOwnProperty('title')) {
                    tl = a[i].fields['title'];
                } else {
                    tl = ""
                }

                /* Determine description */
                var infowindow;
                if (a[i].fields.hasOwnProperty('description')) {
                    infowindow = new google.maps.InfoWindow({
                        content: "<p>" + a[i].fields['description'] + "</p>" +
                        "<p><strong>Created: </strong>" + a[i].fields['date_of_creation'] + "</p>" +
                        "<p><a href='/e/" + a[i]['pk'] + "'>Event page</a></p>"
                    });
                } else {
                    infowindow = new google.maps.InfoWindow({
                        content: ""
                    });
                }

                /* creating the marker */
                var marker = new google.maps.Marker({
                    position: coords,
                    map: map,
                    title: tl
                });


                /* adding some events to the marker */
                google.maps.event.addListener(marker, 'click', function() {
                    map.setZoom(14);
                    map.setCenter(marker.getPosition());
                    infowindow.open(map,marker);
                });

                /* we need this to put all the markers in the window */
                bounds.extend(marker.getPosition());
            }
        }
    });
    /* and finally actually fitting the bounds */
    map.fitBounds(bounds);
};
google.maps.event.addDomListener(window, 'load', initialize);
