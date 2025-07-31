var tablinks = document.getElementsByClassName('tab-links');
var tabcontents = document.getElementsByClassName('tab-contents');

function opentab(tabname){
    for(tablink of tablinks){
        tablink.classList.remove('active-link');
    }
    for(tabcontent of tabcontents){
        tabcontent.classList.remove('active-tab');
    }
    event.currentTarget.classList.add('active-link');
    document.getElementById(tabname).classList.add('active-tab');
}


window.onscroll = function () {
    changeHeaderOnScroll();
  };
  
  function changeHeaderOnScroll() {
    var header = document.getElementById("header");
    if (window.scrollY > 50) { // When the scroll is more than 50px
      header.classList.add("scrolled"); // Add the 'scrolled' class
    } else {
      header.classList.remove("scrolled"); // Remove the 'scrolled' class
    }
  }