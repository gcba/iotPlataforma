var ThingSpeakClient = require('thingspeakclient')
	, config = require('./config.json')
	, client = new ThingSpeakClient()
	, READ_API_KEY = config["ThingSpeak"]["API_KEY_ACCOUNT"]

var cb = function(err, res){
	if (err)
		throw err
}

/*
	https://github.com/imwebgefunden/thingspeakclient_node

	client.attachChannel(channelId, { writeKey: WRITE_API_KEY, readKey: READ_API_KEY}, cb);

	- same as API-Method "Retrieving a Field Feed"
	client.getFieldFeed(channelId, fieldId, query, callback);

	- same as API-Method "Retrieving the Last Entry in a Field Feed"
	client.getLastEntryInFieldFeed(channelId, fieldId, query, callBack);

	- same as API-Method "Retrieving Status Updates"
	client.getStatusUpdates(channelId, query, callBack);

	- same as API-Method "Retrieving Channel Feeds"
	client.getChannelFeeds(channelId, query, callBack);

	- same as API-Method "Retrieving the Last Entry in Channel Feed"
	client.getLastEntryInChannelFeed(channelId, query, callBack);
*/

client.attachChannel(ID_CHANNEL, { readKey: READ_API_KEY}, cb);

setInterval(function(){
	client.getLastEntryInChannelFeed(ID_CHANNEL, function(err, res){
		if (err)
			throw err
		console.log(res)
	});
}, 15000)
