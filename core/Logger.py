from datetime import datetime
import os.path

class Logger:


    def __init__(self, path, path2 = None):
        self.path =  path
        self.path2 = path2
    
    
    def write(self, msg):
        file = open(self.path, 'a')
        file.write("{0}\n".format(msg))
        file.close()

    def compare(self):
        c1 = self.countLines(self.path)
        c2 = self.countLines(self.path2)
        if c1 is c2:
            return True
        else:
            return False

    def repair(self):
        c1 = self.countLines(self.path)
        c2 = self.countLines(self.path2)
        if c1 > c2:
            self.rewriteFile(self.path, c2, c1)
        else :
            self.rewriteFile(self.path2, c1, c2)
            
                
    def rewriteFile(self, file, ind, final):      
            x = ind
            text = ''
            lines = open(file,'r').readlines()

            for i in range(x, final):
                lines[i] = ''

            text = ''.join(lines)
            with open(file,'w') as f:
                f.write(text)
        
    def countLines(self, path):
        file = open(path, 'r')
        n = sum(1 for line in file)
        file.close()
        return n
