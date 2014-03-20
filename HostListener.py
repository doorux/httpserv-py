#HostListener
'''Listener with configured host'''

import os

class HostListener:
	def __init__(self, configuration):
		#interpret configuration
		self.config = configuration
		print("New Hostlistener for: " + self.config.getHostname())
		
	def getURI(self, uri):
	
		if uri == "/":
			try:
				with open('index.html', 'rb') as f:
					return {'status':200, 'content':f.read()}
			except FileNotFoundError as e:
				print(e)
				try:
					with open('404.html', 'rb') as f:
						return {'status':404, 'content':f.read()}
				except FileNotFoundError as fnf:
					print("SUPER BIG FILE NOT FOUND ERROR- COULDN'T EVEN FIND 404")
					return {'status':404, 'text':bytes("404! - 404 not found".encode())}
							
		elif uri != "":
			try:
				with open(uri.split("/")[1], 'rb') as f:
					return {'status':200, 'content':f.read()}
			except FileNotFoundError as e:
				print(e)

				try:
					with open('404.html', 'rb') as f:
						return {'status':404, 'content':f.read()}
				except FileNotFoundError as fnf:
					print("SUPER BIG FILE NOT FOUND ERROR- COULDN'T EVEN FIND 404")
					return {'status':404, 'content':bytes("404! - 404 not found".encode())}
	
	def handleCGI(self, uri):
		print("CGI Call")
		return {'status':200, 'content':bytes("Not yet implemented. Bug the developer.".encode())}
		
	def getHostname(self):
		return self.config.getHostname()
		
	def getBindAddress(self):
		return self.config.getBindAddress()
