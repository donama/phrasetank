#!/usr/bin/env python
"""
a html cleaner class for removing all instances of
html tags
"""

import re

HTML_SPECS=re.compile(r'<[^<]*?/?>')

CHARTAG_SPECS=re.compile(r'(<!--(.*?)-->?)')

def filter_non_ascii(text):
    
    maps=[]
    
    if text:
        
        for m in text:
            
            if ord(m)>127:
                
                continue
            else:
                
                maps.append(m)
    
    return ''.join(maps)

class HtmlCleaner(object):
    def __init__(self):
        self.text=''
        self.tags=[]
    def filter_tags(self):
        #Find all the html tags in a given string with their attributes
        if self.text and len(self.text):
            
            self.tags=HTML_SPECS.findall(self.text)
            
            #filter out duplicates
            if len(self.tags):
                self.tags=list(set(self.tags))
                
    def get_tags(self):
        #Return all the tags found as a list
        return self.tags
        
    def clean_tags(self):
        #removes the found tags from the input streams
        if len(self.tags):
            for t in self.tags:
                self.text=re.sub(t,'',self.text)
        
    def clean_text(self,text=None):
        #cleans a given text of all html tags
        
        text=filter_non_ascii(text)
        #remove char tags
        text=CHARTAG_SPECS.sub('',text)
        text=HTML_SPECS.sub('',text)
        self.text=text
        
        #self.filter_tags()
        
        #self.clean_tags()
        
        return self.text    

