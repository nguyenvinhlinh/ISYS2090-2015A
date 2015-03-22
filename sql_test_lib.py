#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import getpass


def connect(dbname=None, user=None, password=None, host=None, port=None):
    if user is None:
        user = getpass.getuser()
    if password is None:
        password = getpass.getpass()
    if dbname is None:
        dbname = user
    connect_str = "dbname=%s user=%s password=%s" % (dbname, user, password)
    if host is not None:
        connect_str += " host=%s" % host
        if port is not None:
            connect_str += " port=%s" % port
    return psycopg2.connect(connect_str)


def dblogin(db, attempts=3):
    for i in range(attempts):
        try:
            con = connect(dbname=db)
        except psycopg2.OperationalError, e:
            print e
        if con:
            return con
    return None


def execute_and_print(cur, query):
    try:
        cur.execute(query)
        print
        desc = cur.description
        widths = []
        for c in range(len(desc)):
            if len(desc[c][0]) > desc[c][2]:
                widths.append(len(desc[c][0]))
            else:
                widths.append(desc[c][2])
            print desc[c][0], ' '*(widths[c]-len(desc[c][0])),
        print
        for tup in cur.fetchall():
            for c in range(len(tup)):
                print tup[c], ' '*(widths[c]-len(str(tup[c]))),
            print
        print
    except psycopg2.ProgrammingError, e:
        print e
