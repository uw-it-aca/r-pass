(function(m){

    $(document).ready(function() {

    	setContentHeight();
        $("#search-field").keyup(filterService);

    });

    $(m).resize(function(){
        setContentHeight();
    });

    function setContentHeight() {
        var winH = $(window).height(),
            headerH = $("#header").height();
        $("#main").height(winH - headerH);
    }

    function filterService() {
        var searchField = $("#search-field").val(),
            count = 0;

        $(".services ul li").each(function(index, element) {
            if ($(this).children('p').text().search(new RegExp(searchField, "i")) < 0) {
                $(this).fadeOut(200);
            } else {
                $(this).show();
                count++;
            }
        });
    }

})(this);

function make_random_password() {
     var chars = [],
         passchars = [];

     for (i=48; i < 127; i++) {
         chars.push(String.fromCharCode(i));
     }

     for (i = 0; i < 30; i++) {
         var rand = chars[Math.floor(Math.random() * chars.length)];
         passchars.push(rand);
     }

     $("#id_access_token").val(passchars.join(""));

     return false;
 }
