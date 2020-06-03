// preloader
$(window).load(function(){
    $('#login-anchor').click(function() {
        window.location.href = '/accounts/login/';
    });
    $('#register-anchor').click(function() {
        window.location.href = '/accounts/register/';
    });

    $('.preloader').fadeOut(1000); // set duration in brackets
});

$(function() {
    new WOW().init();
    $('.templatemo-nav').singlePageNav({
    	offset: 70
    });

    /* Hide mobile menu after clicking on a link
    -----------------------------------------------*/
    $('.navbar-collapse a').click(function(){
        $(".navbar-collapse").collapse('hide');
    });
})
