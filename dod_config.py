# configuration for dod

DAEMON = False

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8088
USERS = {'zhaw': 'AllOGG4LimhWiLbYbZUsEs3mp'}

# Two roles available:
# frontend: presents /data endpoint with HTTP Digest Auth for the end user
# injector: presents /inject endpoint without Auth, which receives data from frontend and injects into mux
ROLES = ["frontend", "injector"]

INJECTOR_HOST = "127.0.0.1"
INJECTOR_PORT = 8088
INJECTOR_FIFO = "/tmp/data-zhaw.fifo"

# for injector
INJECTOR_LOGFILE = 'dod_bridge.log'
