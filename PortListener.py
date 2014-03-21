'''
	PortListener.py
	Listens for requests on specific ports and spins up host-specific handlers (if configured)
'''
import asyncore
import socket
import time
import RequestProcessor
import signal
import gzip

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
		#h += 'Content-Type: text/html; charset=UTF-8\n'
		h += 'Content-Encoding: gzip\n'
		h += 'Connection: close\n\n'  #tell browser we're closing the connection

		return h
		
	def handle_write(self):	
	
		#process data
		rp = RequestProcessor.RequestProcessor(self.request)
		requestedData = rp.process(self.hostListener)
			
		body = ''
		response_headers = self.gen_headers(requestedData['status']).encode()
		
		if 'text' in requestedData:
			body = requestedData['text'].encode()
		elif 'content' in requestedData:
			body = requestedData['content']
				
		#send data via the socket
		try:
			#lock down the socket so no one else can use it. might defeat 
			#purpose of using asyncore, but asyncore was doing a bad job
			#of handling things, causing sending to fail with "resource
			#unavailable
			self.socket.setblocking(True)
			
			sent = self.sendall(response_headers)
			self.buffer = body
			
			#use gzip compression on body to shrink it a bit
			self.buffer = gzip.compress(self.buffer)
			
			sent = len(self.buffer)
			print("Body content size: ", end='')
			print(sent)
			
			sent = self.sendall(self.buffer)
			
			self.handle_close()
			#unblock socket I guess
			self.socket.setblocking(False)
						
		except socket.error as err:
			print("SOCKET ERROR: ", end="")
			print(err)
			self.handle_close()
		
	
	def writeable(self):
		return True
	
	def handle_close(self):
		print("closing connection")
		self.close()
		
	def handle_read(self):
		msg = ''
		chunk = 'blarg'
		#while len(chunk) != 0:
		chunk = self.recv(8192)
		msg = bytes.decode(chunk)
		
		self.request = msg
		self.handle_write()


class PortListener(asyncore.dispatcher_with_send):

	def __init__(self, listeningPort, hostListener):
		self.hostListener = hostListener
		self.bindAddr = hostListener.getBindAddress()
		self.port = listeningPort; #port to try listening on
		
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		
		#bind the socket to a public host and port
		self.bind((self.bindAddr, self.port))
		self.listen(5)
		
		#start the listeners
		print( "Setting up port-listener on: ", end="") #debug
		print( self.getsockname() )
	
		
	def close_socket(self):
		self.shutdown(0)
		self.close()
		
	def handle_accepted(self, sock, addr):
								
		handler = PortHandler(sock)
		handler.addHostListener(self.hostListener)
		
		
		