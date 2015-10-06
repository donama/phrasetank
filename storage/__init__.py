"""
The phrasetank storage handles writing file to disk as well as perform
text extraction
"""

STORAGE_BASE ='data'

import os

import os.path

class PhrasetankStorage(object):
    
    def __init__(self):
        
        pass
    @staticmethod
    def writeFile(fname,fdata):
        """
        Write the given data to the storage system
        """
        if fname and fdata:
            
            path = os.path.join(os.path.dirname(__file__),STORAGE_BASE)
            
            path = path+'/'+fname
            
            try:
                with open(path,'wb') as f:
                    f.write(fdata)
                    f.close()
                    
            except:
                print "failed to write file "+fname
                
            
      
