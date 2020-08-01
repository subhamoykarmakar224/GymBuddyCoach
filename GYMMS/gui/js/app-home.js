$(function () {
  // Default page init
  $.get('student.html', function (response) {
    $('.div-container').html(response);
  });

  // Sidenav init
  $(".sidenav").sidenav();

  // Navigation Control
  $(".menu-item-selected").on("click", function () {
    $(".menu-item-selected").removeClass("active");
    $(this).addClass("active");
    var option = $(this).text();
    if (option == 'Home') {
      $.get('home.html', function (response) {
        $('.div-container').html(response);
      });
    } else if (option == "Students") {
      $.get('student.html', function (response) {
        $('.div-container').html(response);
      });
    } else if (option == "Notification") {
      $.get('notification.html', function (response) {
        $('.div-container').html(response);
      });
    } else if (option == "Settings") {
      $.get('settings.html', function (response) {
        $('.div-container').html(response);
      });
    } else if (option == "Contact Us") {
      $.get('contactus.html', function (response) {
        $('.div-container').html(response);
      });
    } else {
      $.get('home.html', function (response) {
        $('.div-container').html(response);
      });
    }
  });

});
