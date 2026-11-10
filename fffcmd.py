#!/usr/bin/env python3
# -------------------------------------------------------------------------------
# Name:        fffcmd
# Purpose:     Command line search interface for fastfilefind
#
# Author:      Amir Geva
#
# Created:     04/04/2026
# Copyright:   (c) Amir Geva 2026
# Licence:     GPL V2
# -------------------------------------------------------------------------------
import sqlite3 as sq
import os
import argh
from datetime import datetime, date


def date_format(t):
    try:
        return str(date.fromtimestamp(t))
    except (ValueError, OSError):
        return '?'


def build_conditions(ql, term, ext, exact, size_less, size_greater, before, after):
    if term:
        if exact:
            ql.append(" AND (name = '{}')".format(term))
        else:
            for t in term.split():
                if t:
                    ql.append(" AND (name LIKE '%{}%')".format(t))
    if ext:
        ql.append(" AND (ext=='.{}')".format(ext))
    if size_less is not None:
        ql.append(" AND (size < {})".format(size_less))
    if size_greater is not None:
        ql.append(" AND (size > {})".format(size_greater))
    if before:
        d = datetime.strptime(before, "%Y-%m-%d")
        s = (d - datetime.utcfromtimestamp(0)).total_seconds()
        ql.append(" AND (time < {})".format(s))
    if after:
        d = datetime.strptime(after, "%Y-%m-%d")
        s = (d - datetime.utcfromtimestamp(0)).total_seconds()
        ql.append(" AND (time > {})".format(s))


def search_files(cur, base, term, ext, exact, size_less, size_greater, before, after):
    ql = ["SELECT name, dir, ext, size, time, path FROM t_files INNER JOIN t_dirs ON t_files.dir==t_dirs.id WHERE (1=1"]
    if base:
        ql.append(" AND (path LIKE '{}%')".format(base))
    build_conditions(ql, term, ext, exact, size_less, size_greater, before, after)
    ql.append(');')
    cur.execute(''.join(ql))
    return cur.fetchall()


def search_archive_files(cur, base, term, ext, exact, size_less, size_greater, before, after):
    ql = ["SELECT af.name, af.dir, af.ext, af.size, af.time, ad.path, a.path"
          " FROM t_archive_files af"
          " INNER JOIN t_archive_dirs ad ON af.dir==ad.id"
          " INNER JOIN t_archives a ON ad.archive==a.id"
          " WHERE (1=1"]
    if base:
        ql.append(" AND (a.path LIKE '{}%')".format(base))
    build_conditions(ql, term, ext, exact, size_less, size_greater, before, after)
    ql.append(');')
    cur.execute(''.join(ql))
    return cur.fetchall()


def search(term='', *, ext='', exact=False, base='',
           size_less=None, size_greater=None,
           before='', after='',
           no_archives=False):
    """Search the file index database.

    :param term: Search term (space separated words matched against filename)
    :param ext: Filter by file extension (without dot)
    :param exact: Match filename exactly
    :param base: Base directory filter
    :param size_less: Show files smaller than this size in bytes
    :param size_greater: Show files larger than this size in bytes
    :param before: Show files modified before date (YYYY-MM-DD)
    :param after: Show files modified after date (YYYY-MM-DD)
    :param no_archives: Skip archive search
    """
    if not term and not ext and not base and size_less is None and size_greater is None and not before and not after:
        print("No search filters specified. Run with --help for usage.")
        return

    root = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(root, 'sindex.db')
    if not os.path.exists(db_path):
        print("Database not found. Run fffbuild.py first.")
        return
    con = sq.connect(db_path)
    con.text_factory = str
    cur = con.cursor()

    rows = search_files(cur, base, term, ext, exact, size_less, size_greater, before, after)
    arc_rows = []
    if not no_archives:
        arc_rows = search_archive_files(cur, base, term, ext, exact, size_less, size_greater, before, after)

    if not rows and not arc_rows:
        print("No results found.")
        return

    name_w = 4
    path_w = 4
    size_w = 4
    date_w = 10
    results = []
    for r in rows:
        name, dir_id, ext_val, size, t, path = r
        results.append((name, path, size, t, ''))
    for r in arc_rows:
        name, dir_id, ext_val, size, t, arc_dir, arc_path = r
        results.append((name, arc_dir, size, t, arc_path))

    for name, path, size, t, arc in results:
        name_w = max(name_w, len(name))
        path_w = max(path_w, len(path))
        size_w = max(size_w, len(str(size)))

    fmt = '{:<{nw}}  {:<{pw}}  {:>{sw}}  {:<{dw}}'
    has_archives = any(r[4] for r in results)
    if has_archives:
        fmt += '  {}'
    header = fmt.format('Name', 'Path', 'Size', 'Date',
                        *(['Archive'] if has_archives else []),
                        nw=name_w, pw=path_w, sw=size_w, dw=date_w)
    print(header)
    print('-' * len(header))

    for name, path, size, t, arc in results:
        line = fmt.format(name, path, size, date_format(t),
                          *([arc] if has_archives else []),
                          nw=name_w, pw=path_w, sw=size_w, dw=date_w)
        print(line)

    print("\n{} results found.".format(len(results)))


if __name__ == '__main__':
    argh.dispatch_command(search)
