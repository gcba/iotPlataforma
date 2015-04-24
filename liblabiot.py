
import time
import urllib
import json
import urllib2, base64
from config import Config
import random

# abrimos archivo de configuracion
def opencfg(name):

	with file(name) as f:
		cfg = Config(f)
		return cfg

cfg = opencfg('labiot.cfg')
listendpoints = opencfg('listpaths.cfg')

# asignamos los parametros de configuracion
# funcion para el request
def __request(username, password, url, query_args):

	try:
		request = urllib2.Request(url)
		base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
		request.add_data(query_args)
		request.add_header("Authorization", "Basic %s" % base64string)
		result = json.loads(urllib2.urlopen(request).read())
		return result
	except:
		return {}


def functpost():

	url = cfg.urlname
	username = cfg.username
	password = cfg.password
	sensor = cfg.sensor
	datatype = cfg.datatype
	datos = listendpoints.datos
	
	urlpath = url+datos[1]

	while True:
	
		query_args = urllib.urlencode({
			"id": sensor,
			"datatype1" : datatype[0],
			"data1": random.randrange(20),
			"datatype2" : datatype[1],
			"data2": random.randrange(80),
		})

		result = __request(username, password, urlpath, query_args)

		if result.get('codigo') == "200":
			print "timestamp", result['datos']['current_time_stamp']
			print datatype[0], result['datos']['data1']
			print datatype[1], result['datos']["data2"]
			print 30*"="
		else:
			print "fallid"
			print result

		time.sleep(10)


if __name__ == '__main__':
	functpost()