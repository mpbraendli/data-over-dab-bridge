#!/usr/bin/env python3
from dod_config import *
import requests
from requests.auth import HTTPDigestAuth

print("Sending data request")

body = "THIS IS TEST DATA".encode()

user, passwd = tuple(USERS.items())[0]

print("Digest auth with {}:{}".format(user, passwd))

r = requests.post("http://{}:{}/data".format(INJECTOR_HOST, INJECTOR_PORT),
        data=body,
        auth=HTTPDigestAuth(user, passwd))

print("""Response from injector:
        HTTP {} {}
        {}""".format(r.status_code, r.reason, r.text))
