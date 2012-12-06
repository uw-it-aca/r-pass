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