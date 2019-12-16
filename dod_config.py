# configuration for dod

SERVER_PORT = 8088
USERS = {'zhaw': 'AllOGG4LimhWiLbYbZUsEs3mp'}

# Two roles available:
# frontend: presents /data endpoint with HTTP Digest Auth for the end user
# injector: presents /inject endpoint without Auth, which receives data from frontend and injects into mux
ROLES = ["frontend", "injector"]

INJECTOR_ALLOW_IPS = ["127.0.0.1"]
INJECTOR_HOST = "127.0.0.1"
INJECTOR_PORT = 8088
INJECTOR_FIFO = "/tmp/data-zhaw.fifo"