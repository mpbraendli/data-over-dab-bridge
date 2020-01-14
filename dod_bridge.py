#!/usr/bin/env python3
import time
import requests
from requests.auth import HTTPDigestAuth
import cherrypy
from cherrypy.lib import auth_digest
import sys
import configparser

config = configparser.ConfigParser()

if len(sys.argv) != 2:
    print("Usage: {} <config file>".format(sys.argv[0]))
    sys.exit(1)

config.read(sys.argv[1])

daemon = config['general'].getboolean('daemon')
server_host = config['general']['server_host']
server_port = config['general'].getint('server_port')
username = config['general']['username']
password = config['general']['password']

has_role_frontend = 'frontend' in config
if has_role_frontend:
    injector_host = config['frontend']['injector_host']
    injector_port = config['frontend'].getint('injector_port')

has_role_injector = 'injector' in config
if has_role_injector:
    injector_fifo = config['injector']['fifo']
    injector_logfile = config['injector']['logfile']

cherrypy.config.update({'server.socket_port': server_port})
cherrypy.config.update({'server.socket_host': server_host})

users = {username : password}
conf = {
   '/data': {
        'tools.auth_digest.on': True,
        'tools.auth_digest.realm': 'localhost',
        'tools.auth_digest.get_ha1': auth_digest.get_ha1_dict_plain(users),
        'tools.auth_digest.key': 'iw4jURBej6oPraM3mISaH0xat',
        'tools.auth_digest.accept_charset': 'UTF-8',
   },
   '/inject': {
        'tools.auth_digest.on': True,
        'tools.auth_digest.realm': 'localhost',
        'tools.auth_digest.get_ha1': auth_digest.get_ha1_dict_plain(users),
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
        if has_role_frontend:
            raise cherrypy.HTTPError(501, 'Not Implemented')
        cl = cherrypy.request.headers['Content-Length']
        body = cherrypy.request.body.read(int(cl))

        if not isinstance(body, (bytes, bytearray)):
            raise cherrypy.HTTPError(400, 'Bad Request')

        r = requests.post("http://{}:{}/inject".format(injector_host, injector_port),
                data=body,
                auth=HTTPDigestAuth(username, password))

        return """Response from injector:
        HTTP {} {}
        {}""".format(r.status_code, r.reason, r.text)

    @cherrypy.expose
    def inject(self):
        if has_role_injector:
            raise cherrypy.HTTPError(501, 'Not Implemented')

        with open(injector_fifo, "wb") as fifo:
            cl = cherrypy.request.headers['Content-Length']
            body = cherrypy.request.body.read(int(cl))
            fifo.write(body)

            if injector_logfile:
                with open(injector_logfile, "a") as logfd:
                    logfd.write("{}: {} bytes injected\n".format(
                        time.strftime("%Y-%m-%dZ%H:%M:%S", time.gmtime()),
                        cl))

        return "OK"

if __name__ == '__main__':
    if daemon:
        from cherrypy.process.plugins import Daemonizer
        d = Daemonizer(cherrypy.engine)
        d.subscribe()

    cherrypy.tree.mount(Root(), "/", conf)
    cherrypy.engine.start()
    cherrypy.engine.block()

