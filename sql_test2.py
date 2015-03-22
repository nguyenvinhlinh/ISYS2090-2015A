#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
from sql_test_lib import connect
import sys


con = connect("bit")
cur = con.cursor()
print "Enter your query: ",
query = sys.stdin.readline()
try:
    cur.execute(query)

    for tup in cur.fetchall():
        print tup
except psycopg2.ProgrammingError, e:
    print e
    
con.commit()
con.close()