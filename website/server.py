# -*- coding: utf-8 -*-
#!/usr/bin/env python

import web
import sys
from web import form
sys.path.append('services')
import api
import re

render = web.template.render('templates/')

urls = (
	'/', 'index',
	'/stat', 'stat',
)

userData = form.Form(
	form.Textbox("name"), 
	form.Dropdown('region', ['euw', 'na']),
)

class index:
	def GET(self): 
		form = userData()
		return render.summonerName(form)
	def POST(self):
		games = getGames(web.input()["region"], web.input()["name"]) 
		return render.list(games)

class stat:
	def GET(self):
		return "Hello World!"
	def POST(self):
		region = str(web.input()["region"])
		gameId = int(web.input()["gameId"])
		teamId = int(web.input()["teamId"])
		championId = int(web.input()["championId"])
		return getRandomStat(region, gameId, teamId, championId)

def getGames(region, summonerName):
	summonerId = api.getIdBySummonerName(region, summonerName)
	return api.getUrfGames(region, summonerId)

def getRandomStat(region, gameId, teamId, championId):
	return 'pots', api.calcHpPots(region, gameId, teamId, championId)

def notfound():
	return web.notfound("Sorry, Teemo mushrooms destroyed the page you are looking for :(")

def internalerror():
	return web.internalerror("Looks like some black magic was happening... Heimerdinger is looking the answer to this problem and Thresh is trying to hook Lucian.")

if __name__ == '__main__':
	app = web.application(urls, globals())
	app.notfound = notfound
	app.internalerror = internalerror
	try:
		app.run()
	except Exception, e:
		print e
