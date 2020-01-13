#!/usr/bin/env python3
import requests
from requests.auth import HTTPDigestAuth

USERS = {'zhaw': 'AllOGG4LimhWiLbYbZUsEs3mp'}
INJECTOR_HOST = "127.0.0.1"
INJECTOR_PORT = 8088
url = 'data'

print("Sending data request")

body = "THIS IS TEST DATA".encode()

user, passwd = tuple(USERS.items())[0]

print("Digest auth with {}:{}".format(user, passwd))

r = requests.post("http://{}:{}/{}".format(INJECTOR_HOST, INJECTOR_PORT, url),
        data=body,
        auth=HTTPDigestAuth(user, passwd))

print("""Response from injector:
        HTTP {} {}
        {}""".format(r.status_code, r.reason, r.text))
