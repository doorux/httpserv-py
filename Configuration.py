#Configuration class

class Configuration:
	def __init__(self, configFile):
		self.interpret(configFile)
		
	def interpret(self, configFile):
		self.config = configFile
		self.name = configFile['name']
		self.port = int(configFile['port'])
		
		try:
			self.bindAddress = configFile['bindAddress']
		except KeyError as ke:
			self.bindAddress = ''
			
	def getConfig(self):
		return self.config
		
	def getPort(self):
		return self.port
		
	def getHostname(self):
		return self.name
	
	def getBindAddress(self):
		return self.bindAddress