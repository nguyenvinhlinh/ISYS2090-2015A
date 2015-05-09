__author__ = 'Nguyen Vinh Linh & Nguyen Duy Kien'
from sql_test_lib import connect
from Exercise1 import execute_query

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
    connection = connect("bit")
    cursor = connection.cursor()
    new_table_sql = ""
    execute_query(cursor, new_table_sql, None, None)
    connection.commit()
    connection.close()


the_file = check_file_sql()
print(the_file.__class__)
if the_file.__class__ == file:
    list = extract_sql(the_file)
