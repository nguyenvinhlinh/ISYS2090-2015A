__author__ = 'Nguyen Vinh Linh & Nguyen Duy Kien'
from sql_test_lib import connect
import time
import re

def check_file_sql(file_name=None):
    """
    @param file_name: input parameter, string, name of file
    @return the_file: the file object
    """
    if file_name is None:
        file_name = raw_input("Enter file name: ")
    if file_name[-4:] != ".sql":
        print("Invalid chosen file. File must be .sql")
        return False
    try:
        the_file = open(file_name, "r")
        return the_file
    except IOError as ex:
        print("File not found")
        return False


def extract_sql(the_file):
    """
    @param the_file: input parameter, file object
    @return sql_list: list of all sql command
    """
    content = the_file.read().replace("\n", "")
    sql_list = content.split(";")
    # remove the last element, cause, the last character is ';'
    sql_list.pop()
    # Add ';' to end of each sql command
    for i in range(0, len(sql_list)):
        sql_list[i] += ";"
    return sql_list


def make_exe2_db():
    connection = connect("bit","bit","bit")
    cursor = connection.cursor()
    new_table_sql = "CREATE TABLE academics.sql_analysis (ID SERIAL PRIMARY KEY, " \
                    "DateTime TIMESTAMP NOT NULL," \
                    "ActualTime1 REAL NOT NULL," \
                    "ActualTime2 REAL NOT NULL," \
                    "TotalRuntime INTERVAL NOT NULL," \
                    "CSExeTime INTERVAL NOT NULL," \
                    "TextQuery TEXT NOT NULL )"
    cursor.execute(new_table_sql)
    connection.commit()
    connection.close()


def drop_exe2_db():
    connection = connect("bit","bit","bit")
    cursor = connection.cursor()
    new_table_sql = "DROP TABLE academics.sql_analysis;"
    cursor.execute(new_table_sql)
    connection.commit()
    connection.close()


def query_analysis(sql_list):
    print("wololo")
    connection = connect("bit")
    cursor = connection.cursor()
    for query in sql_list:
        analysis_query = "EXPLAIN ANALYZE " + query
        clientside_begin_time = time.clock()
        cursor.execute(query)
        connection.commit()
        clientside_end_time = time.clock()
        # This is Client-side exe time
        clientside_exe_time = clientside_end_time - clientside_begin_time
        print("Clientside time: %s %s %s" %(str(clientside_begin_time), str(clientside_end_time), str(clientside_exe_time)))

        cursor.execute(analysis_query)
        connection.commit()

        # Regular expression for first line
        regular1 = re.compile(r"actual time=(\d+\.\d*)\.{2}(\d+\.\d*) rows")
        # Regular expression for second line
        regular2 = re.compile(r"Total runtime: (\d+\.\d*) ms")

        receive_data = cursor.fetchall()
        m = regular1.search(str(receive_data[0]))
        if m is not None:
            actual_time1 = str(m.groups()[0])
            actual_time2 = str(m.groups()[1])
            actual_runtime = str(regular2.search(str(receive_data[1])).groups()[0])
            print(actual_time1 + "+++++" + actual_time2+ "+++++"+ actual_runtime + "+++++"+ str(clientside_exe_time))
            # Insert data to database named academics.sql_analysis
            sql_text = "INSERT INTO academics.sql_analysis(DateTime, ActualTime1, ActualTime2, TotalRuntime,CSExeTime, TextQuery) VALUES " \
                       "(%s, '%s', '%s', '%s', '%s', '%s');" % ("now()", actual_time1,actual_time2,
                                                                actual_runtime, clientside_exe_time, query)

            cursor.execute(sql_text)
            connection.commit()

def test_re():
    string_res1 = "Seq Scan on academic  (cost=0.00..8.58 rows=358 width=72) (actual time=0.008..0.084 rows=358 loops=1)"
    string_res2 = "Total runtime: 0123.170 ms"
    # Using () to extract time data easier with groups() method.
    regular1 = re.compile(r"actual time=(\d+\.\d*)\.{2}(\d+\.\d*) rows")
    res1 = regular1.search(string_res1)
    print(str(res1.groups()[0]))
    print(str(res1.groups()[1]))

    regular2 = re.compile(r"Total runtime: (\d+\.\d*) ms")
    res2 = regular2.search(string_res2)
    print(str(res2.groups()[0]))

#
#make_exe2_db()
#drop_exe2_db()
the_file = check_file_sql()
print(the_file.__class__)
if the_file.__class__ == file:
    sql_list = extract_sql(the_file)
    query_analysis(sql_list)


