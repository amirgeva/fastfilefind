#!/usr/bin/env python3
import sqlite3 as sq
import os
import sys
import re
import numpy as np


def levenshein(a, b):
    na = len(a)
    nb = len(b)
    m = np.zeros((na + 1, nb + 1))
    for i in range(nb):
        m[0][i + 1] = i + 1
    for i in range(na):
        m[i + 1][0] = i + 1
    for i in range(na):
        for j in range(nb):
            swap_cost = 0
            if a[i].upper() != b[j].upper():
                swap_cost = 1
            swap = m[i][j] + swap_cost
            insert = m[i][j + 1] + 1
            delete = m[i + 1][j] + 1
            m[i + 1][j + 1] = min(insert, min(delete, swap))
    return m[na][nb]


def find_best_match(dirs, args):
    scores = {}
    for dir in dirs:
        parts = re.split(r'/|\\', dir)
        parts = [p for p in parts if len(p) > 0]
        for arg in args:
            for part in parts:
                if arg.upper() in part.upper():
                    distance = levenshein(arg, part)
                    if distance < len(arg):
                        score = 1.0 / (1.0 + distance)
                        if dir in scores:
                            score = score + scores[dir]
                        scores[dir] = score
    max_score = 0
    res = ''
    for dir in scores:
        score = scores.get(dir)
        if score > max_score:
            max_score = score
            min_len = len(dir)
            res = dir
        elif score == max_score and len(dir) < len(res):
            res = dir
    return res


def main():
    if len(sys.argv) < 2:
        print("Usage: fffdir.py <term> [term] ...")
        return
    args = sys.argv[1:]
    root = os.path.dirname(os.path.abspath(__file__))
    con = sq.connect(os.path.join(root, 'sindex.db'))
    con.text_factory = str
    cur = con.cursor()
    ql = ["SELECT path FROM t_dirs WHERE ("]
    conds = []
    for term in args:
        conds.append("path LIKE '%{}%'".format(term))
    ql.append(' AND '.join(conds))
    ql.append(')')
    cur.execute(''.join(ql))
    res = cur.fetchall()
    i = 0
    if len(res) == 0:
        print(os.getcwd())
    else:
        res = [d[0] for d in res]
        print(find_best_match(res, args))


if __name__ == '__main__':
    main()
