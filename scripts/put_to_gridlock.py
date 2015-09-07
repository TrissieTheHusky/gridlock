import time
import requests
import logging

try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig() 
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

payload = {'description': 'TEST',
           'service': 'TEST',
           'status':  'up',
           'location': 'cuckooland',
           'env': 'prd',
           'timestamp': int(time.time())}
r = requests.put('http://localhost:5000/gridlock/api/v0.1/', json=payload)
print r.status_code
print r.raw
