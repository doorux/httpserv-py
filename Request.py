#Request.py
'''A request class for handling incoming server requests'''


class Request:
		
		def __init__(self, req):
			self.request = req
			(self.host, self.hostport, self.method, self.resource, self.proto) = self.parse()

		def parse(self):
		
			method = self.request.split(' ')[0]
			resource = self.request.split(' ')[1]
			proto = self.request.split(' ')[2].split('\n')[0]
			
			try: 
				host = self.request.split('Host:')[1].split("\n")[0]
			except IndexError as e:
				host = ''
			try:
				hostport = host.split(':')[1]
				host = host.split(':')[0]
				host = host.strip()
			except IndexError as e:
				hostport = ''
		
		
			return (host, hostport, method, resource, proto)
