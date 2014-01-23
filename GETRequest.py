#GETRequest.py
'''A class specifically for handling GET requests'''

import Request
class GETRequest(Request.Request):

	textExts = [ '.txt',  '.htm', '.html', '.doc', '.dat', '.xml', '.xhtml' ]
	mediaExts = ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.ico', 
				'.raw', '.mov', '.avi', '.mp4', '.mp3', '.mkv', '.rm', '.rmvb']

	def __init__(self, req):
		self.re = Request.Request(req)
		print("New GET request")
		
	def parse(self):
		print("Parsed...")
	
	def process(self, hostListener):
		#request resource from HostListener
		#if requested a type of text file
		if( any(x in self.re.resource.lower() for x in self.textExts)
			or self.re.resource == "/"):
			return hostListener.gettextURI(self.re.resource)
		#else if media type file is requested
		elif(any(x in self.re.resource.lower() for x in self.mediaExts)):
			return hostListener.getmediaURI(self.re.resource)
		