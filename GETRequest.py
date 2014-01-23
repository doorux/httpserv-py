#GETRequest.py
'''A class specifically for handling GET requests'''

import Request
class GETRequest(Request.Request):

	cgiExts = ['.php', '.py', '.aspx']

	def __init__(self, req):
		self.re = Request.Request(req)
		print("New GET request")
		
	def parse(self):
		print("Parsed...")
	
	def process(self, hostListener):
		#request resource from HostListener
		#if requested a type of text file
		if(self.re.resource == "/"):
			return hostListener.getURI(self.re.resource)
		#else if media type file is requested
		elif(any(x in self.re.resource.lower() for x in self.cgiExts)):
			return hostListener.handleCGI(self.re.resource)
		else:
			return hostListener.getURI(self.re.resource)