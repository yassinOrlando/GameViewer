var dark = document.querySelector("nav input[name='dark-mode']")
dark.addEventListener( 'change', function() {
    let html = document.querySelector('html')
    if(this.checked) {
        html.className = "html-dark"
    } else {
        html.className = "html"
    }
});

console.log(dark)