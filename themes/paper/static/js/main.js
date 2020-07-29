(function () {
    window.addEventListener('scroll', function (ev) {
        var fixedNav = false
        if ((window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0) > 100) {
            fixedNav = true
        }
        document.querySelector('nav').style.position = fixedNav ? 'fixed' : 'static'
        document.querySelector('main').style['padding-top'] = fixedNav ? '50px' : '0'
    })
    var pager = document.querySelector('.paginator-input')
    pager && pager.addEventListener('keypress', function (ev) {
        if (ev.keyCode === 13) {
            var page = parseInt(this.value)
            if (page && page > 0) {
                page = page === 1 ? '' : page
                window.location.href = '/index' + page + '.html'
            }
        }
    })
})()