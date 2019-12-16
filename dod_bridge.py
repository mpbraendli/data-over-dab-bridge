#!/usr/bin/env python3
import requests
from requests.auth import HTTPDigestAuth
import cherrypy
from cherrypy.lib import auth_digest

from dod_config import *

cherrypy.config.update({'server.socket_port': SERVER_PORT})


conf = {
   '/data': {
        'tools.auth_digest.on': True,
        'tools.auth_digest.realm': 'localhost',
        'tools.auth_digest.get_ha1': auth_digest.get_ha1_dict_plain(USERS),
        'tools.auth_digest.key': 'iw4jURBej6oPraM3mISaH0xat',
        'tools.auth_digest.accept_charset': 'UTF-8',
   },
   '/inject': {
        'tools.auth_digest.on': True,
        'tools.auth_digest.realm': 'localhost',
        'tools.auth_digest.get_ha1': auth_digest.get_ha1_dict_plain(USERS),
        'tools.auth_digest.key': 'iw4jURBej6oPraM3mISaH0xat',
        'tools.auth_digest.accept_charset': 'UTF-8',
   }
}

class Root(object):
    @cherrypy.expose
    def index(self):
        return "Data-over-DAB bridge"

    @cherrypy.expose
    @cherrypy.tools.accept(media="application/octet-stream")
    def data(self):
        if "frontend" not in ROLES:
            raise cherrypy.HTTPError(501, 'Not Implemented')
        cl = cherrypy.request.headers['Content-Length']
        body = cherrypy.request.body.read(int(cl))

        if not isinstance(body, (bytes, bytearray)):
            raise cherrypy.HTTPError(400, 'Bad Request')

        username, passwd = tuple(USERS.items())[0]

        r = requests.post("http://{}:{}/inject".format(INJECTOR_HOST, INJECTOR_PORT),
                data=body,
                auth=HTTPDigestAuth(username, passwd))

        return """Response from injector:
        HTTP {} {}
        {}""".format(r.status_code, r.reason, r.text)

    @cherrypy.expose
    def inject(self):
        if "injector" not in ROLES:
            raise cherrypy.HTTPError(501, 'Not Implemented')
        if cherrypy.request.remote.ip not in INJECTOR_ALLOW_IPS:
            raise cherrypy.HTTPError(403, 'Forbidden')

        with open(INJECTOR_FIFO, "wb") as fifo:
            cl = cherrypy.request.headers['Content-Length']
            body = cherrypy.request.body.read(int(cl))
            fifo.write(body)

        return "OK"

if __name__ == '__main__':
   cherrypy.quickstart(Root(), '/', conf)

