"""
Sink serves just one purpose, to ensure that links are never crawled
twice during the running of the phrasetank service
all producers checks the sink to ensure that it does not crawl a link
twice
"""

import zlib

class PhrasetankSink(object):
    
    sinks = {}
    
    def __init__(self):
        pass
    
    @staticmethod
    def addSeenURI(uri):
        """
        Add already crawled link to the sink
        we create two hashes here the hash of the link
        as well as a hash of the link reversed
        """
        
        if uri:
            
            hash_f = zlib.crc32(uri.strip())
            hash_r = zlib.crc32(uri.strip()[::-1])
            #Ensure that the link does not exists int he sink
            PhrasetankSink.willAddLink(hash_f,hash_r,uri)
            
    @staticmethod
    def hasSeenURI(uri):
        """
        Checks to see if we have visited this uri before now
        """
        if uri:
            hash_f = zlib.crc32(uri.strip())
            hash_r = zlib.crc32(uri.strip()[::-1])
            
            if PhrasetankSink.sinks.has_key(str(hash_f)) or PhrasetankSink.sinks.has_key(str(hash_r)):
                return True
            else:
                return False
            
        return False
    
    @staticmethod
    def willAddLink(hash_one,hash_two,uri):
        
        if PhrasetankSink.sinks.has_key(str(hash_one)) or PhrasetankSink.sinks.has_key(str(hash_two)):
            # No need to add this link a second time
            return
        # Add the link on those two hashes
        PhrasetankSink.sinks[str(hash_one)] = uri
        PhrasetankSink.sinks[str(hash_two)] = uri
        