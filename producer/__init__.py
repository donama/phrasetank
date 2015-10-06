"""
The PhrasetankProducer handles fetching files across the network
using the tornado api for this as well as updating the URLQueue
for later fetching of data
"""

import threading

import tornado

from tornado.httpclient import HTTPClient

from phrasetank.pulverizer import PhrasetankPulverizer

from phrasetank.sink import PhrasetankSink

from phrasetank.consumer import PhrasetankConsumer

def logMessage(msg_type,message):
    """
    Log the given message
    """
    message = '['+ msg_type+']'+ message+'\n'
    print message
    
class PhrasetankProducer(threading.Thread):
    
    def __init__(self):
        
        threading.Thread.__init__(self)
        self.uri = None
        self.uriTank = set()
        self.name = None
    
        
        
    def setURI(self,uri):
        """
        Set the uri from which the producer will start off
        fetching data, each producer will maintain its own
        cache of urls that needs to be visited as well as keep
        track of visited urls. the Producer will only exit when its
        done with fetching data from its source
        """
        self.uri = uri
        self.uriTank.add(uri)
        
        # Use the base link hostname as the name of the producer
        self.name = uri.split('.')[1].upper()+' Producer'
        
        return self
    
    def fetchURIData(self,uri):
        """
        Visit the given uri and fetch its page content
        """
        contentsource = None
        print "Visiting page at "+uri
        
        try:
            client = HTTPClient()
            response = client.fetch(uri)
            contentsource = response.body or None
        except:
            pass
        
        if contentsource:
            # Send the content source to the pulverizer for processing
            pulverize = PhrasetankPulverizer()
            pulverize.setBaseURI(self.uri)
            pulverize.setCurrentURI(uri)
            pulverize.setRawData(contentsource)
            #process the data
            pulverize.pulverizeData()
            
            links = pulverize.getLinks() or []
            content = pulverize.getTextContent() or ''
            if links and len(links):
                #self.uriTank.extend(links)
                for l in links:
                    self.uriTank.add(l)
            
            if content and len(content):
                # call the consumer for further processing of the data content
                consumer = PhrasetankConsumer()
                consumer.setDataContent(content)
                consumer.setProducerName(self.name)
                consumer.start()
        else:
            # Perhaps the link has an issue we need to not visit it again
            PhrasetankSink.addSeenURI(uri)
            logMessage("ERROR",'Failed to read content source for '+uri)
        
    def run(self):
        """
        Start running the producer
        """
        logMessage('START','PhrasetankProducer '+self.name+' is starting to crawl '+self.uri+' ...')
        
        while True:
            
            uri = None
            
            try:
                uri = self.uriTank.pop()
            except:
                pass
            
            if not uri:
                break
            # make sure that we have not visited this link before
            if PhrasetankSink.hasSeenURI(uri):
                #Log the seen status
                logMessage('SEEN',uri+' has been visited before now...')
                continue
            #Ok we are ready to visit the link
            self.fetchURIData(uri)