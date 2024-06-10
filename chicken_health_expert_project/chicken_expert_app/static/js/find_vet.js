var map;
var service;
var infowindow;

function intialize(){
    var pyrmont = new google.maps.LatLng(-1.3193672, 36.7718402);
    map = new google.maps.Map(document.getElementById('map'), {
        center: pyrmont,
        zoom: 15
    });

    // Location autocomplete
    var input = document.getElementById('searchTextField');
    let autocomplete =  new google.maps.places.Autocomplete(input);
    autocomplete.bindTo('bounds', map);

    let marker = new google.maps.Marker({
        map: map,
        visible: false  //set initially visibility to false & make it visible only when a place is selected
    });

    google.maps.event.addListener(autocomplete, 'place_changed', () => {
        let place = autocomplete.getPlace();
        console.log(place);

        if(!place.geometry){
            console.log("Autocomplete's returned place contains no geometry");
            return;
        }

        // Adjust the map view to the selected place
        if(place.geometry.viewport){
            map.fitBounds(place.geometry.viewport);
        }else{
            map.setCenter(place.geometry.location);
            map.setZoom(17);
        }

        // update marker position & make it visible on the map
        marker.setPosition(place.geometry.location);
        marker.setVisible(true);

        let request = {
            location: place.geometry.location,
            radius: '500',
            type: ['veterinary_care']
        };

        service = new google.maps.places.PlacesService(map);
        service.nearbySearch(request, callback);
    })

}
// callback function executes whenever request is successful
function callback(results, status){
    if(status == google.maps.places.PlacesServiceStatus.OK){
        for(var i=0; i<results.length; i++){
            var place = results[i];
            createMarker(place);
        }
    }else{
        console.log('Places service status: ' + status);
    }
}

// create a marker(icon) for each location identified
function createMarker(place){
    var marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location
    });

    google.maps.event.addListener(marker, 'click', function (){
        alert(place.name);
        if(place.photos && place.photos.length > 0){
            window.open(place.photos[0].getUrl(), '_blank');
        }else{
            console.log('No photos available for this place');
            alert('No photos available for this place')
        }
    });
}
google.maps.event.addDomListener(window, 'load', intialize);
