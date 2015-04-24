import time
import datetime
import urllib
import urlparse
import httplib
import json
import urllib2, base64
from config import Config

# abrimos archivo de configuracion
f = file('labiot.cfg')
cfg = Config(f)

# asignamos los parametros de configuracion
url = cfg.urlname
username = cfg.username
password = cfg.password
sensor = cfg.sensor
datatype = cfg.datatype

# listamos path de api
DATOS = [
	# {0} = id
	"/api/data/create",
	"/api/data/dynamic/create",
	"/api/data/{0}",
	"/api/data/{0}/last",
	"/api/data/{0}/status"
]

# creamos parametros
query_args = {
	"id": sensor,
	"datatype1" : datatype[0],
	"data1": "2",
	"datatype2" : datatype[1],
	"data2": "5"
}

urlpath = url+DATOS[1]
# funcion para el request
def __request(username, password, url, query_args):

	request = urllib2.Request(url)
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	request.add_data(urllib.urlencode(query_args))
	request.add_header("Authorization", "Basic %s" % base64string)
	result = json.loads(urllib2.urlopen(request).read())

	return result

print __request(username, password, urlpath, query_args)