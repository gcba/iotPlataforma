import httplib

from pprint import pprint
from time import sleep, asctime
from urllib import urlencode
from cStringIO import StringIO
from random import randrange
from gzip import GzipFile
from json import loads


with open("./config.json") as f:
    config = json.loads(f.read())
	APY_KEY = config["ThingSpeak"]["ACCOUNT_API_KEY"].encode("utf-8")

def readresponse(read):

	stream = StringIO(read)
	with GzipFile(mode="rb", fileobj=stream) as f:
		source = f.read()
		datajson = loads(source)
		return datajson

def post_things(debug=0, result=0):

	field1 = randrange(231)
	field2 = randrange(31)
	created_at = asctime()

	params = urlencode({
		'field1': field1, 
		'field2': field2, 
		'created_at': created_at, 
		'key':APY_KEY
	})
	
	headers = {
		"Content-type": "application/x-www-form-urlencoded", \
		'accept-charset': 'utf-8,*', \
		'cache-control': 'no-cache', \
		'accept-encoding': 'gzip,deflate,sdch', \
		'accept': 'text/plain', \
		'accept-language': 'es,en-US;q=0.8,en;q=0.6', \
		'user-agent': "Mozilla/5.0 (X11; Linux x86_64)", \
		'connection': 'keep-alive', \
		'DNT': 1 
	}
	
	httplib.HTTPSConnection.debuglevel = debug
	conn = httplib.HTTPSConnection("api.thingspeak.com:443")

	try:
		if debug:
			print "-" * 40
			print "NEW REQUEST"
			print "-" * 40
			print "HEADERS REQUEST"
			print "-" * 40
		conn.request("POST", "/update.json", params, headers)
		response = conn.getresponse()
		if debug:
			res_headers = dict(response.getheaders() + [("status", response.status)])
			print "-" * 40
			print "HEADERS RESPONSE"
			print "-" * 40
			pprint(res_headers)
		if result:
			print "-" * 40
			print "RESULT RESPONSE"
			print "-" * 40
			dataencoding = response.read()
			data = readresponse(dataencoding)
			pprint(data)
		conn.close()
	except:
		print "connection failed"

if __name__ == '__main__':

	while True:
		post_things(debug=1, result=0)
		sleep(18)