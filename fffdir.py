#!/usr/bin/env python
import sqlite3 as sq
import os
import sys

def main():
    if len(sys.argv)<2:
        print("Usage: fffdir.py <term> [term] ...")
        return
    args=sys.argv[1:]
    root=os.path.dirname(os.path.abspath(__file__))
    os.chdir(root)
    con=sq.connect('sindex.db')
    con.text_factory = str
    cur=con.cursor()
    ql = ["SELECT path FROM t_dirs WHERE ("]
    conds=[]
    for term in args:
        conds.append("path LIKE '%{}%'".format(term))
    ql.append(' AND '.join(conds))
    ql.append(')')
    cur.execute(''.join(ql))
    res=cur.fetchall()
    i=0
    dir,=res[0]
    print(dir)

if __name__ == '__main__':
    main()

