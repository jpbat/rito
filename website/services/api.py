# -*- coding: utf-8 -*-
#!/usr/bin/env python

import json
import utils
import requests

baseUrl = "https://euw.api.pvp.net/"
apiKey = "abca4714-5ed2-4e2e-91ff-a379b9d8ed1d"

# Returns a JSON list containing ids from URF games
def getUrfGamesTimestamp(region, date):

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

#Returns the int with the number of minions slained in the URF mode in the 2015 season
def getMinionsSlained(region, summonerId):

	url = "/api/lol/" + region + "/v1.3/stats/by-summoner/" + str(summonerId) + "/summary"

	payload = {'api_key': apiKey}
	requestUrl = baseUrl + url
	
	try:
		response = requests.get(requestUrl, params=payload).text
	except Exception, e:
		print e

	games = json.loads(response)["playerStatSummaries"]
	
	for game in games:
		if game["playerStatSummaryType"] == "URF":
			return game["aggregatedStats"]["totalMinionKills"]

	return None

#Returns the int with the number of jungle monsters slained in the URF mode in the 2015 season
def getMonstersSlained(region, summonerId):

	url = "/api/lol/" + region + "/v1.3/stats/by-summoner/" + str(summonerId) + "/summary"

	payload = {'api_key': apiKey}
	requestUrl = baseUrl + url
	
	try:
		response = requests.get(requestUrl, params=payload).text
	except Exception, e:
		print e

	games = json.loads(response)["playerStatSummaries"]
	
	for game in games:
		if game["playerStatSummaryType"] == "URF":
			return game["aggregatedStats"]["totalNeutralMinionsKilled"]

	return None

# Returns a JSON array of the last 10 matches done
def getRecentMatches(region, summonerId):
	url = "api/lol/" + region + "/v1.3/game/by-summoner/" + str(summonerId) + "/recent"
	payload = {'api_key': apiKey}
	requestUrl = baseUrl + url
	
	try:
		response = requests.get(requestUrl, params=payload).text
	except Exception, e:
		print e
	
	return json.loads(response)["games"]

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

# Returns a list containing the URF games of a given username and region
def getUrfGames(region, summonerId):
	retval = []

	gameList = getRecentMatches(region, summonerId)

	for game in gameList:
		if "subType" in game and game["subType"] == "URF":
			retval.append(game)

	return retval

# Returns a list containing the number of HP pots bought by each player
def calcHpPots(region, gameId):
	
	items = getItemsBought(region, gameId)

	# hp pot - 2003
	return [items[i].count(2003) for i in xrange(len(items))]

# Returns a list containing the ammount of gold earned by the players
def getGoldEarned(region, gameId):

	game = getGameById(region, gameId)

	retval = []

	for participant in game["participants"]:
		retval.append(participant["stats"]["goldEarned"])

	return retval

# Returns a list containing the largest critical strike of the players
def getLargestCriticalStrike(region, gameId):

	game = getGameById(region, gameId)

	retval = []

	for participant in game["participants"]:
		retval.append(participant["stats"]["largestCriticalStrike"])

	return retval

# Returns a list containing the total damage dealt to champions by each player
def getTotalDamageDealtToChampions(region, gameId):

	game = getGameById(region, gameId)

	retval = []

	for participant in game["participants"]:
		retval.append(participant["stats"]["totalDamageDealtToChampions"])

	return retval

# Returns a list containing the number of wards placed by each player
def getWardsPlaced(region, gameId):

	game = getGameById(region, gameId)

	retval = []

	for participant in game["participants"]:
		retval.append(participant["stats"]["wardsPlaced"])

	return retval

# Returns a list containing the total heal done by each player
def getTotalHeal(region, gameId):

	game = getGameById(region, gameId)

	retval = []

	for participant in game["participants"]:
		retval.append(participant["stats"]["totalHeal"])

	return retval

# Returns the ammont of IP earned in the last URF match
def getIpEarned(region, summonerId):
	return getUrfGames(region, summonerId)[0]["ipEarned"]

# Returns the sum of IP earned in the last URF matches 
def getTotalIpEarned(region, summonerId):
	total = 0
	games = getUrfGames(region, summonerId)
	for game in games:
		total += game["ipEarned"]
	return total

# Returns the avg level obtained in the urf matches
def getAvgLvlUrf(region, summonerId):
	total = 0
	games = getUrfGames(region, summonerId)
	for game in games:
		total += game["stats"]["level"]
	return total * 1.0 / len(games)

# Returns a list containing the total true damage dealt by each player
def getTrueDamageDealt(region, gameId):

	game = getGameById(region, gameId)

	retval = []

	for participant in game["participants"]:
		retval.append(participant["stats"]["trueDamageDealt"])

	return retval

# Returns a list containing the total true damage taken by each player
def getTrueDamageTaken(region, gameId):

	game = getGameById(region, gameId)

	retval = []

	for participant in game["participants"]:
		retval.append(participant["stats"]["magicDamageTaken"])

	return retval

# Returns the total number of kills on urf matches on the 2015 season
def getUrfKills(region, summonerId):

	url = "/api/lol/" + region + "/v1.3/stats/by-summoner/" + str(summonerId) + "/summary"

	payload = {'api_key': apiKey}
	requestUrl = baseUrl + url
	
	try:
		response = requests.get(requestUrl, params=payload).text
	except Exception, e:
		print e

	games = json.loads(response)["playerStatSummaries"]
	
	for game in games:
		if game["playerStatSummaryType"] == "URF":
			return game["aggregatedStats"]["totalChampionKills"]

	return None