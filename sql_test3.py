#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sql_test_lib import *
import sys


con = dblogin("bit")
while con:
    cur = con.cursor()
    print "Enter your query: ",
    query = sys.stdin.readline()
    if query[:-1] == "exit":
        break
    execute_and_print(cur, query)    
    con.commit()

if con:
    con.close()