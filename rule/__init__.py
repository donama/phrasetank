"""
Rules defines what is seen by Phrasetank as a valid url that can be visited
"""

import re

import urlparse

FILTER_PATTERN=re.compile(r"""\.js|\.css|\.png|\.gif|\.jpg|\.swf|\.facebook|\.twiiter|\.google|\.jpeg|\.doc|\.docx|\.pdf|\.xml""")

class PhrasetankRule(object):
    
    def __init__(self):
        pass
    @staticmethod
    def isCrawlable(base_uri,raw_uri):
        """
        Checks or validates that a given uri is crawlable
        """
        
        if not raw_uri or not base_uri:
            return None
        
        raw_uri = PhrasetankRule.normalizeURI(base_uri,raw_uri)
        
        search = FILTER_PATTERN.search(raw_uri)
        
        if search and search.group():
            # Not a valid link
            return None
        if raw_uri.startswith('mailto') or raw_uri.startswith('javascript'):
            return None
        if raw_uri.startswith('#'):
            return None
        # Check if this uri has slug-like feature, that marks the uri we are interested in
        # because news generally have slugs for the news title and to make it easy for search engine
        # to get to the news article, Phrasetank loves this too
        loc = urlparse.urlparse(raw_uri)
        slug = loc.path
        pos = slug.find('-')
        
        if pos < 0:
            return None
        
        return raw_uri
    
    @staticmethod
    def normalizeURI(base_uri,raw_uri):
        """
        Normalize that raw uri so that we can validate
        the url
        """
        parts = []
        
        if raw_uri and raw_uri.startswith('http'):
            return raw_uri
        
        parts = raw_uri.split('/')
        
        assembled = []
        
        if parts and len(parts):
            
            for fragment in parts:
                if fragment == '' or fragment == '.':
                    continue
                if fragment == '..':
                    # Pop from the assembled lists if its not empty
                    if len(assembled):
                        assembled.pop()
                    else:
                        # Push the fragement into the lists
                        assembled.append(fragment)
        
        # Rebuild the link
        full_uri = ''
        uri = urlparse.urlparse(base_uri)
        
        full_uri += str(uri.scheme)
        full_uri += '://'
        full_uri += str(uri.netloc)+ '/'
        full_uri += '/'.join(assembled)
        
        return full_uri