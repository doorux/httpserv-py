#Configuration class

class Configuration:
	def __init__(self, configFile):
		self.interpret(configFile)
		
	def interpret(self, configFile):
		self.config = configFile
	
	def getConfig(self):
		return self.config