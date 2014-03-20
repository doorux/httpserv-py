import xml.etree.ElementTree as ET


class XMLParserException(Exception):
	def __init__(self, msg):
		
		self.message = msg
		
	def __str__(self):
		return repr(self.message)


class XMLParser:
				
	def parse(self, XMLFile):
		
		config = {}
			
		try:
			tree = ET.parse(XMLFile)
			root = tree.getroot() 
			
			if(root.tag != "host"):
				raise XMLParserException("Poorly formed XML File: " + XMLFile)
				
			else:
				for child in root:
					config.update({child.tag : child.text})
				
		except ET.ParseError as e:
			raise XMLParserException("Poorly formed XML File: " + XMLFile)
			
		return config