#!/usr/bin/env python3
import time
import requests
from requests.auth import HTTPDigestAuth
import cherrypy
from cherrypy.lib import auth_digest

from dod_config import *

cherrypy.config.update({'server.socket_port': SERVER_PORT})
cherrypy.config.update({'server.socket_host': SERVER_HOST})

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

        with open(INJECTOR_FIFO, "wb") as fifo:
            cl = cherrypy.request.headers['Content-Length']
            body = cherrypy.request.body.read(int(cl))
            fifo.write(body)

            if INJECTOR_LOGFILE:
                with open(INJECTOR_LOGFILE, "a") as logfd:
                    logfd.write("{}: {} bytes injected\n".format(
                        time.strftime("%Y-%m-%dZ%H:%M:%S", time.gmtime()),
                        cl))

        return "OK"

if __name__ == '__main__':
    if DAEMON:
        from cherrypy.process.plugins import Daemonizer
        d = Daemonizer(cherrypy.engine)
        d.subscribe()

    cherrypy.tree.mount(Root(), "/", conf)
    cherrypy.engine.start()
    cherrypy.engine.block()

