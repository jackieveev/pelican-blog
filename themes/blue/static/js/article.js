(function(){
    window.addEventListener('scroll', function (ev) {
        var fixed = false
            scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0
        if (scrollTop > 60) {
            fixed = true
        }
        document.querySelector('#article-catelog').style['position'] = fixed ? 'fixed' : 'static'
        document.querySelector('#article-reader-operations').style['position'] = fixed ? 'fixed' : 'absolute'
    })
})();