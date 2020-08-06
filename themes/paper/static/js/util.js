(function() {
    function getQueryString(obj) {
        var keys = Object.keys(obj), qsComponent = []
        for (var i = 0; i < keys.length; i++) {
            var value = obj[keys[i]]
            if (value === null || value === undefined) {
                value = ''
            }
            qsComponent.push(encodeURIComponent(keys[i]) + '=' + encodeURIComponent(obj[keys[i]]))
        }
        if (qsComponent.length) {
            return '?' + qsComponent.join('&')
        }
        return ''
    }
    function request(opt) {
        var url = opt.url, method = opt.method || 'GET', req = new XMLHttpRequest(),
            qs = getQueryString(opt.params || {}), data = opt.data
        req.open(method, url + qs, true)
        req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
        req.send(data)
        req.onreadystatechange = function() {
            if (this.readyState === 4 && this.status === 200) {
                return opt.success({
                    status: this.status,
                    response: this.response,
                    responseText: this.responseText,
                    responseType: this.responseType,
                    responseURL: this.responseURL
                })
            }
        }
    }
    window.http = request
})();