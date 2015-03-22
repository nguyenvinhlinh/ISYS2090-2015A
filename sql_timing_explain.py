#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
from sql_test_lib import connect
import re

# connect to DB and execute query
con = connect("bit")
cur = con.cursor()
query = "EXPLAIN ANALYSE SELECT * FROM college.student;"

try:
    cur.execute(query)
except psycopg2.ProgrammingError, e:
    print e
    con.commit()
    con.close()

# parse the results of the query to extract running times
actual_time_re = re.compile(r"actual time=(\d+\.\d*)\.{2}(\d+\.\d*) rows")
runtime_re = re.compile(r"Total runtime: (\d+\.\d*) ms")

for tup in cur.fetchall():
    print tup[0]
    actual_time = actual_time_re.search(tup[0])
    if actual_time:
        print actual_time.groups()
    runtime = runtime_re.search(tup[0])
    if runtime:
        print runtime.groups()

con.commit()
con.close()