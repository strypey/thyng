from paste.httpserver import serve
import sys
from webob import Request
from wsgifilter import proxyapp

import rewritelinks


class ProxyApp(object):

    def __init__(self):
        self.proxies = {
            'thyng': proxyapp.ForcedProxy(remote="http://django:8000/",
                                          force_host=True),
            'trac': proxyapp.ForcedProxy(remote="http://trac:8001/",
                                         force_host=True)
        }
        
    def __call__(self, environ, start_response):
        req = Request(environ).copy()
        req.path_info = req.path_info.lstrip("/")
        resp = req.get_response(self.proxies['thyng'])

        if resp.status_code != 305:
            return resp(environ, start_response)

        subreq = Request(dict(environ)).copy()
        container = resp.headers['X-Thyng-Container-Url'].lstrip("/")
        featurelet = resp.headers['X-Thyng-Featurelet-Slug'].lstrip("/")
        instance = resp.headers['X-Thyng-Featurelet-Instance'].rstrip("/")
        path_info = (
            instance + "/" +
            resp.headers['X-Thyng-Path-Info'].lstrip("/")).lstrip("/")
        subreq.path_info = path_info
        proxy = resp.headers['Location']
        resp = subreq.get_response(self.proxies[proxy])
        resp = rewritelinks.rewrite_links(
            req, resp,
            'http://trac:8001/' + instance,
            'http://django:8000/' + container.strip('/') + '/' + featurelet,
            'http://trac:8001/' + subreq.path_info)
        return resp(environ, start_response)

if __name__ == '__main__':
    serve(ProxyApp(), host='0.0.0.0', port=sys.argv[-1])
