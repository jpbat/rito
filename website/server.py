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
	'/stat', 'stat'
)

userData = form.Form(
	form.Textbox("name"), 
	form.Dropdown('region', ['euw', 'na']),
)

class index:
	def GET(self): 
		form = userData()
		return render.formtest(form)
	def POST(self):
		return getGames(web.input()["region"], web.input()["name"])

class stat:
	def GET(self):
		return "Hello World!"
	def POST(self):
		return getRandomStat(web.input()["region"], web.input()["summonerId"])

def getGames(region, summonerName):
	summonerId = api.getIdBySummonerName(region, summonerName)
	return api.getUrfGames(region, summonerId)

def getRandomStat(region, gameId):
	# m['gameId'], m['championId'], m['teamId']
	print api.getItemsBought(region, gameId)
	return None

def notfound():
	return web.notfound("Sorry, Teemo mushrooms destroyed the page you are looking for :(")

if __name__ == '__main__':
	app = web.application(urls, globals())
	app.notfound = notfound
	app.run()