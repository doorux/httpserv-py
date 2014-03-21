#HostListener
'''Listener with configured host'''

import os
import subprocess


class HostListener:
	def __init__(self, configuration):
		#interpret configuration
		self.config = configuration
		self.rootDirectory = self.config.getDocumentRoot()
		if(self.rootDirectory[-1] != '/'):
			self.rootDirectory = self.rootDirectory + '/'
			
		
		print("New Hostlistener for: " + self.config.getHostname())
		print("root" + self.rootDirectory)
		
	def getURI(self, uri):
	
		if uri == "/":
			if(os.path.isfile(self.rootDirectory + 'index.html')):
				resource = self.rootDirectory + 'index.html'
			elif(os.path.isfile(self.rootDirectory + 'index.php')):
				resource = self.rootDirectory + 'index.php'
			else:
				resource = self.rootDirectory + 'index.html' #temp placeholder
				#do a directory listing?
			try:
				with open(resource, 'rb') as f:
					content = f.read()
					f.close()
					return {'status':200, 'content':content}
			except IOError as e:
				print(e)
				try:
					with open(self.rootDirectory + '404.html', 'rb') as f:
						content = f.read()
						f.close()
						return {'status':404, 'content':content}
				except IOError as fnf:
					print("SUPER BIG FILE NOT FOUND ERROR- COULDN'T EVEN FIND 404")
					return {'status':404, 'text':bytes("404! - 404 not found".encode())}
				except PermissionError:
					print("Not allowed to read " + resource)
					return {'status':550, 'content':bytes("550! - Permission denied. You may not access\
						that resource!".encode())}
							
		elif uri != "":
			if(uri.startswith('/')):
				uri = uri.lstrip('/')
			resource = self.rootDirectory + uri 
			try:
				#grab everything after the URI / (ideally the resource & extension) and
				#prepend with root directory so we're looking in the right place
				with open(resource, 'rb') as f:
					content = f.read()
					
					f.close()
					return {'status':200, 'content':content}
			except IOError as e:
				print(e)

				try:
					with open(self.rootDirectory + '404.html', 'rb') as f:
						content = f.read()
						f.close()
						return {'status':404, 'content':content}
				except IOError as fnf:
					print("SUPER BIG FILE NOT FOUND ERROR- COULDN'T EVEN FIND 404")
					return {'status':404, 'content':bytes("404! - 404 not found".encode())}
				except PermissionError:
					print("Not allowed to read " + resource)
					return {'status':550, 'content':bytes("550! - Permission denied. You may not access\
						that resource!".encode())}
	
	def handleCGI(self, uri):
		if(uri.startswith('/')):
			uri = uri.lstrip('/')
			resource = self.rootDirectory + uri
	
		print("CGI Call")
		#return {'status':200, 'content':bytes("Not yet implemented. Bug the developer.".encode())}
		#return self.getURI(uri) #temporarily just grab the file and return it (or not, if that's the case)
		
		proc = subprocess.Popen(["php", resource], stdout=subprocess.PIPE, env={"SERVER_NAME":self.getHostname()})
		script_response = proc.stdout.read()
		return {'status':200, 'content':script_response} 
		
	def getHostname(self):
		return self.config.getHostname()
		
	def getBindAddress(self):
		return self.config.getBindAddress()
