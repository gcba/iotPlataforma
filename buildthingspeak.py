#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib

from collections import deque, defaultdict
from socket import setdefaulttimeout
from pprint import pprint
from time import sleep, asctime
from urllib import urlencode
from cStringIO import StringIO
from random import randrange
from gzip import GzipFile
from json import loads

# import logging
# import ipdb
# ipdb.set_trace()

class TalkBack:
	"""
		TalkBack allows any device to act upon queued commands. 

		TalkBack Example

		The following steps would allow you to control a door that opens only once:
		Create a new TalkBack using the web interface.
		Add some queued commands using the web interface or API, such as "OPENDOOR", "CLOSEDOOR".
		If the door (with Wi-Fi and a connected motion sensor) senses someone nearby, execute the next command from ThingSpeak: "OPENDOOR".
		After 5 minutes of no motion detected, execute the next command from ThingSpeak: "CLOSEDOOR".
		When someone else approaches the door, execute the next command from ThingSpeak, which will be empty--the door won't open again until more commands are added to the queue.
	"""
	def __init__(self, instance, TalkBackID=None, TalkBackKEY=None):

		self.__idtalkback = TalkBackID
		self.__key = TalkBackKEY
		self.__ins = instance
		self.__settigs = {}

	def addcmd(self, **parameters):
		"""
			Add a TalkBack Command

			To add a TalkBack command, send an HTTP POST.
			There is no limit to the number of commands that a single TalkBack can have. 

			Valid parameters:
				command_string (string) - Command to be sent to your device. There is a limit of 255 characters per command_string.
				position (integer) - The position you want this command to appear in. 
					Any previous commands at or after this position will be shifted down. 
					If the position is left blank, the command will automatically be added to the end of the queue.

			The response will be the command ID, for example: 18
		"""
		path = "/talkbacks/{0}/commands".format(self.__idtalkback)
		__add = [
			"command_string", "position"
		]
		result = self.__ins._Channels__ins._before_insert("POST", True, path, {'api_key':self.__key}, __add, **parameters)
		return result

	def get_cmd(self, id):
		"""
			Get a TalkBack Command
			To show an existing TalkBack command, send an HTTP GET.

			Valid parameters:
				api_key (string) - API key for this specific TalkBack (required)

			The response will be the command string, for example: OPENDOOR
		"""
		path = "/talkbacks/{0}/commands/{1}".format(self.__idtalkback, id)
		result = self.__ins._Channels__ins._before_insert("GET", True, path, {'api_key':self.__key})
		return result

	def update_cmd(self, **parameters):
		"""
			Update a TalkBack Command
			To update an existing TalkBack command, send an HTTP PUT.
		
			Valid parameters:
				command_string (string) - Command to be sent to your device
				position (integer) - The position you want this command to appear in.

			The response will be the command string, for example: OPENDOOR
		"""
		__updcmd = [
			"command_string", "position"
		]		
		path = "/talkbacks/{0}/commands/{1}".format(self.__idtalkback, parameters.get("id"))
		del parameters['id']
		result = self.__ins._Channels__ins._before_insert("PUT", False, path, {'api_key':self.__key}, __updcmd, **parameters)
		return result

	def execute(self):
		"""
			Execute the Next TalkBack Command
			To execute the next TalkBack command in the queue (normally in position 1), send an HTTP GET or POST.

			Executing a command removes it from the queue, sets executed_at to the current time, sets position to null, 
			and reorders the remaining commands. 

			The response will be the command string, for example: OPENDOOR 
				If there are no commands left to execute, the response body will be empty.
		"""		
		path = "/talkbacks/{0}/commands/execute".format(self.__idtalkback)
		result = self.__ins._Channels__ins._before_insert("POST", False, path, {'api_key':self.__key})
		return result

	def delete_cmd(self, id):
		"""
			Delete a TalkBack Command	
				To delete an existing TalkBack command, send an HTTP DELETE.
				The response will be the deleted command string, for example: OPENDOOR		
		"""
		path = "/talkbacks/{0}/commands/{1}".format(self.__idtalkback, id)
		result = self.__ins._Channels__ins._before_insert("DELETE", False, path, {'api_key':self.__key})
		return result

	def update_execute(self, **parameters):
		"""
			Update a Channel and Execute the Next TalkBack Command

			The next TalkBack command in the queue (normally in position 1) can be executed at the same time a 
			Channel is updated by sending an HTTP GET or POST to https://api.thingspeak.com/update. 

			Executing a command removes it from the queue, sets executed_at to the current time, sets position to null, 
			and reorders the remaining commands. 

			Please note that the parameters for this action are different than other TalkBack commands. Since a Channel 
			is being updated, the api_key parameter refers to the Channel API write key, while the talkback_key refers 
			to the TalkBack API key.

			Valid parameters:
				talkback_key (string) - API key for this specific TalkBack (required)
				Additional parameters for updating a Channel can be found in the Channel API documentation. 

			The response will be the command string, for example: OPENDOOR
		"""
		__channel = [
			"name", "description", "elevation", \
			"field1", "field2" ,"field3" ,"field4" ,"field5" ,"field6" 
			,"field7", "field8", \
			"latitude" ,"longitude" ,"metadata" ,"name" ,"public_flag" ,"tags" ,"url"
		]

		path = "/update"
		result = self.__ins._Channels__ins._before_insert("PUT", False, "/update", {'api_key':self.__key}, __channel, **parameters)
		return result

	def delete_allcmd(self):
		"""		
			Delete All TalkBack Commands
			To delete all of a TalkBack's commands, send an HTTP DELETE
		"""
		path = "/talkbacks/{0}/commands".format(self.__idtalkback)
		result = self.__ins._Channels__ins._before_insert("DELETE", False, path, {'api_key':self.__key})
		return result

	def last_execute(self):
		"""
			Get the Last Executed Command
			To show the most recently executed TalkBack command.
			The response will be the command string, for example: OPENDOOR
		"""
		path = "/talkbacks/{0}/commands/last".format(self.__idtalkback)
		result = self.__ins._Channels__ins._before_insert("GET", True, path, {'api_key':self.__key})
		return result

	def list_cmd(self):
		"""
			To show all of a TalkBack's commands, send an HTTP GET. 
		"""
		path = "/talkbacks/{0}/commands".format(self.__idtalkback)
		result = self.__ins._Channels__ins._before_insert("GET", True, path, {'api_key':self.__key})
		return result

class Channels(TalkBack):
	
	"""
		Write API Key
			In order to update a channel, you need to know your Write API Key. If your Write API Key gets 
			compromised you can generate a new key. 

		Read Public API Key
			The Read API Key allows your application to read data from the API. You can generate
			multiple Read API Keys for different applications. 
			Follow these steps to get a Read API Key: 
			Select Channels
			Select the Channel to update
			Select Manage API Keys
			Select Generate New Read API Key
	"""
	
	def __init__(self, instance, result={}, keys={}):

		self.__ins = instance
		self.keys = keys
		self.settings = result
		self.settings.update(self.keys)

	def insert(self, **parameters):
		"""
			Sending Data
				o update a Channel feed, send an HTTP GET or POST.

			Valid parameters:
				field1 (string) - Field 1 data (optional)

				field2 (string) - Field 2 data (optional)
				field3 (string) - Field 3 data (optional)
				field4 (string) - Field 4 data (optional)
				field5 (string) - Field 5 data (optional)
				field6 (string) - Field 6 data (optional)
				field7 (string) - Field 7 data (optional)
				field8 (string) - Field 8 data (optional)
				lat (decimal) - Latitude in degrees (optional)
				long (decimal) - Longitude in degrees (optional)
				elevation (integer) - Elevation in meters (optional)
				status (string) - Status update message (optional)
				twitter (string) - Twitter username linked to ThingTweet (optional)
				tweet (string) - Twitter status update; see updating ThingTweet for more info (optional)
				created_at (datetime) - Date when this feed entry was created, in ISO 8601 format,
				for example: 2014-12-31 23:59:59 . Time zones can be specified via the timezone parameter (optional)
		"""
		valid = 0
		params = parameters.iteritems()
		if not valid:
			for key, value in params:
				if not key in ["field1", "field2", "field3", "field4", "field5", "field6", "field7", "field8",\
				"created_at", "status", "latitude", "longitude", "elevation", "location"]:
					del parameters[key]
		valid = 1
		self.__ins._ThingSpeak__send(**parameters)

	def update(self, **parameters):
		"""
			Update a Channel
				To update a Channel, send an HTTP PUT.

			Valid parameters:
				description (string) - Description of the Channel (optional)
				elevation (integer) - Elevation in meters (optional)
				field1 (string) - Field1 name (optional)
				field2 (string) - Field2 name (optional)
				field3 (string) - Field3 name (optional)
				field4 (string) - Field4 name (optional)
				field5 (string) - Field5 name (optional)
				field6 (string) - Field6 name (optional)
				field7 (string) - Field7 name (optional)
				field8 (string) - Field8 name (optional)
				latitude (decimal) - Latitude in degrees (optional)
				longitude (decimal) - Longitude in degrees (optional)
				metadata (text) - Metadata for the Channel, which can include JSON, XML, or any other data (optional)
				name (string) - Name of the Channel (optional)
				public_flag (true/false) - Whether the Channel should be public, default false (optional)
				tags (string) - Comma-separated list of tags (optional)
				url (string) - Webpage URL for the Channel (optional)
		"""

		self.__ins.rd = True
		if self.__ins.crd:
			path = "/channels/{0}.json".format(self.settings["id"])
		else:
			raise ValueError("sin crear canal")

		__channel = [
			"name", "description", "elevation", \
			"field1", "field2" ,"field3" ,"field4" ,"field5" ,"field6" 
			,"field7", "field8", \
			"latitude" ,"longitude" ,"metadata" ,"name" ,"public_flag" ,"tags" ,"url"
		]

		self.settings = self.__ins._before_insert("PUT", True, path, "account", __channel, **parameters)
		self.settings.update(self.keys)
		return self.settings

	def feed(self, **parameters): # get
		"""
			Get a Channel Feed
				To view a Channel feed, send an HTTP GET-

			Valid parameters:
				results (integer) Number of entries to retrieve, 8000 max, default of 100 (optional)
				days (integer) Number of 24-hour periods before now to include in feed (optional)
				start (datetime) Start date in format YYYY-MM-DD%20HH:NN:SS (optional)
				end (datetime) End date in format YYYY-MM-DD%20HH:NN:SS (optional)
				timezone (string) Timezone identifier for this request (optional)
				offset (integer) Timezone offset that results should be displayed in.
				status (true/false) Include status updates in feed by setting "status=true" (optional)
				metadata (true/false) Include Channel's metadata by setting "metadata=true" (optional)
				location (true/false) Include latitude, longitude, and elevation in feed by setting "location=true" (optional)
				min (decimal) Minimum value to include in response (optional)
				max (decimal) Maximum value to include in response (optional)
				round (integer) Round to this many decimal places (optional)

				Valid values: 10, 15, 20, 30, 60, 240, 720, 1440, "daily" (optional)
					timescale (integer or string) Get first value in this many minutes,
					sum (integer or string) Get sum of this many minutes, valid values
					average (integer or string) Get average of this many minutes
					median (integer or string) Get median of this many minutes
		"""
		__feed = [
			"results", "days", "start", "end", "timezone", "offset", "status", "metadata", "location", "min", "max", "round"
			"timescale", "sum", "average", "median"
		]
		path = "/channels/{0}/feeds.json".format(self.settings['id'])
		result = self.__ins._before_insert("GET", True, path, "write", __feed, **parameters)
		return result

	def clear(self): # get
		"""
			Clear a Channel
				To clear all feed data from a Channel, send an HTTP DELETE.
		"""

		path = "/channels/{0}/feeds.json".format(self.settings['id']) # DELETE
		result = self.__ins._ThingSpeak__insert("DELETE", path)
		return result

	def delete(self): # delete
		"""
			Delete a Channel
				To create a new Channel, send an HTTP DELETE.
		"""
		path = "/channels/{0}.json".format(self.settings['id']) # DELETE
		result = self.__ins._ThingSpeak__insert("DELETE", path)
		return result

	def fieldfeed(self, **parameters): # get
		"""
			Get a Channel Field Feed
				To view a Channel's field feed, send an HTTP GET.

			Valid parameters:
				nro_field (integer) umber of entries to retrieve, 8000 max, default of 100 (optional)
				results (integer) Number of entries to retrieve, 8000 max, default of 100 (optional)
				days (integer) Number of 24-hour periods before now to include in feed (optional)
				start (datetime) Start date in format YYYY-MM-DD%20HH:NN:SS (optional)
				end (datetime) End date in format YYYY-MM-DD%20HH:NN:SS (optional)
				timezone (string) Timezone identifier for this request (optional)
				offset (integer) Timezone offset that results should be displayed in.
				status (true/false) Include status updates in feed by setting "status=true" (optional)
				metadata (true/false) Include Channel's metadata by setting "metadata=true" (optional)
				location (true/false) Include latitude, longitude, and elevation in feed by setting "location=true" (optional)
				min (decimal) Minimum value to include in response (optional)
				max (decimal) Maximum value to include in response (optional)
				round (integer) Round to this many decimal places (optional)
				
				Valid values: 10, 15, 20, 30, 60, 240, 720, 1440, "daily" (optional)
					timescale (integer or string) Get first value in this many minutes
					sum (integer or string) Get sum of this many minutes
					average (integer or string) Get average of this many minutes
					median (integer or string) Get median of this many minutes
		"""

		__fieldfeed = [
			"results", "days", "start", "end", "timezone", "offset", "status", "metadata", "location", "min", "max", "round"
			"timescale", "sum", "average", "median"
		]
		
		path = "/channels/{0}/fields/{1}.json".format(self.settings['id'], parameters.get("nro_field")) # GET
		del parameters["nro_field"]
		result = self.__ins._before_insert("GET", True, path, "write", __fieldfeed, **parameters)
		return result
	
	def view(self): # get
		"""
			View a Channel
				To view a specific Channel, send an HTTP GET to https://api.thingspeak.com/channels/CHANNEL_ID.json .

		"""

		path = "/channels/{0}.json".format(self.settings['id']) # GET
		result = self.__ins._before_insert("GET", True, path, "account")
		return result

	def listpublic(self, **parameters): # 
		"""
			List Public Channels
				To view a list of public Channels, send an HTTP GET

			Valid parameters:
				page (integer) Page number to retrieve (optional)
				tag (string) Name of tag to search for (optional)
				username (string) Person's username that you want to search Channels for (optional)

				You can also search for Channels within a certain distance of a location by including the following location :
					latitude (decimal) - Latitude of location in degrees. (optional)
					longitude (decimal) - Longitude of location in degrees. (optional)
					distance (decimal) - Distance in kilometers from location. (optional)
		"""
		__publicChannels = [
			"page", "tag", "username", "latitude", "longitude", "distance"
		]

		path = "/channels/public.json" # GET
		result = self.__ins._before_insert("GET", True, path, "write", __publicChannels, **parameters)
		return result

	def status(self, **parameters): # get
		"""
			Get Status Updates
				To view a Channel's status updates, send an HTTP GET

			Valid parameters:
				timezone (string) Timezone identifier for this request (optional)
				offset (integer) Timezone offset that results should be displayed in.
		"""

		__status  = [ 
			"timezone", "offset"
		]

		path = "/channels/{0}/status.json".format(self.settings['id']) # GET
		result = self.__ins._before_insert(self, "GET", True, path, "write", __status, **parameters)
		return result

	def last(self, **parameters):
		"""
			Get Last Entry in a Field Feed
				To get the last entry in a Channel's field feed, send an HTTP GET.

			Valid parameters:
				field (string) name to field.
				timezone (string) Timezone identifier for this request (optional)
				offset (integer) Timezone offset that results should be displayed in.
				status (true/false) Include status updates in feed by setting "status=true" (optional)
				location (true/false) Include latitude, longitude, and elevation in feed by setting "location=true" (optional)
		"""

		__lastentry = [
			"field", "timezone", "offset", "status", "location"
		]

		path = "/channels/{0}/fields/{1}/last.json".format(self.settings['id'], parameters.get("field"))  # GET
		del parameters["field"]
		result = self.__ins._before_insert("GET", True, path, "write", __lastentry, **parameters)
		return result

	def view_data(self, callback):
		"""
			Viewing Data
		"""
		path = "/channels/{0}/feed.json".format(self.settings['id'])
		result = self.__ins._before_insert("GET", True, path, "write")
		return result

	def instalkback(self, TalkBackID, TalkBackKEY):
		return TalkBack(self, TalkBackID, TalkBackKEY)

class ThingSpeak(httplib.HTTPSConnection):

	"""
		API Keys
			Private / Public Channels
			By default, your channel is private and requires a Read API Key to access its feed. You can make
			a channel public which gives other users the ability to use your feed without a Read API Key. 

	"""

	URL = "api.thingspeak.com"
	TIMEOUT = 14000

	def __init__(self, accountkey=None, debug=0):

		self.time_zone = {"identifier":"America/Argentina/Buenos_Aires", \
			"description":"Buenos Aires", "current_offset":"UTC -03:00"}
		
		self.__apikey = accountkey
		self.__writekey = None
		self.__keytalkback = None
		self.__readkey = None

		self.crd = 0
		self.rd = 0
		self.rs = 0

		self.channel = {}
		self.headers = {
			"Content-type": "application/x-www-form-urlencoded",
			'cache-control': 'no-cache',
			'accept-encoding': 'gzip,deflate,sdch',
			'accept': 'text/plain; charset=utf-8', # 'application/json; charset=utf-8',
			'accept-language': 'es,en-US;q=0.8,en;q=0.6',
			'user-agent': "Mozilla/5.0 (X11; Linux x86_64)",
			'connection': 'keep-alive', 
			'DNT': 1 }

		setdefaulttimeout(self.TIMEOUT)
		httplib.HTTPSConnection.debuglevel = debug
		httplib.HTTPSConnection.__init__(self, "api.thingspeak.com")

	def addheaders(self, addhead={}):
        
		if len(addhead) > 1:
			self.headers.update(addhead)

	def __decoding(self, read):
		
		stream = StringIO(read)
		with GzipFile(mode="rb", fileobj=stream) as f:
			source = f.read()
			result = loads(source)
			return result

	def __req(self, method, path, params=None):
		
		reshead = {}

		if self.rd:
			self.headers['accept'] = 'application/json; charset=utf-8'
		else:
			self.headers['accept'] = 'text/plain; charset=utf-8'

		try:
			self.close()
			self._send_request(method, path, params, self.headers)
			response = self.getresponse()
		except Exception, e:
			self.close()
			raise ValueError("no me pude conectar {0}, {1}, {2}, {3}".format(method, path, params, e))

		if self.rs:
			reshead = dict(response.getheaders() + [("status", response.status)])
			self.rs = False
		else:
			reshead["status"] = response.status

		if reshead['status'] == 200:
			if self.rd:
				encoding = response.read()
				data = self.__decoding(encoding)
				self.rd = False
				return data
		elif reshead['status'] in (301, 302, 303, 307, 308):
			return ValueError("no me pude conectar redireccionamiento {0}".format(reshead['status']))
		elif reshead['status'] in (400, 401, 403, 404):
			return ValueError("no me pude conectar api_key o host, invalid {0}".format(reshead['status']))
		elif reshead['status'] in (502, 503, 504):
			return ValueError("no me pude conectar {0}".format(reshead['status']))
	
	def setkey(self, key):
		
		keys = ['read', 'account', 'write', 'talkback', 'talkbackaccount']

		if key in keys:
			return {"api_key":self.__readkey}
		elif key in keys:
			return {"api_key":self.__apikey}
		elif key in keys:
			return {"key":self.__writekey}
		elif key in keys:
			return {"api_key":self.__keytalkback}
		elif key in keys:
			return {"api_key":self.__apikey, "talkback_key":self.__keytalkback}
		else:
			return key

	def __insert(self, method="GET", path="/", key="account", validparams=[], **kwargs):

		params_update = self.setkey(key)

		if validparams and kwargs:
			
			for key in kwargs.keys():
				if key in validparams:
					params_update.update({key: kwargs[key]})

			sendparams = urlencode(params_update)
			result = self.__req(method, path, sendparams)

		else:

			sendparams = urlencode(params_update)
			result = self.__req(method, path, sendparams)

		if type(result) != ValueError:
			return result
		else:
			raise result

	def _before_insert(self, method, rd, path, key, validparams=[], **parameters):

		"""	

		"""

		self.rd = rd
		result = self.__insert(method, path, key, validparams, **parameters)
		return result

	def created(self, **parameters):
		"""
			Create a Channel
				To create a new Channel, send an HTTP POST.

			Valid parameters:
				description (string) - Description of the Channel (optional)
				elevation (integer) - Elevation in meters (optional)
				field1 (string) - Field1 name (optional)
				field2 (string) - Field2 name (optional)
				field3 (string) - Field3 name (optional)
				field4 (string) - Field4 name (optional)
				field5 (string) - Field5 name (optional)
				field6 (string) - Field6 name (optional)
				field7 (string) - Field7 name (optional)
				field8 (string) - Field8 name (optional)
				latitude (decimal) - Latitude in degrees (optional)
				longitude (decimal) - Longitude in degrees (optional)
				metadata (text) - Metadata for the Channel, which can include JSON, XML, or any other data (optional)
				name (string) - Name of the Channel (optional)
				public_flag (true/false) - Whether the Channel should be public, default false (optional)
				tags (string) - Comma-separated list of tags (optional)
				url (string) - Webpage URL for the Channel (optional)
		"""
		
		__channel = [
			"name", "description", "elevation",
			"field1", "field2" ,"field3" ,"field4" ,"field5" ,"field6" ,"field7", "field8",
			"latitude" ,"longitude" ,"metadata" ,"name" ,"public_flag" ,"tags" ,"url"
		]

		self.rd = True
		result = self.__insert("POST", "/channels.json", "account", __channel, **parameters)

		if type(result) != ValueError:
			self.crd = 1
			return Channels(self, result)
		else:
			raise result

	def instance(self, id, accountkey, writekey=None, readkey=None):
		"""
			le paso el numero del id del sensor, junto a una account api key 
		"""
		self.crd = True
		self.__apikey = accountkey
		self.__writekey = writekey
		self.__readkey = readkey
		self.infokeys = {
			"account" : accountkey,
			"write" : writekey,
			"read" : readkey,
			"id" : id
		}
		return Channels(self, {}, self.infokeys)

	def __send(self, **values):

		self.close()
		values.update({"api_key":self.__writekey})
		parameters = urlencode(values)

		try:
			self._send_request("POST", "/update", parameters, self.headers)
		except Exception, e:
			raise("error {0}".format(e))


if __name__ == '__main__':
	
	"""
		channel tiene que disponer de su api_key
		settings tiene que disponer de las api Keys de account + del sensor (Write, Read)
	"""
	channel = ThingSpeak(accountkey="K8P9HHY4RM85BUP8")

	sensor3 = channel.instance(id=27992, accountkey="K8P9HHY4RM85BUP8", writekey="IJI9SJDSAFJYDBR2", readkey="")
	sensor3.update(
		field1="heladera",
	 	field2="cocina",
	 	field3="luzbaño",
	 	field4="luzpasillo"
	)
	sensor3.insert(
		field1=1,
	 	field2=2
	 	field3=2
	 	field4=2
	)
	print sensor3.fieldfeed(nro_field=2)
	print sensor3.view()
	print sensor3.listpublic(username="lmuran")
	print sensor3.last(field="heladera")
	print sensor3.view_data()

	# armar un perfil del talkback + info del sensor
	talk1 = sensor3.instalkback(1494, "6KTBPLNPPZDE0INP")
	talk1.addcmd(command_string="LOLO")
	talk1.get_cmd(65670)
	talk2.update_cmd(id=65670, command_string="NUEVO")
	talk2.execute()
	talk2.delete_cmd(65670)
	talk2.list_cmd()
	talk2.last_execute()
	talk2.delete_allcmd()

	def whilepost(**values):
		
		while True:

			sleep(16)
			
			sensor1.insert(
				field1=1,
				field2=2,
				longitude=-53.000,
				latitude=-53.000
			)

			sensor2.insert(
				field1=1,
				longitude=-53.000,
				latitude=-53.000
			)
			
			sensor3.insert(
				field1=1,
				field2=2,
				field3=3,
				field4=0,			
				longitude=-53.000,
				latitude=-53.000
			)