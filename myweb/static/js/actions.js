var dark = document.querySelector("nav input[name='dark-mode']")
var html = document.querySelector('html')

dark.addEventListener( 'change', function() {
    if(this.checked) {
        html.className = "html-dark"
        sessionStorage['mode'] = true
    } else {
        html.className = "html"
        sessionStorage.removeItem('mode')
    }
});

window.onload = function() {
    if( typeof sessionStorage['mode'] !== 'undefined'){
        html.className = "html-dark"
        dark.checked = true
    } else {
        html.className = "html"
        dark.checked = false
    }
};


document.addEventListener("DOMContentLoaded", function() {
    [].forEach.call(document.querySelectorAll('.dropimage'), function(img){
      img.onchange = function(e){
        var inputfile = this, reader = new FileReader();
        reader.onloadend = function(){
          inputfile.style['background-image'] = 'url('+reader.result+')';
        }
        reader.readAsDataURL(e.target.files[0]);
      }
    });
  });