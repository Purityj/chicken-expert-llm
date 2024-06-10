document.getElementById('question-form').addEventListener('submit', function(event){
    event.preventDefault();
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(function(position){
            const locationData = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            document.getElementById('location-data').value = JSON.stringify(locationData);
            event.target.submit();
        });
    }else{
        alert('Geolocation is not supported by this browser');
        event.target.submit();
    }
});