# -*- coding: utf-8 -*-
#!/usr/bin/env python

import json
import requests
import time
import api
import utils

def main():
	id = 2043838452
	summonerId = 53331486
	print "getGoldEarned", api.getGoldEarned("euw", id)
	print "getLargestCriticalStrike", api.getLargestCriticalStrike("euw", id)
	print "getTotalDamageDealtToChampions", api.getTotalDamageDealtToChampions("euw", id)
	print "getWardsPlaced", api.getWardsPlaced("euw", id)
	print "getTotalHeal", api.getTotalHeal("euw", id)
	print "getIpEarned", api.getIpEarned("euw", summonerId)
	print "getTotalIpEarned", api.getTotalIpEarned("euw", summonerId)
	print "getAvgLvlUrf", api.getAvgLvlUrf("euw", summonerId)
	print "getTrueDamageDealt", api.getTrueDamageDealt("euw", id)
	print "getTrueDamageTaken", api.getTrueDamageTaken("euw", id)
	print "getUrfKills", api.getUrfKills("euw", summonerId)
if __name__ == '__main__':
	main()
