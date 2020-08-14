(function(){
    var changedByClick = false
    window.addEventListener('scroll', function (ev) {
        var fixed = false
            scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0
        if (scrollTop > 60) {
            fixed = true
        }
        document.querySelector('#article-catelog').style['position'] = fixed ? 'fixed' : 'static'
        document.querySelector('#article-reader-operations').style['position'] = fixed ? 'fixed' : 'absolute'
        document.querySelector('#back-to-top').style['visibility'] = fixed ? 'visible' : 'hidden'
        if (changedByClick) {
            changedByClick = false
            return
        }
        var headings = document.querySelectorAll('.article-headings')
        for (var i = 0; i < headings.length; i++) {
            var top = headings[i].getBoundingClientRect().top
            if (top > 0) {
                var current = document.querySelector('.current-heading')
                if (current) {
                    current.classList.remove('current-heading')
                }
                var aTag = document.querySelector('a[href="#' + headings[i].lastElementChild.id + '"]')
                if (aTag) {
                    aTag.parentElement.classList.add('current-heading')
                }
                break
            }
        }
    })

    var catelog = document.querySelector('#article-catelog')
    if (catelog) {
        catelog.addEventListener('click', function (ev) {
            if (ev.srcElement.href && ev.srcElement.href.indexOf('#article-anchor-') !== -1) {
                var current = document.querySelector('.current-heading')
                if (current) {
                    current.classList.remove('current-heading')
                }
                changedByClick = true
                ev.srcElement.parentElement.classList.add('current-heading')
            }
        })
    }
})();