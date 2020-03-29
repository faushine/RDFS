class File:
    fId=''
    content=b''
    def __init__(self,parentId,fname,permission,fileOwner,groupOwner,type,fileSize,fileNode,lastModified):
        self.fname=fname
        self.permission=permission
        self.fileOwner=fileOwner
        self.groupOwner=groupOwner
        self.fId=parentId+'-'+fname
        self.type=type
        self.fileSize=fileSize
        self.fileNode=fileNode
        self.lastModified=lastModified
    