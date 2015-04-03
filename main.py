# -*- coding: utf-8 -*-
#!/usr/bin/env python

import json
import requests
import time
import api
import utils

def main():
	urfs = api.getUrfGames("euw", "2015-4-3 11:00:00")
	print api.getGameById("euw", urfs[0])

if __name__ == '__main__':
	main()