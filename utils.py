import subprocess
from pathlib import Path
from directory import Directory
from file import File
import pymysql.cursors
import warnings
import hashlib
import re
from line import Line


def connect():
    # Connect to the database
    connection = pymysql.connect(host='mysql.cmigjolufvv5.us-west-2.rds.amazonaws.com',
                                 user='admin',
                                 password='gotohell',
                                 db='rdfs',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def getRoot():
    connection = connect()
    root = ''
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT min(dirPath) FROM Directory ORDER BY dirPath'
            cursor.execute(sql)
            result = cursor.fetchone()
            root = result['min(dirPath)']
    finally:
        connection.close()
    return root

def storePath(key,value):
    connection = connect()
    try:
        with connection.cursor() as cursor:
            sql = 'INSERT INTO `Path` (pkey, pvalue) VALUES(%s, %s);'
            cursor.execute(sql,(key,value))
            connection.commit()
    except:
        print('error')
    finally:
        connection.close()

def checkDirExists(dir, path):
    dirs = getSubDirInDirName(dir)
    if path in dirs:
        return True
    else:
        return False


def getFilesInDirName(path):
    files = []
    dirHash = hashlib.md5(path.encode()).hexdigest()
    connection = connect()
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT fname FROM File WHERE fId LIKE %s'
            cursor.execute(sql, (dirHash + '%',))
            results = cursor.fetchall()
            for r in results:
                files.append(r['fname'])
    finally:
        connection.close()
    return files


def getSubDirInDirName(path):
    dirs = []
    dirHash = hashlib.md5(path.encode()).hexdigest()
    connection = connect()
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT dirSub FROM Directory WHERE dirId=%s'
            cursor.execute(sql, (dirHash,))
            result = cursor.fetchone()
            subdir = result['dirSub'].split(',')
            for sub in subdir:
                dirs.append(sub)
    except:
        return dirs
    finally:
        connection.close()
    return dirs


def trackPathInName(path):
    objList = []
    objList.append(getFilesInDirName(path))
    objList.append(getSubDirInDirName(path))
    return objList

def trackPath(path):
    dirs=getSubDirInfo(path)
    files=getFileInfo(path)
    return (dirs,files)

def getSubDirInfo(path):
    dirs = []
    connection = connect()
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM Directory WHERE dirPath LIKE %s'
            cursor.execute(sql, (path+'%',))
            result = cursor.fetchall()
            for r in result:
                if r['dirPath']!=path:
                    dir = Directory(r['dirPath'],r['dirName'],r['permission'],r['dirOwner'],r['groupOwner'],r['dirSize'],r['dirNode'],r['lastModified'])
                    dirs.append(dir)
    finally:
        connection.close()
    return dirs

def getFileInfo(path):
    files = []
    dirHash = hashlib.md5(path.encode()).hexdigest()
    connection = connect()
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM File WHERE fId LIKE %s'
            cursor.execute(sql, (dirHash + '%',))
            results = cursor.fetchall()
            for r in results:
                file = File('',r['fname'],r['permission'],r['fileOwner'],r['groupOwner'],r['fileType'],r['fileSize'],r['fileNode'],r['lastModified'],r['filePath'])
                file.content=r['content']
                files.append(file)
    finally:
        connection.close()
    return files

def uploadObjects(dirs, files):
    warnings.filterwarnings("ignore")
    connection = connect()
    try:
        with connection.cursor() as cursor:
            sql = 'truncate Directory'
            cursor.execute(sql)
            sql = 'truncate File'
            cursor.execute(sql)
            connection.commit()
            # upload directories
            for dir in dirs:
                sql = "INSERT INTO Directory (dirId, dirPath,dirName, dirSub, permission, dirNode, dirOwner, groupOwner, dirSize, lastModified) " \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (
                    dir.dirId, dir.dirPath, dir.dirName, dir.dirSub, dir.permission, dir.dirNode, dir.dirOwner,
                    dir.groupOwner,
                    dir.dirSize, dir.lastModified))
            # upload files
            for file in files:
                sql = "INSERT INTO File (fId, fname, content, permission, fileNode, fileOwner, groupOwner, fileSize, fileType,lastModified, filePath) " \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql,
                               (file.fId, file.fname, file.content, file.permission, file.fileNode, file.fileOwner,
                                file.groupOwner,
                                file.fileSize, file.type, file.lastModified,file.filePath))
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        connection.close()


def getInfoFile(parent, fname):
    fullPath = parent.dirPath + '/' + fname
    out = subprocess.Popen(['stat', fullPath],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    res = stdout.decode("utf-8")
    attrs = res.split()
    permission = attrs[2]
    fileNode = int(attrs[3])
    fileOwner = attrs[4]
    groupOwner = attrs[5]
    fileSize = int(attrs[7])
    t = fname.split('.')
    type = 'hidden'
    if len(t) > 1 and len(t[0]) > 0:
        type = t[-1]
    date = formatDate(res)
    file = File(parent.dirId, fname, permission, fileOwner, groupOwner, type, fileSize, fileNode, date, fullPath)
    try:
        f = open(fullPath, "rb")
        content = f.read()
        file.content = content
    except:
        return None
    return file


def getInfoDir(dirPath):
    out = subprocess.Popen(['stat', dirPath],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    res = stdout.decode("utf-8")
    attrs = res.split()
    permission = attrs[2]
    dirNode = int(attrs[3])
    dirOwner = attrs[4]
    groupOwner = attrs[5]
    dirSize = int(attrs[7])
    dirName = attrs[-1].split("/")[-1]
    date = formatDate(res)
    dir = Directory(dirPath, dirName, permission, dirOwner, groupOwner, dirSize, dirNode, date)
    subout = subprocess.Popen(['ls', '-lh', dirPath],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    substdout, substderr = subout.communicate()
    if len(substdout) == 0: return dir
    subres = substdout.decode("utf-8").splitlines(True)
    for sub in subres:
        subAttrs = sub.split()
        if subAttrs[0].startswith('d'):
            dir.addDirSub(subAttrs[-1])
    return dir


def formatDate(res):
    temp = res.split("\"")
    date = temp[3].split(":")
    return date[0] + ":" + date[1]


def printLs(objs):
    for obj in objs:
        for o in obj:
            if len(o)!=0:
                print(o)

def findByPattern(pattern,dirs,files):
    resDir=[]
    resFile=[]
    for d in dirs:
        if re.search(pattern, d.dirName) is not None:
            resDir.append(d)
    for f in files:
        if re.search(pattern, f.fname) is not None:
            resFile.append(f)
    return (resDir,resFile)

def findFilesByPattern(pattern,files):
    resFile = []
    for f in files:
        if re.search(pattern, f.fname) is not None:
            resFile.append(f)
    return resFile

def findContentByPattern(pattern,files):
    result = {}
    regex = re.compile(pattern)
    for file in files:
        res=[]
        lines=[]
        try:
            lines = str(file.content.decode(encoding='UTF-8')).splitlines()
        except:
            continue
        for i in range(0,len(lines)):
            if regex.search(lines[i]) is not None:
                l = Line(i,lines[i])
                res.append(l)
        if len(res)>0: result[file.filePath]=res
    return result

def execProg(prog):
    connection = connect()
    path=''
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT pvalue FROM Path WHERE pkey=%s'
            cursor.execute(sql, (prog,))
            result = cursor.fetchone()
            path = result['pvalue']
    finally:
        connection.close()
    if len(path)==0:
        print('No such executable file!')
        return
    # subprocess.run(['/bin/sh','/Users/faushine/Documents/CourseWork/2020Winter/ECE656/project/.testt'])
    pathA=path.split('/')
    dir=''
    for i in range(1,len(pathA)-1):
        dir=dir+'/'+pathA[i]
    fname = pathA[-1]
    cmd1 = 'cd '+dir
    cmd2 = './'+fname
    final = subprocess.Popen("{}; {}".format(cmd1, cmd2), shell=True, stdin=subprocess.PIPE,
                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    stdout, nothing = final.communicate()
    print(stdout.decode(encoding='UTF-8'))

def printLsVerbose(dirs,files):
    for obj in dirs:
        print("{} {:>5}  {}  {} {:>8}  {:>3}  {}".format(obj.permission, obj.dirNode, obj.dirOwner,
                                                   obj.groupOwner, obj.dirSize,
                                                   obj.lastModified, obj.dirName))
    for obj in files:
        print("{} {:>5}  {}  {} {:>8}  {:>3}  {}".format(obj.permission, obj.fileNode, obj.fileOwner,
                                                   obj.groupOwner, obj.fileSize,
                                                   obj.lastModified, obj.fname))

def printLsVerbosePath(dirs,files):
    for obj in dirs:
        print("{} {:>5}  {}  {} {:>8}  {:>3}  {}".format(obj.permission, obj.dirNode, obj.dirOwner,
                                                   obj.groupOwner, obj.dirSize,
                                                   obj.lastModified, obj.dirPath))
    for obj in files:
        print("{} {:>5}  {}  {} {:>8}  {:>3}  {}".format(obj.permission, obj.fileNode, obj.fileOwner,
                                                   obj.groupOwner, obj.fileSize,
                                                   obj.lastModified, obj.filePath))


def printMathchFiles(lines):
    for fname in lines:
        print("Find matching file:",fname)
        for l in lines[fname]:
            print("{} {}".format(l.num,l.content))

def printShowPath():
    connection = connect()
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM Path'
            cursor.execute(sql)
            result = cursor.fetchall()
            for r in result:
                print('{} = {}'.format(r['pkey'],r['pvalue']))
    finally:
        connection.close()

if __name__ == '__main__':
    import re
    r = 'Bat(wo)+man'
    batRegex = re.compile(r)
    mo1 = batRegex.search('The Adventures of Batwoman')
    print(mo1.group())