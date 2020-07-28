(function () {
    window.addEventListener('scroll', function (ev) {
        var visible = true
        if (window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0) {
            visible = false
        }
        document.querySelector('.my-profile').style.display = visible ? 'block' : 'none'
        document.querySelector('main').style['padding-top'] = visible ? '150px' : '50px'
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