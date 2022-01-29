import requests
from time import sleep
from urllib.error import HTTPError
from urllib.request import urlopen, Request, HTTPError



def api_get(url):
	# Opens a URL and returns JSON

	for i in range(3):
		# If an error is received, tries 2 more times, with a 10 second interval
		r = requests.get(url)
		if r.status_code == 200:
			return r.json()
		elif r.status_code >= 400 and r.status_code < 500:
			raise Exception("Client-side error when contacting the API server.")
		sleep(10)
	
	raise Exception("Failed consecutively trying to connect sucessfully to:\n",url,"\n\n")