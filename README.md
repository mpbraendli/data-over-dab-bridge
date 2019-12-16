Data over DAB bridge
====================

One single program has two roles:

1. Offer HTTP endpoint in `dod-bridge-webserver`
  * HTTP POST to `/data` shall contain the DAB packet mode packets as returned by `wrap_data()`
  * Sends the data to the injector, using HTTP POST to `/inject`

2. Carry DAB packets from web-server to `dod-bridge-injector`
  * HTTP POST to `/inject` with the same contents as for `/data`
  * Writes to fifo

For both:
  * MIME type shall be `application/octet-stream`
  * Authenticated (HTTP digest)

Deploy
------

```
python -m venv dod
cd dod
source bin/activate
pip install requests cherrypy
```
