#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        fffbuild
# Purpose:
#
# Author:      Amir Geva
#
# Created:     07/04/2014
# Copyright:   (c) Amir Geva 2014
# Licence:     GPL V2
#-------------------------------------------------------------------------------
import sqlite3 as sq
import os
import sys
import time

def getWindowsDrives():
    import win32api
    import win32file
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    phys=[]
    for d in drives:
        if win32file.GetDriveType(d) == win32file.DRIVE_FIXED:
            phys.append(d)
    return phys
    
def getLinuxDrive():
    return ['/']

def getDrives():
    if sys.platform == 'win32':
        return getWindowsDrives()
    if sys.platform.startswith('linux'):
        return getLinuxDrive()
    print "Unknown platform '{}'".format(sys.platform)
    return []

def createTables(cur):
    try:
        cur.execute('CREATE TABLE t_dirs(id INTEGER PRIMARY KEY, path TEXT)')
        cur.execute('CREATE INDEX dirs_path_idx ON t_dirs(path);')
    except sq.Error, e:
        cur.execute('DELETE from t_dirs')
    try:
        cur.execute('CREATE TABLE t_files(file_id INTEGER PRIMARY KEY, name TEXT, dir INTEGER, ext TEXT, size INT, time INT)')
        cur.execute('CREATE INDEX files_name_idx ON t_files(name);')
        cur.execute('CREATE INDEX files_ext_idx ON t_files(ext);')
        cur.execute('CREATE INDEX files_size_idx ON t_files(size);')
        cur.execute('CREATE INDEX files_time_idx ON t_files(time);')
    except sq.Error, e:
        cur.execute('DELETE from t_files')

def writeDirs(cur,dirs):
    id=0;
    for d in dirs:
        cur.execute('INSERT INTO t_dirs (id,path) VALUES ("{}","{}")'.format(id,d))
        id=id+1

def writeFiles(cur,files):
    for f in files:
        cur.execute('INSERT INTO t_files (name,dir,ext,size,time) VALUES ("{}",{},"{}",{},{})'.format(*f))

def writeDB(dirs,files,dbDir):
    try:
        con=sq.connect(os.path.join(dbDir,'sindex.db'))
        cur=con.cursor()
        createTables(cur)
        writeDirs(cur,dirs)
        writeFiles(cur,files)
        con.commit()
    except sq.Error, e:
        print "Error : {}".format(e.args[0])

def scan(excludes,dirs,files,base):
    total=0
    for dirpath,dirnames,filelist in os.walk(base):
        dirnames[:] = [
            dn for dn in dirnames
            if os.path.join(dirpath, dn) not in excludes ]
        idx=len(dirs)
        if ((idx&255)==0):
            print "{} {}".format(len(files),dirpath)
        dirs.append(dirpath)
        for f in filelist:
            fullpath=os.path.join(dirpath,f)
            base,ext=os.path.splitext(fullpath)
            filesize=0
            filetime=0
            try:
                filesize=os.path.getsize(fullpath);
                filetime=os.path.getmtime(fullpath)
            except Exception,e:
                pass
            files.append([f,idx,ext,filesize,filetime])

def main():
    start=time.time()
    drives=getDrives()
    excludes=[]
    dbDir=os.path.dirname(os.path.abspath(__file__))
    for line in open(os.path.join(dbDir,"fffbuild.cfg")):
        if (line.startswith("exclude=")):
            dir=line[8:]
            excludes.append(dir.strip())
    print "Excluding:"
    print excludes
    dirs=[]
    files=[]
    for d in drives:
        if d not in excludes:
            scan(excludes,dirs,files,d)
    end=time.time()
    print "Scan took {} second".format(int(end-start))
    start=end
    writeDB(dirs,files,dbDir)
    end=time.time()
    print "Database write took {} seconds".format(int(end-start))

if __name__ == '__main__':
    main()
