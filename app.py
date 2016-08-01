#!/usr/bin/env python

import os, sys, json, logging
import requests
from BeautifulSoup import BeautifulSoup
from bottle import route, request, hook, run, response, default_app

@hook('before_request')
def content_type():
	response.content_type = 'application/json'

@route('/')
def index():
	page = BeautifulSoup(requests.get("http://{}/livedata.htm".format(weatherIP)).text)
	ignored = [
		'submit',
		'reset',
		'button'
	]

	elements = {}

	for element in page.findAll('input'):
		if not element['type'] in ignored:
			if element['name'].find('ID') is -1:
				elements[element['name'].lower()] = str(element['value'])


	# Now return it as JSON
	return json.dumps(
		elements,
		sort_keys=True,
		indent=4
	)

if __name__ == '__main__':

	# Initially get some data we need from the OS environment variables
	serverHost = os.getenv('IP', 'localhost')
	serverPort = os.getenv('PORT', '5000')
	weatherIP = os.getenv('WEATHER_IP', '192.168.1.119')

	# Instantiate the logger
	log = logging.getLogger('log')
	console = logging.StreamHandler()
	log.setLevel(logging.INFO)
	log.addHandler(console)

	if os.getenv('APP_MODE', 'web') is 'web':
		application = default_app()

		# Now we're ready, so start the server
		log.info("Successfully started application server")
		application.run(host=serverHost, port=serverPort, quiet=True, server='cherrypy')
	else:
		print index()       