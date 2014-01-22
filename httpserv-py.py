#httpserv-py
#Main class for a HTTP1.1 compliant python-based web server (for the lolz)

print("Starting server...")

#import ConfigurationManager
import PortListener
import HostListener
import Configuration

#Read site configurations (ala simplified apache vhosts)

myConf = Configuration.Configuration({'host' : 'test.co.uk'})

#Start Request Processor(s) with specific hosts & configs for each
host = HostListener.HostListener(myConf)

#Start port listeners on all defined ports
pl = PortListener.PortListener(8080, host)

pl.play()



