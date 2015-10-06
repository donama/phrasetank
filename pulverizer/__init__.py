"""
The PhrasetankPulverizer handles all raw data that is returned
from the Producer. It performs necessary cleaning of the data before handing
them over to the consumer for further processing
"""

from BeautifulSoup import BeautifulSoup

import urllib2

import urlparse

from phrasetank.rule import PhrasetankRule

from phrasetank.htmlutil import HtmlCleaner

from phrasetank.sink import PhrasetankSink

class PhrasetankPulverizer(object):
    
    def __init(self):
        
        self.rawData = None
        self.currentUri = None
        self.content = None
        self.anchors = set()
        self.baseUri = None
    
    def setCurrentURI(self,uri):
        """
        Set the currently crawled uri so that we can track
        it for double craling
        """
        self.currentUri = uri
        return self
    
    def setBaseURI(self,uri):
        """
        The original uri from which the producer started off
        the crawling process
        """
        self.baseUri = uri
        
        return self
    def setRawData(self,raw):
        
        self.rawData = raw
        return self
    def pulverizeData(self):
        """
        Pulverizes the original raw data building up
        a map of links to be visited as well as cleaned up data
        """
        self.anchors = set()
        
        if not self.rawData:
            return
        text_content = None
        soup = BeautifulSoup(self.rawData)
        # Get rid of all script style and link rules
        for elem in soup.findAll(['script','link','style']):
           elem.extract()
        
        text_content = str(soup.html.body)
        #Clean all unworthy characters in the text document
        cleaner = HtmlCleaner()
        self.content = cleaner.clean_text(text_content)
        # Ensure that the current uri is not crawled again by putting it
        # into the list of crawled uri
        PhrasetankSink.addSeenURI(self.currentUri)
        #Extract all links on the document
        links = soup.findAll('a',dict(href=True))
        
        for link in links:
            uri = PhrasetankRule.isCrawlable(self.baseUri,link['href'])
            if uri is not None:
                #Check if we had seen this link before
                if not PhrasetankSink.hasSeenURI(uri):
                    #Add this for later crawling
                    self.anchors.add(uri)
                    
                    
    
    def getLinks(self):
        
        return list(self.anchors)
    
    def getTextContent(self):
        
        return self.content
    