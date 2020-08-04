(function () {
    window.addEventListener('scroll', function (ev) {
        var fixedNav = false,
            fixedCatelog = false,
            scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0
        if (scrollTop > 100) {
            fixedNav = true
            fixedCatelog = true
        }
        document.querySelector('nav').style.position = fixedNav ? 'fixed' : 'static'
        document.querySelector('main').style['padding-top'] = fixedNav ? '50px' : '0'
        var articleCatelog = document.querySelector('#catelog')
        if (articleCatelog) {
            articleCatelog.style.position = fixedCatelog ? 'fixed' : 'static'
        }
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