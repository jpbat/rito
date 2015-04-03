# -*- coding: utf-8 -*-
#!/usr/bin/env python

import json
import utils
import requests

baseUrl = "https://euw.api.pvp.net/"
apiKey = "abca4714-5ed2-4e2e-91ff-a379b9d8ed1d"

# Returns a JSON list containing ids from URF games
def getUrfGames(region, date):

	url = "/api/lol/" + region + "/v4.1/game/ids"

	payload = {'api_key': apiKey, 'beginDate' : utils.convertToEpoch(date)}
	requestUrl = baseUrl + url
	
	try:
		response = requests.get(requestUrl, params=payload).text
	except Exception, e:
		print e

	return json.loads(response)

# Returns the full data from a match using its gameId, including timeline
def getGameById(region, gameId):

	url = "api/lol/" + region + "/v2.2/match/" + str(gameId)

	payload = {'api_key': apiKey, 'includeTimeline' : 'true'}
	requestUrl = baseUrl + url
	
	try:
		response = requests.get(requestUrl, params=payload).text
	except Exception, e:
		print e
	
	return json.loads(response)

# Returns a Python list containing the number of seconds that each player was dead
def getDeadTime(region, gameId):
	data = getGameById(region, gameId)
	eventList = data["timeline"]["frames"]
	participantLevels = [1 for i in range(10)]
	deadList = [[] for i in range(10)]

	for frame in eventList:
		if "events" in frame:
			for event in frame["events"]:
				if event["eventType"] == "SKILL_LEVEL_UP":
					participantLevels[event["participantId"] - 1] += 1

				if event["eventType"] == "CHAMPION_KILL":
					deadList[event["victimId"] - 1].append((participantLevels[event["victimId"] - 1], event["timestamp"]))
		
	totalDeadTimes = [0 for i in range(10)]
	for i in xrange(10):
		totalDeadTimes[i] = utils.timeDead(deadList[i])

	return totalDeadTimes

# Returns the id that represents that summoner
def getIdBySummonerName(region, summonerName):
	url = "api/lol/" + region + "/v1.4/summoner/by-name/" + summonerName

	payload = {'api_key': apiKey}
	requestUrl = baseUrl + url
	
	try:
		response = requests.get(requestUrl, params=payload).text
	except Exception, e:
		print e
	
	return json.loads(response)[summonerName]['id']

#TODO
def getMinionsSlained(region, summonerId):

	url = "/api/lol/" + region + "/v1.3/stats/by-summoner/" + summonerId + "/summary"

	payload = {'api_key': apiKey}
	requestUrl = baseUrl + url
	
	try:
		response = requests.get(requestUrl, params=payload).text
	except Exception, e:
		print e
	
	return json.loads(response)
# TODO
def getRecentMatches(region, summonerId):
	url = "api/lol/" + region + "/v1.3/game/by-summoner/" + summonerId + "/recent"
	payload = {'api_key': apiKey}
	requestUrl = baseUrl + url
	
	try:
		response = requests.get(requestUrl, params=payload).text
	except Exception, e:
		print e
	
	return json.loads(response)

# Returns a Python list containing the number of seconds that each player was dead
def getItemsBought(region, gameId):
	data = getGameById(region, gameId)
	eventList = data["timeline"]["frames"]
	playerItems = [[] for i in range(10)]

	for frame in eventList:
		if "events" in frame:
			for event in frame["events"]:
				if event["eventType"] == "ITEM_PURCHASED":
					playerItems[event["participantId"] - 1].append(event["itemId"])

	return playerItems