# -*- coding: utf-8 -*-
#!/usr/bin/env python

import json

def getChampionImage(key):
	return "http://ddragon.leagueoflegends.com/cdn/5.2.1/img/champion/" + key + ".png"

# returns a json containing info about the champion with the provided id
def getChampion(championId):
	f = open("data/champion.json")
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