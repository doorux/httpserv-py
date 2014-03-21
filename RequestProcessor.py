'''
	RequestProcessor.py
	Listens for requests on specific ports and spins up host-specific handlers (if configured)
'''
import socket
import sys
import GETRequest

class RequestProcessor:

	def __init__(self, req):
		self.request = req

	def process(self, hostListener):
		req = self.request.split('\n')[0]
		
		if (req.find("GET") != -1):
			#Create a new get request
			gr = GETRequest.GETRequest(self.request)
			return gr.process(hostListener)
		elif (req.find("HEAD") != -1):
			#Create new HEAD request
			print("HEAD")
		elif (req.find("POST") != -1):
			#Create new POST request
			print("POST")
		else: 
			#Something ain't right
			#invalid request
			print("INVALID REQUEST TYPE: " + req)
			return {'status':404, 'content':bytes("404 NOT FOUND - FURTHERMORE - NOT A VALID REQUEST".encode())}
			
	
