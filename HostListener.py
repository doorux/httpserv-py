#HostListener
'''Listener with configured host'''

import os

class HostListener:
	def __init__(self, configuration):
		#interpret configuration
		self.config = configuration
		print("New Hostlistener for: " + self.config.getConfig()['host'])
		
	def gettextURI(self, uri):
	
		if uri == "/":
			try:
				with open('index.html', 'r') as f:
					return {'status':200, 'text':f.read()}
			except FileNotFoundError as e:
				print(e)
				try:
					with open('404.html', 'r') as f:
						return {'status':404, 'text':f.read()}
				except FileNotFoundError as fnf:
					print("SUPER BIG FILE NOT FOUND ERROR- COULDN'T EVEN FIND 404")
					return {'status':404, 'text':"404! - 404 not found"}
							
		elif uri != "":
			try:
				with open(uri.split("/")[1], 'r') as f:
					return {'status':200, 'text':f.read()}
			except FileNotFoundError as e:
				print(e)

				try:
					with open('404.html', 'r') as f:
						return {'status':404, 'text':f.read()}
				except FileNotFoundError as fnf:
					print("SUPER BIG FILE NOT FOUND ERROR- COULDN'T EVEN FIND 404")
					return {'status':404, 'text':"404! - 404 not found"}
	
	def getmediaURI(self, uri):
		if uri != "":
			try:
				with open(uri.split("/")[1], 'rb') as f:
					return {'status':200, 'content':f.read()}
			except FileNotFoundError as e:
				print(e)

				try:
					with open('404.html', 'rb') as f:
						return {'status':404, 'text':f.read()}
				except FileNotFoundError as fnf:
					print("SUPER BIG FILE NOT FOUND ERROR- COULDN'T EVEN FIND 404")
					return {'status':404, 'text':"404! - 404 not found"}