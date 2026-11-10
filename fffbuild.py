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
import zipfile
import py7zr


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
    try:
        cur.execute('CREATE TABLE t_archives(id INTEGER PRIMARY KEY, path TEXT)')
        cur.execute('CREATE INDEX archives_path_idx ON t_archives(path);')
    except sq.Error:
        cur.execute('DELETE from t_archives')
    try:
        cur.execute('CREATE TABLE t_archive_dirs(id INTEGER PRIMARY KEY, archive INTEGER, path TEXT)')
        cur.execute('CREATE INDEX archive_dirs_archive_idx ON t_archive_dirs(archive);')
        cur.execute('CREATE INDEX archive_dirs_path_idx ON t_archive_dirs(path);')
    except sq.Error:
        cur.execute('DELETE from t_archive_dirs')
    try:
        cur.execute(
            'CREATE TABLE t_archive_files(file_id INTEGER PRIMARY KEY, name TEXT, dir INTEGER, ext TEXT, size INT, time INT)')
        cur.execute('CREATE INDEX archive_files_name_idx ON t_archive_files(name);')
        cur.execute('CREATE INDEX archive_files_ext_idx ON t_archive_files(ext);')
        cur.execute('CREATE INDEX archive_files_size_idx ON t_archive_files(size);')
        cur.execute('CREATE INDEX archive_files_time_idx ON t_archive_files(time);')
    except sq.Error:
        cur.execute('DELETE from t_archive_files')


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


def write_archives(cur, archives):
    arc_id = 0
    for a in archives:
        try:
            cur.execute('INSERT INTO t_archives (id,path) VALUES ("{}","{}")'.format(arc_id, a))
            arc_id = arc_id + 1
        except sq.Error as e:
            print("Error : {}".format(e.args[0]))


def write_archive_dirs(cur, archive_dirs):
    dir_id = 0
    for d in archive_dirs:
        try:
            cur.execute('INSERT INTO t_archive_dirs (id,archive,path) VALUES ("{}",{},"{}") '.format(dir_id, d[0], d[1]))
            dir_id = dir_id + 1
        except sq.Error as e:
            print("Error : {}".format(e.args[0]))


def write_archive_files(cur, archive_files):
    for f in archive_files:
        try:
            cur.execute('INSERT INTO t_archive_files (name,dir,ext,size,time) VALUES ("{}",{},"{}",{},{})'.format(*f))
        except sq.Error as e:
            print(f"Error : {e.args[0]}")


def write_db(dirs, files, archives, archive_dirs, archive_files, db_dir):
    try:
        con = sq.connect(os.path.join(db_dir, 'sindex.db'))
        cur = con.cursor()
        create_tables(cur)
        write_dirs(cur, dirs)
        write_files(cur, files)
        write_archives(cur, archives)
        write_archive_dirs(cur, archive_dirs)
        write_archive_files(cur, archive_files)
        con.commit()
    except sq.Error as e:
        print("Error : {}".format(e.args[0]))


def scan_zip(fullpath, archives, archive_dirs, archive_files):
    try:
        with zipfile.ZipFile(fullpath, 'r') as zf:
            arc_id = len(archives)
            archives.append(fullpath)
            print("[zip] {} {}".format(len(archive_files), fullpath))
            dir_map = {}
            for info in zf.infolist():
                if info.is_dir():
                    continue
                name = info.filename
                dir_part = os.path.dirname(name)
                if dir_part not in dir_map:
                    dir_map[dir_part] = len(archive_dirs)
                    archive_dirs.append((arc_id, dir_part))
                dir_idx = dir_map[dir_part]
                basename = os.path.basename(name)
                _, ext = os.path.splitext(basename)
                dt = info.date_time
                file_time = int(time.mktime(dt + (0, 0, -1)))
                archive_files.append([basename, dir_idx, ext, info.file_size, file_time])
    except Exception as e:  # corrupt files, unsupported features...
        print("[zip] skipped {}: {}".format(fullpath, type(e).__name__))


def scan_7z(fullpath, archives, archive_dirs, archive_files):
    try:
        with py7zr.SevenZipFile(fullpath, 'r') as zf:
            arc_id = len(archives)
            archives.append(fullpath)
            print("[7z] {} {}".format(len(archive_files), fullpath))
            dir_map = {}
            for info in zf.list():
                if info.is_directory:
                    continue
                name = info.filename
                dir_part = os.path.dirname(name)
                if dir_part not in dir_map:
                    dir_map[dir_part] = len(archive_dirs)
                    archive_dirs.append((arc_id, dir_part))
                dir_idx = dir_map[dir_part]
                basename = os.path.basename(name)
                _, ext = os.path.splitext(basename)
                file_time = int(info.creationtime.timestamp()) if info.creationtime else 0
                archive_files.append([basename, dir_idx, ext, info.uncompressed, file_time])
    except Exception as e:  # encrypted headers, unsupported methods, corrupt files...
        print("[7z] skipped {}: {}".format(fullpath, type(e).__name__))


def scan(excludes, dirs, files, archives, archive_dirs, archive_files, base):
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
            if ext.lower() == '.zip':
                scan_zip(fullpath, archives, archive_dirs, archive_files)
            elif ext.lower() == '.7z':
                scan_7z(fullpath, archives, archive_dirs, archive_files)


def main():
    start = time.time()
    if len(sys.argv) > 1:
        drives = [sys.argv[1]]
    else:
        drives = get_drives()
    excludes = []
    extra_drives = []
    db_dir = os.path.dirname(os.path.abspath(__file__))
    for line in open(os.path.join(db_dir, "fffbuild.cfg")):
        if line.startswith("exclude="):
            directory = line[8:]
            excludes.append(directory.strip())
        elif line.startswith("include="):
            extra_drives.extend(line[8:].strip().split())
    if len(sys.argv) <= 1:
        drives.extend(extra_drives)
    print("Excluding:")
    print(excludes)
    dirs = []
    files = []
    archives = []
    archive_dirs = []
    archive_files = []
    for d in drives:
        if d not in excludes:
            scan(excludes, dirs, files, archives, archive_dirs, archive_files, d)
    end = time.time()
    print("Scan took {} second".format(int(end - start)))
    print("Found {} archives with {} files".format(len(archives), len(archive_files)))
    start = end
    write_db(dirs, files, archives, archive_dirs, archive_files, db_dir)
    end = time.time()
    print("Database write took {} seconds".format(int(end - start)))


if __name__ == '__main__':
    main()
