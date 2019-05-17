from datetime import datetime
import os.path

class Logger:


    def __init__(self, path):
        self.path =  path
    
    
    def write(self, msg):
        file = open(self.path, 'a')
        file.write(msg)
        file.close()
        
