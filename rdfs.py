from pathlib import Path
import os
from directory import Directory
from utils import *
from line import Line

current_dir=''
files=[]
dirs=[]
root=''

def process_cd(path):
    global current_dir
    if len(current_dir)==0:
        current_dir=root
    if path.startswith('..'):
        slash=len(path.split('/'))-1
        paths = current_dir.split('/')
        tempDir=''
        for i in range(1,len(paths)-slash-1):
            tempDir=tempDir+'/'+paths[i]
        tempPath=tempDir+'/'+paths[len(paths)-slash-1]
        if tempPath==root or checkDirExists(tempDir,paths[len(paths)-slash-1]):
            current_dir=tempDir+'/'+paths[len(paths)-slash-1]
        else:
            print('No such file or directory')
        return
    if checkDirExists(current_dir,path):
        current_dir = current_dir + '/' + path
    else:
        print('No such file or directory')


def process_ls(paras):
    global current_dir
    if len(current_dir) == 0: current_dir = root
    if len(paras)==1:
        objs = trackPathInName(current_dir)
        printLs(objs)
    elif len(paras)==2:
        if paras[1]=='-l':
            (dirs, files) = trackPath(current_dir)
            printLsVerbose(dirs,files)
        else:
            objs=[]
            if paras[1].startswith('/'):
                objs = trackPathInName(paras[paras[1]])
            else:
                if checkDirExists(current_dir, paras[1]):
                    objs = trackPathInName(current_dir+'/'+paras[1])
                else:
                    print('No such file or directory')
                    return
            printLs(objs)
    elif len(paras)==3:
        files = []
        dirs = []
        if paras[2].startswith('/'):
            (dirs,files) = trackPath(paras[2])
        else:
            if checkDirExists(current_dir,paras[2]):
                (dirs, files) = trackPath(current_dir+'/'+paras[2])
            else:
                print('No such file or directory')
                return
        printLsVerbose(dirs,files)

def process_find(path,pattern):
    global current_dir
    if len(current_dir)==0:current_dir=root
    if path=='./':path=current_dir
    pattern=eval(pattern)
    (dirs, files) = trackPath(path)
    (dirs, files) = findByPattern(pattern,dirs,files)
    printLsVerbosePath(dirs,files)
    return files

def process_grep(fPattern,cPattern):
    # grep pattern path
    global current_dir
    if len(current_dir) == 0: current_dir = root
    cPattern=eval(cPattern)
    fPattern=eval(fPattern)
    files=findFilesByPattern(fPattern,getFileInfo(current_dir))
    lines = findContentByPattern(cPattern,files)
    printMathchFiles(lines)

def process_upload():
    path = Path(__file__).parent.absolute()
    global current_dir
    current_dir=str(path)
    print('ready to traverse path:',path)
    for dirName, subdirList, fileList in os.walk(path):
        print('Found directory: %s' % dirName)
        dir = getInfoDir(str(dirName))
        dirs.append(dir)
        for fname in fileList:
            file = getInfoFile(dir,fname)
            if file is not None:
                files.append(file)
    print('traverse success!')
    print('total files:',len(files))
    print('total directories',len(dirs))
    print('ready to upload contents')
    uploadObjects(dirs,files)
    print('upload success!')

def process_path(path):
    p=path.split("=")
    storePath(p[0],p[1])
    print('store PATH success!')

def pshow_path():
    printShowPath()

def process_exec(prog):
    execProg(prog)

def main():
    global current_dir
    try:
        while(True):
            inn = input("$ ")
            paras =  inn.split()
            if paras[0]=='cd':
                if len(paras)>1 :
                    process_cd(paras[1])
            elif paras[0]=='ls':
                process_ls(paras)
            elif paras[0]=='find':
                if len(paras)<3:
                    print('pattern or path is required')
                    continue
                process_find(paras[1],paras[2])
            elif paras[0]=='grep':
                if len(paras)<3:
                    print('pattern is required')
                    continue
                process_grep(paras[1],paras[2])
            elif paras[0]=='upload':
                process_upload()
            elif paras[0]=='pwd':
                if len(current_dir)==0:current_dir=root
                print(current_dir)
            elif paras[0]=='path':
                if paras[1].startswith('-'):pshow_path()
                else:
                    process_path(paras[1])
            else:
                process_exec(paras[0])

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    root=getRoot()
    main()