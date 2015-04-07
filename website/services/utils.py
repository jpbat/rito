# -*- coding: utf-8 -*-
#!/usr/bin/env python

import time

def convertToEpoch(date):
	return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S'))) - time.timezone

def convertFromEpoch(epoch):
	return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(epoch/1000.))

def getDate(year, month, day, hour, minute):
	return str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":00"

def currentDeadTime(level, timestamp):

	deadTime = None
	brw = level * 2.5 + 5
	currentTime = timestamp / 1000. / 60

	if currentTime < 35:
		deadTime = brw
	else:
		if currentTime > 47.5:
			currentTime = 47.5
		deadTime = brw + (brw / 50) * ((currentTime - 35) * 2)

	deadTime += 2.5

	if deadTime > 52.5:
		deadTime = 52.5

	return deadTime

def timeDead(deadList):
	timer = 0
	for i in xrange(len(deadList)):
		timer += currentDeadTime(deadList[i][0], deadList[i][1])
	return timer

def getChampionImage(key):
	return "http://ddragon.leagueoflegends.com/cdn/5.2.1/img/champion/" + key + ".png"

# returns a json containing info about the champion with the provided id
def getChampion(championId):
	f = open("../data/champion.json")
	data = f.read()

	ids = []

	for c in json.loads(data)["data"]:
		ids.append(str(c))

	champions = json.loads(data)

	for i in xrange(len(ids)):
		champion = champions["data"][ids[i]]
		if int(champion["key"]) == championId:
			return {'id': str(champion["id"]), 'name': str(champion["name"]), 'image': str(getChampionImage(champion["id"]))}


	return {}