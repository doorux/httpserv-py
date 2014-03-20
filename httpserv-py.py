#httpserv-py
#Main class for a HTTP1.1 compliant python-based web server (for the lolz)


#import ConfigurationManager
import sys, getopt
import PortListener
import HostListener
import Configurator
import Configuration
import os
import XMLParser
import asyncore

#read args
if(len(sys.argv) > 1):
	opts = []
	args = []
	try:
		opts, args = getopt.getopt(sys.argv[1:], "f:c:")
		fFound = False
		cFound = False
		for opt, arg in opts:
			if opt == "-f":
				if fFound == True:
					raise getopt.GetoptError("TOO MANY -f ARGS")
				else:
					#process -f arg (location of conf file)
					print("opt: " + opt + " arg: "+arg)
					fFound = True
			elif opt == "-c":
				if cFound:
					raise getopt.GetoptError("TOO MANY -c ARGS")
				else:
					#process -c args (directory of site config files)
					print("opt: " + opt + " arg: "+arg)
					fFound = True

					
	except getopt.GetoptError:
		print("usage: python httpserv-py.py [-f <config file>]")
		sys.exit(1)
	
		
	
	
print("Starting server...")

#find port listener, add host config to it

#Read site configurations (ala simplified apache vhosts)
hostsDir = './hosts'
fileNames = [f for f in os.listdir(hostsDir)]
xmlParser = XMLParser.XMLParser()
configs = []
hlisteners = []
plisteners = []

for fileName in fileNames:
	fileLoc = hostsDir + "/" + fileName
	try:
	#	print(fileLoc)
		elems = xmlParser.parse(fileLoc)
		configs.append(Configuration.Configuration(elems))

	except Exception as xe:
		print(xe.message)
		sys.exit(1)
	

for conf in configs:
	
	#Start Request Processor(s) with specific hosts & configs for each
	host = HostListener.HostListener(conf)
	hlisteners.append(host)

	#Start port listeners on all defined ports
	pl = PortListener.PortListener(conf.getPort(), host)
	plisteners.append(pl)

#for pl in plisteners:
#	pl.play()

asyncore.loop()