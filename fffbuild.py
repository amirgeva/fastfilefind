#!/usr/bin/env python3
# -------------------------------------------------------------------------------
# Name:        fffbuild
# Purpose:
#
# Author:      Amir Geva
#
# Created:     07/04/2014
# Copyright:   (c) Amir Geva 2014
# Licence:     GPL V2
# -------------------------------------------------------------------------------
import sqlite3 as sq
import os
import sys
import time


def get_windows_drives():
    import win32api
    import win32file
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    phys = []
    for d in drives:
        if win32file.GetDriveType(d) == win32file.DRIVE_FIXED:
            phys.append(d)
    return phys


def get_linux_drive():
    return ['/']


def get_drives():
    if sys.platform == 'win32':
        return get_windows_drives()
    if sys.platform.startswith('linux'):
        return get_linux_drive()
    print("Unknown platform '{}'".format(sys.platform))
    return []


def create_tables(cur):
    try:
        cur.execute('CREATE TABLE t_dirs(id INTEGER PRIMARY KEY, path TEXT)')
        cur.execute('CREATE INDEX dirs_path_idx ON t_dirs(path);')
    except sq.Error:
        cur.execute('DELETE from t_dirs')
    try:
        cur.execute(
            'CREATE TABLE t_files(file_id INTEGER PRIMARY KEY, name TEXT, dir INTEGER, ext TEXT, size INT, time INT)')
        cur.execute('CREATE INDEX files_name_idx ON t_files(name);')
        cur.execute('CREATE INDEX files_ext_idx ON t_files(ext);')
        cur.execute('CREATE INDEX files_size_idx ON t_files(size);')
        cur.execute('CREATE INDEX files_time_idx ON t_files(time);')
    except sq.Error:
        cur.execute('DELETE from t_files')


def write_dirs(cur, dirs):
    dir_id = 0
    for d in dirs:
        try:
            cur.execute('INSERT INTO t_dirs (id,path) VALUES ("{}","{}")'.format(dir_id, d))
            dir_id = dir_id + 1
        except sq.Error as e:
            print("Error : {}".format(e.args[0]))


def write_files(cur, files):
    for f in files:
        try:
            cur.execute('INSERT INTO t_files (name,dir,ext,size,time) VALUES ("{}",{},"{}",{},{})'.format(*f))
        except sq.Error as e:
            print(f"Error : {e.args[0]}")


def write_db(dirs, files, db_dir):
    try:
        con = sq.connect(os.path.join(db_dir, 'sindex.db'))
        cur = con.cursor()
        create_tables(cur)
        write_dirs(cur, dirs)
        write_files(cur, files)
        con.commit()
    except sq.Error as e:
        print("Error : {}".format(e.args[0]))


def scan(excludes, dirs, files, base):
    for dir_path, dir_names, filelist in os.walk(base):
        dir_names[:] = [
            dn for dn in dir_names
            if os.path.join(dir_path, dn) not in excludes]
        idx = len(dirs)
        if (idx & 255) == 0:
            print("{} {}".format(len(files), dir_path))
        dirs.append(dir_path)
        for f in filelist:
            fullpath = os.path.join(dir_path, f)
            base, ext = os.path.splitext(fullpath)
            file_size = 0
            file_time = 0
            try:
                file_size = os.path.getsize(fullpath)
                file_time = os.path.getmtime(fullpath)
            except OSError:
                pass
            files.append([f, idx, ext, file_size, file_time])


def main():
    start = time.time()
    drives = get_drives()
    excludes = []
    db_dir = os.path.dirname(os.path.abspath(__file__))
    for line in open(os.path.join(db_dir, "fffbuild.cfg")):
        if line.startswith("exclude="):
            directory = line[8:]
            excludes.append(directory.strip())
    print("Excluding:")
    print(excludes)
    dirs = []
    files = []
    for d in drives:
        if d not in excludes:
            scan(excludes, dirs, files, d)
    end = time.time()
    print("Scan took {} second".format(int(end - start)))
    start = end
    write_db(dirs, files, db_dir)
    end = time.time()
    print("Database write took {} seconds".format(int(end - start)))


if __name__ == '__main__':
    main()
