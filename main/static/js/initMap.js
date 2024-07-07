document.addEventListener("DOMContentLoaded", function() {
    if (typeof kakao === "undefined") {
        console.error("Kakao map library not loaded.");
        return;
    }
    var container = document.getElementById('map'); 
    var options = {
        center: new kakao.maps.LatLng(36.817, 127.1422), 
        level: 3 
    };

    var map = new kakao.maps.Map(container, options);

    var markerPosition  = new kakao.maps.LatLng(36.817, 127.1422); 

    var marker = new kakao.maps.Marker({
        position: markerPosition
    });

    marker.setMap(map);
});
