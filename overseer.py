"""
This is the main entry point to starting the Phrasetank crawlers
"""
from phrasetank.producer import PhrasetankProducer

import time

class PhrasetankOverseer(object):
    
    def __init__(self,uri=[]):
        
        self.uris = uri
        self.canDeamonize = False
    
    def shouldDeamonize(self):
        """
        Should the producers be deamonized
        or not
        """
        
        self.canDeamonize = True
        return self
    
    def startCrawlers(self):
        """
        Start the crawlers or producers based on the number
        of links given, each producer will have the tash of handling all
        subsequently generated links from the original uri
        """
        
        if not self.uris or len(self.uris) == 0:
            print "Starting the Phrasetank Crawlers requires a set of urls to be crawled..."
            return
        
        cnt = len(self.uris)
        
        print "Starting "+str(cnt)+" Phrasetank producers ..."
        
        started = time.time()
        
        for uri in self.uris:
            
            producer = PhrasetankProducer()
            producer.setURI(uri)
            if self.canDeamonize:
                producer.setDaemon(True)
                
            producer.start()
        
        ended = time.time()
        
        print "Phrasetank completed crawling in %s"%(ended-started)
            
         
        
        