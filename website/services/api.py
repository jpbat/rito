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
def getDeadTime(region, gameId, teamId, championId):
	data = getGameById(region, gameId)

	# find the participantId:
	participantId = None
	participants = data["participants"]
	for participant in participants:
		if participant["teamId"] == teamId and participant["championId"] == championId:
			participantId = participant["participantId"]
			break

	# Process the timeline so that all the kills and level ups can be caught to calc the death timmers
	eventList = data["timeline"]["frames"]
	level = 1
	deadList = []

	for frame in eventList:
		if "events" in frame:
			for event in frame["events"]:
				if event["eventType"] == "SKILL_LEVEL_UP" and event["participantId"] == participantId:
					level += 1

				if event["eventType"] == "CHAMPION_KILL" and event["victimId"] == participantId:
					deadList.append((level, event["timestamp"]))

	return utils.timeDead(deadList)

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

# Returns a Python list containing the items each player bought
def getItemsBought(region, gameId, teamId, championId):
	data = getGameById(region, gameId)

	# find the participantId:
	participantId = None
	participants = data["participants"]
	for participant in participants:
		if participant["teamId"] == teamId and participant["championId"] == championId:
			participantId = participant["participantId"]
			break

	eventList = data["timeline"]["frames"]
	items = []

	for frame in eventList:
		if "events" in frame:
			for event in frame["events"]:
				if event["eventType"] == "ITEM_PURCHASED" and event["participantId"] == participantId:
					items.append(event["itemId"])

	return items

# Returns a list containing the URF games of a given username and region
def getUrfGames(region, summonerId):
	retval = []

	gameList = getRecentMatches(region, summonerId)

	for game in gameList:
		if "subType" in game and game["subType"] == "URF":
			retval.append(game)

	return retval

# Returns a list containing the number of HP pots bought by each player
def calcHpPots(region, gameId, teamId, championId):
	
	items = getItemsBought(region, gameId, teamId, championId)

	# hp pot - 2003
	return items.count(2003)

# Returns a list containing the ammount of gold earned by the players
def getGoldEarned(region, gameId, teamId, championId):

	game = getGameById(region, gameId)

	# find the participantId:
	participantId = None
	participants = game["participants"]
	for participant in participants:
		if participant["teamId"] == teamId and participant["championId"] == championId:
			participantId = participant["participantId"]
			break

	for participant in game["participants"]:
		if participant["participantId"] == participantId:
			return participant["stats"]["goldEarned"]

	return None

# Returns a list containing the largest critical strike of the players
def getLargestCriticalStrike(region, gameId, teamId, championId):

	game = getGameById(region, gameId)

	# find the participantId:
	participantId = None
	participants = game["participants"]
	for participant in participants:
		if participant["teamId"] == teamId and participant["championId"] == championId:
			participantId = participant["participantId"]
			break

	for participant in game["participants"]:
		if participant["participantId"] == participantId:
			return participant["stats"]["largestCriticalStrike"]

	return None

# Returns a list containing the total damage dealt to champions by each player
def getTotalDamageDealtToChampions(region, gameId, teamId, championId):

	game = getGameById(region, gameId)

	# find the participantId:
	participantId = None
	participants = game["participants"]
	for participant in participants:
		if participant["teamId"] == teamId and participant["championId"] == championId:
			participantId = participant["participantId"]
			break

	for participant in game["participants"]:
		if participant["participantId"] == participantId:
			return participant["stats"]["totalDamageDealtToChampions"]

	return None

# Returns a list containing the number of wards placed by each player
def getWardsPlaced(region, gameId, teamId, championId):

	game = getGameById(region, gameId)

	# find the participantId:
	participantId = None
	participants = game["participants"]
	for participant in participants:
		if participant["teamId"] == teamId and participant["championId"] == championId:
			participantId = participant["participantId"]
			break

	for participant in game["participants"]:
		if participant["participantId"] == participantId:
			return participant["stats"]["wardsPlaced"]

	return None

# Returns a list containing the total heal done by each player
def getTotalHeal(region, gameId, teamId, championId):

	game = getGameById(region, gameId)

	# find the participantId:
	participantId = None
	participants = game["participants"]
	for participant in participants:
		if participant["teamId"] == teamId and participant["championId"] == championId:
			participantId = participant["participantId"]
			break

	for participant in game["participants"]:
		if participant["participantId"] == participantId:
			return participant["stats"]["totalHeal"]

	return None

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
def getTrueDamageDealt(region, gameId, teamId, championId):

	game = getGameById(region, gameId)

	# find the participantId:
	participantId = None
	participants = game["participants"]
	for participant in participants:
		if participant["teamId"] == teamId and participant["championId"] == championId:
			participantId = participant["participantId"]
			break

	for participant in game["participants"]:
		if participant["participantId"] == participantId:
			return participant["stats"]["trueDamageDealt"]

	return None

# Returns a list containing the total true damage taken by each player
def getTrueDamageTaken(region, gameId, teamId, championId):

	game = getGameById(region, gameId)
	
	# find the participantId:
	participantId = None
	participants = game["participants"]
	for participant in participants:
		if participant["teamId"] == teamId and participant["championId"] == championId:
			participantId = participant["participantId"]
			break

	for participant in game["participants"]:
		if participant["participantId"] == participantId:
			return participant["stats"]["magicDamageTaken"]

	return None

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