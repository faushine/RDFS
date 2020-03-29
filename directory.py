import hashlib


class Directory:
    dirSub = ''
    dirId = ''
    def __init__(self, dirPath,dirName, permission, dirOwner, groupOwner,dirSize,dirNode,lastModified):
        self.dirPath = dirPath
        self.dirName=dirName
        self.dirId = hashlib.md5(dirPath.encode()).hexdigest()
        self.permission = permission
        self.dirOwner = dirOwner
        self.groupOwner = groupOwner
        self.dirSize=dirSize
        self.dirNode=dirNode
        self.lastModified=lastModified

    def addDirSub(self, sub):
        if len(self.dirSub)==0:
            self.dirSub=sub
        else:
            self.dirSub=self.dirSub+','+sub

