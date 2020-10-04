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


