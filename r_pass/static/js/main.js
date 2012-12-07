(function(m){

	$(document).ready(function() {

    	setContentHeight();


	});

	$(m).resize(function(){

        setContentHeight();
	});



	function setContentHeight() {
        var winH = $(window).height();
        var headerH = $("#header").height();
        $("#main").height(winH - headerH);
    }

})(this);


function make_random_password() {
    var chars = []
    for (i=48; i < 127; i++) {
        chars.push(String.fromCharCode(i));
    }

    var passchars = []
    for (i = 0; i < 30; i++) {
        var rand = chars[Math.floor(Math.random() * chars.length)];
        passchars.push(rand);
    }

    var password = passchars.join("");

    document.getElementById("id_access_token").value = password;
    return false;
}

