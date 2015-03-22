#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
from sql_test_lib import connect
from time import clock

# connect to DB and execute query
con = connect("bit")
cur = con.cursor()
query = "SELECT * FROM college.student;"
try:
    start = clock()
    for i in range(1000):
        cur.execute(query)
    end = clock()
except psycopg2.ProgrammingError, e:
    print e
    con.commit()
    con.close()

print "exec time:", end-start, "seconds."
con.commit()
con.close()