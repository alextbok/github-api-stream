#!/usr/bin/python

import simplejson as json
import sys, time
import requests, json
'''
This script streams all github users. Throughout the stream, every time your github api rate limit is reached, 
the script sleeps until your rate limit is reset (every hour).

The only command line flags comprise your github login credentials. You should have an account with an api key

To run:
./users.py <github username> <github password>

'''

GET_USERS_URL = 'https://api.github.com/users'

class User():

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
	This method streams all users from the github api and calls another method to post them to Neo4j
	It will pause according to rate limits and it runs until all github users have been processed
	'''
	def get_all_users(self):

		url = GET_USERS_URL

		while True:

			batch_users = []

			#batch together 20 requests (100 users are returned each request)
			for i in range(20):

				#get the next 100 users
				response = self.get_request(url)
				users = response.json()

				#if our ratelimit is reached, sleep until the limit expires
				if int(response.headers['X-RateLimit-Remaining']) < 1:
					print 'Sleeping for ' + str( float(response.headers['X-RateLimit-Reset']) - time.time() ) \
					+ ' seconds. (' + time.ctime(float(response.headers['X-RateLimit-Reset'])) + ' local time)'
					time.sleep(float(response.headers['X-RateLimit-Reset']) - time.time() + 1)

				#indicates we have processed all users
				if len(users) == 0:
					print 'All users have been processed\nHTTP header: '
					print response.headers
					print 'Users: '
					print users
					print "---Done---"
					return

				for user in users:
					batch_users.append(user)

				#update the url for the next request
				url = response.links['next']['url']

			#do something cool with the users
			self.process_users(batch_users)

			#some useful info messages
			print str( len(batch_users) ) + ' users processed'
			print 'id of last user posted: ' + str( batch_users[-1]['id'] )
			print 'Remaining Requests: ' + response.headers['X-RateLimit-Remaining']

	'''
	Do something cool with the users
	'''
	def process_users(self, users):
		for user in users:
			print user

if __name__=='__main__':
	if len(sys.argv) < 3:
		print 'ERROR: Authentication information needed.\n./repos.py <username> <password>'
	else:
		user = User(sys.argv[1], sys.argv[2])
		user.get_all_users()



