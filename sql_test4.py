#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sql_test_lib import *
import sys


con = dblogin("bit")
while con:
    cur = con.cursor()
    print "Enter the last name: ",
    last = sys.stdin.readline()[:-1]
    if last == "exit":
        break
    print "Enter the first name: ",
    first = sys.stdin.readline()[:-1]
    query = "SELECT * FROM bank.client WHERE lastname = '%s' AND firstname = '%s'" % (last, first)
    print query
    execute_and_print(cur, query)    
    con.commit()

if con:
    con.close()