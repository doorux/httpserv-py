#httpserv-py
#Main class for a HTTP1.1 compliant python-based web server (for the lolz)


#import ConfigurationManager
import sys, getopt
import PortListener
import HostListener
import Configurator
import Configuration
import os

#read args
if(len(sys.argv) > 1):
	print("GRAG")
	try:
		opts, args = getopt.getopt(sys.argv, "f:")
	except getopt.GetoptError:
		print("usage: python httpserv-py.py [-f <config file>]")
		sys.exit(1)
		
	print(opts)
	
	for opt, arg in opts:
		#if opt == "-f":
		print("opt: " + opt + " arg: "+arg)
		
	
	
print("Starting server...")

#find port listener, add host config to it

#Read site configurations (ala simplified apache vhosts)
hostsDir = './hosts'
fileNames = [f for f in os.listdir(hostsDir)]
for fileName in fileNames:
	try:
		with open(hostsDir + '/' + fileName, 'r') as f:
			print(f.read())
	except FileNotFoundError as e:
		print(e)
		
myConf = Configuration.Configuration({'host' : 'test.co.uk'})

#Start Request Processor(s) with specific hosts & configs for each
host = HostListener.HostListener(myConf)

#Start port listeners on all defined ports
pl = PortListener.PortListener(8080, host)

pl.play()

