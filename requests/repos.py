#!/usr/bin/python

import simplejson as json
import sys, time, io
import requests, json

'''
This script streams all github repositories. Throughout the stream, every time the 
github api rate limit is reached, the script sleeps until the rate limit is reset (every hour).

The only command line flags comprise your github login credentials. You should have an account with an api key

To run:
./repos.py <github username> <github password>

'''

REPOS_GET_URL = 'https://api.github.com/repositories'

class Repos():

	'''
	Stores the password upon instantiation
	'''
	def __init__(self, username, password):
		self._username = username
		self._password = password

	'''
	Perfoms a get request with the instance's authentication information
	'''
	def get_request(self, url):
		return requests.get(url, auth=(self._username, self._password) )		

	'''
	This method streams all repositories from the github api
	It will pause according to rate limit and it runs until all github repos have been processed
	'''
	def stream_repos(self):

		url = REPOS_GET_URL

		while True:

			#get the repos returned by the github api repo GET
			#most contains links to other api calls
			response = self.get_request(url)
			repos = response.json()

			repos_to_process = []

			#if our ratelimit is reached, sleep until the limit expires
			if int(response.headers['X-RateLimit-Remaining']) < 1:
				print 'Sleeping for ' + str( float(response.headers['X-RateLimit-Reset']) - time.time() ) \
				+ ' seconds. (' + time.ctime(float(response.headers['X-RateLimit-Reset'])) + ' local time)'
				time.sleep(float(response.headers['X-RateLimit-Reset']) - time.time() + 5)

			for repo in repos:

				#this api call actually returns useful information about the repositories
				res = self.get_request('https://api.github.com/repos/' + repo['full_name'])

				#if our ratelimit is reached, sleep until the limit expires
				if int(res.headers['X-RateLimit-Remaining']) < 1:
                                	print 'Sleeping for ' + str( float(res.headers['X-RateLimit-Reset']) - time.time() ) \
                                	+ ' seconds. (' + time.ctime(float(res.headers['X-RateLimit-Reset'])) + ' local time)'
                                	time.sleep(float(res.headers['X-RateLimit-Reset']) - time.time() + 5)

				repos_to_process.append( res.json() )


			#do something cool with the repositories
			self.process_repos(repos_to_process)

			#indicates we have processed all repos
			if len(repos) == 0:
				print 'All repos have been processed\nHTTP header: '
				print response.headers
				print 'Repos: '
				print repos
				print "---Done---"
				return

			#update the url for the next request
			url = response.links['next']['url']

			#some useful info messages
			print str( len(repos) ) + ' repos processed and posted to solr'
			print 'id of last repo processed: ' + str( repos[-1]['id'] )
			print 'Remaining Requests: ' + response.headers['X-RateLimit-Remaining']

	'''
	Do something cool with the repositories
	'''
	def process_repos(self,repos):
		for repo in repos:
			print repo


if __name__=='__main__':
	if len(sys.argv) < 3:
		print 'ERROR: Authentication information needed.\n./repos.py <username> <password>'
	else:
		repos = Repos(sys.argv[1],sys.argv[2])
		repos.stream_repos()


