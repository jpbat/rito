# -*- coding: utf-8 -*-
#!/usr/bin/env python

import api
import web
import sys
from web import form
sys.path.append('services')

render = web.template.render('templates/')

urls = (
	'/', 'index'
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
		data = web.data() # you can get data use this method
		return web.input()["name"], web.input()["region"]

if __name__ == '__main__':
	app = web.application(urls, globals())
	app.run()