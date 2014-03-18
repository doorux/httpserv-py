'''
	PortListener.py
	Listens for requests on specific ports and spins up host-specific handlers (if configured)
'''
import socket
import time
import RequestProcessor
import signal

class PortListener:

	def __init__(self, listeningPort, hostListeners):
		self.hostListeners = hostListeners
		self.host = ''
		self.port = listeningPort; #default port to try listening on
		self.serversocket = socket.socket (
						socket.AF_INET, socket.SOCK_STREAM)
		#bind the socket to a public host and port
		self.serversocket.bind((self.host, self.port))
		#start the listeners
		print( "Starting port-listener on port: ") #debug
		print( self.serversocket.getsockname() )
		
	
	def graceful_shutdown(self, sig, dummy):
		'''shutdown server from SIGINT signal'''
		print("Shutting down server")
		import sys
		self.serversocket.shutdown(0)
		self.serversocket.close()
		sys.exit(1)

	
	def receive(self, clientsocket):
		msg = ''
		chunk = 'blarg'
		#while len(chunk) != 0:
		chunk = clientsocket.recv(1024)
		#if not chunk: break
		chunk = bytes.decode(chunk)
		msg = msg + chunk
		return msg


	#Generates HTTP response Headers
	def gen_headers(self,  code):
	
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
		
	def senddata(self, clientsocket, requestedData):	
		body = ''
		response_headers = self.gen_headers(requestedData['status'])
		
		if 'text' in requestedData:
			body = requestedData['text'].encode()
		elif 'content' in requestedData:
			body = requestedData['content']
		
		#send data via the socket
		clientsocket.send(response_headers.encode())
		clientsocket.send(body)
	
		
	def play(self):
		while 1:

			signal.signal(signal.SIGINT, self.graceful_shutdown)

			self.serversocket.listen(5)
			
			
			#accept connections
			(clientsocket, address) = self.serversocket.accept()
			print("Socket open")
			
			#receive data on connection
			data = self.receive(clientsocket)
			
			#process data
			rp = RequestProcessor.RequestProcessor(data)
			requestedData = rp.process(self.hostListeners)
			self.senddata(clientsocket, requestedData)
			
			#print("Socket closed") #debug
			#close socket
			clientsocket.close()
		
		
		