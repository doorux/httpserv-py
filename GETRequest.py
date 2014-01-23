#GETRequest.py
'''A class specifically for handling GET requests'''

import Request
class GETRequest(Request.Request):
	def __init__(self, req):
		self.re = Request.Request(req)
		print("New GET request")
		
	def parse(self):
		print("Parsed...")
	
	def process(self, hostListener):
		#request resource from HostListener
		#if requested a type of text file
		if(self.re.resource.lower().find('.txt') != -1 
			or self.re.resource.lower().find('.htm') != -1 
			or self.re.resource.lower().find('.html') != -1 
			or self.re.resource.lower().find('.doc') != -1 
			or self.re.resource.lower().find('.dat') != -1 
			or self.re.resource.lower().find('.xml') != -1 
			or self.re.resource.lower().find('.xhtml') != -1
			or self.re.resource == "/"):
			return hostListener.gettextURI(self.re.resource)
		#else if media type file is requested
		elif(self.re.resource.lower().find('.jpg') != -1 
			or self.re.resource.lower().find('.jpeg') != -1 
			or self.re.resource.lower().find('.png') != -1 
			or self.re.resource.lower().find('.bmp') != -1 
			or self.re.resource.lower().find('.tif') != -1 
			or self.re.resource.lower().find('.tiff') != -1 
			or self.re.resource.lower().find('.ico') != -1 
			or self.re.resource.lower().find('.raw') != -1
			or self.re.resource.lower().find('.mov') != -1
			or self.re.resource.lower().find('.avi') != -1
			or self.re.resource.lower().find('.mp4') != -1):
			return hostListener.getmediaURI(self.re.resource)
		