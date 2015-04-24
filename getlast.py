import time
import json
import urllib2, base64
from config import Config
from liblabiot import opencfg

cfg = opencfg('labiot.cfg')
listendpoints = opencfg('listpaths.cfg')

url = cfg.urlname
username = cfg.username
password = cfg.password
sensor = cfg.sensor
datos = listendpoints.datos
datatype = cfg.datatype

if __name__ == '__main__':
	
	"""
		script que traer los datos enviados por liblabiot, cada 10 segundos.
		y los muestra en pantalla, con timestamp, y valores de los campos ['ANPS', 'VNOPS'].
	"""

	while True:

		try:
			endpoint = url+datos[4].format(sensor)
			request = urllib2.Request(endpoint)
			base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
			request.add_header("Authorization", "Basic %s" % base64string)
			result = json.loads(urllib2.urlopen(request).read())
		except:
			result = {}

		if result.get('codigo') == "200":
			print "timestamp", result['datos'][0]['date']
			print datatype[0], result['datos'][0]['data']
			print datatype[1], result['datos'][1]["data"]
			print 30*"="
		else:
			print "fallid"
			print result

		time.sleep(10)