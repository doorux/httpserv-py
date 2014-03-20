'''
	PortListener.py
	Listens for requests on specific ports and spins up host-specific handlers (if configured)
'''
import asyncore
import socket
import time
import RequestProcessor
import signal

class PortHandler(asyncore.dispatcher_with_send):
			
	def addHostListener(self, hostListener):
		self.hostListener = hostListener
			
	#Generates HTTP response Headers
	def gen_headers(self, code):
	
		h = ''
		# determine response code
		if (str(code) == "200"):
			h = 'HTTP/1.1 200 OK\n'
		elif(str(code) == "404"):
			h = 'HTTP/1.1 404 Not Found\n'

		# write additional headers
		current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
		#h += "Content-type: text/html\n" #not including Content-type just yet. Needs refinement
		h += 'Date: ' + current_date +'\n'
		h += 'Server: Simple-Python-HTTP-Server\n'
		h += 'Connection: close\n\n'  #tell browser we're closing the connection

		return h
		
	def senddata(self, requestedData):	
		body = ''
		response_headers = self.gen_headers(requestedData['status'])
		
		if 'text' in requestedData:
			body = requestedData['text'].encode()
		elif 'content' in requestedData:
			body = requestedData['content']
		
		#send data via the socket
		self.send(response_headers.encode())
		self.send(body)
	
	def handle_read(self):
		msg = ''
		chunk = 'blarg'
		#while len(chunk) != 0:
		chunk = self.recv(8192)
		msg = bytes.decode(chunk)
		
		#process data
		rp = RequestProcessor.RequestProcessor(msg)
		requestedData = rp.process(self.hostListener)
		self.senddata(requestedData)


class PortListener(asyncore.dispatcher):

	def __init__(self, listeningPort, hostListener):
		asyncore.dispatcher.__init__(self)
		self.hostListener = hostListener
		self.bindAddr = hostListener.getBindAddress()
		self.port = listeningPort; #default port to try listening on
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		#bind the socket to a public host and port
		self.bind((self.bindAddr, self.port))
		self.listen(5)
		#start the listeners
		print( "Setting up port-listener on: ", end="") #debug
		print( self.getsockname() )
	
	def graceful_shutdown(self, sig, dummy):
		'''shutdown server from SIGINT signal'''
		print("Shutting down server")
		import sys
		self.shutdown(0)
		self.close()
		sys.exit(1)
		
	def handle_accepted(self, sock, addr):
			
		signal.signal(signal.SIGINT, self.graceful_shutdown)
					
		handler = PortHandler(sock)
		handler.addHostListener(self.hostListener)
		
		
		