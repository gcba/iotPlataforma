import httplib, urllib
from time import sleep
import random
from pprint import pprint 

APY_KEY = ''

def post_things():
	
	field1 = random.randrange(231)
	field2 = random.randrange(31)

	params = urllib.urlencode({'field1': field1, 'field2': field2,'key':APY_KEY})
	headers = { "Content-type": "application/x-www-form-urlencoded", 'accept-charset': 'utf-8,*', 'cache-control': 'no-cache', \
	'accept-encoding': 'gzip,deflate,sdch', 'accept': 'text/plain', 'accept-language': 'es,en-US;q=0.8,en;q=0.6', \
	'user-agent': "Mozilla/5.0 (X11; Linux x86_64)", 'connection': 'keep-alive', 'DNT': 1 }
	httplib.HTTPSConnection.debuglevel = 1
	conn = httplib.HTTPSConnection("api.thingspeak.com:443")

	try:
		print "HEADERS REQUEST"
		print "-" * 40
		conn.request("POST", "/update", params, headers)
		response = conn.getresponse()
		res_headers = dict(response.getheaders() + [("status", response.status)])
		print "-" * 40
		print "HEADERS RESPONSE"
		print "-" * 40
		#pprint(res_headers)
		print "field1: {0}".format(field1)
		print "field2: {0}".format(field2)
		print "status: {0}".format(res_headers.get("status"))
		print "reason: {0}".format(response.reason)
		print "-" * 40
		#data = response.read()
		conn.close()
	except:
		print "connection failed"


if __name__ == '__main__':

	while True:
		post_things()
		sleep(8)