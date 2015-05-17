#author: Nguyen Vinh Linh & Nguyen Duy Kien
import psycopg2
from sql_test_lib import connect
import requests
import HTML as html
import re


def execute_query(cursor=None, query=None, filename=None, format=None):
    cursor_is_given = False
    if cursor is None:
        connection = connect("bit")
        cursor = connection.cursor()
        cursor_is_given = False
    else:
        cursor_is_given = True
    if query is None:
        query = "SELECT * FROM academics.academic"
    output = ""
    output_array = []
    try:
        cursor.execute(query)
        for tup in cursor.fetchall():
            output += str(tup) + "\n"
            output_array.append(tup)
        # for Printing all data
        # for i in output_array:
        #     print i
    except psycopg2.ProgrammingError, e:
        print e
    if(cursor_is_given == False):
        connection.commit()
        connection.close()
    # print to file
    if filename is not None:
        if format == "html":
            print "print in html"
            # f = open(filename+"."+format, 'w')
            # f.write("<table border=\"1\">")
            # output = output.replace('(', '<tr><td>')
            # output = output.replace(',', '</td><td>')
            # output = output.replace(')', '</td></tr>')
            # f.write(output)
            # f.write("</table>")
            # f.close()
            a = html.table(output_array)
            print(a)

        elif format == "csv":
            print "print in csv"
            output = output.replace('(', '')
            output = output.replace(')', '')
            output = output.replace('\'', '')
            print output
            f = open(filename + "." + format, 'w')
            f.write(output)
            f.close()
        elif format(format == "none"):
            print("print in no documentation")
            print(output)
        else:
            format = "txt"
            print "print in txt"
            f = open(filename + "." + format, 'w')
            f.write(output)
            f.close()

    return


def main1():
    filename = "out"
    formatf = "txt"
    while True:
        console = raw_input()
        if console[0:9] == "filename=":
            filename = console[9:]
            print "filename: " + filename
        elif console[0:7] == "format=":
            formatf = console[7:]
            print "format: " + formatf
        elif console[0:3] == "exe":
            print "filename=" + filename + ", format=" + formatf
            execute_query(filename=filename, format=formatf)
        elif console == "exit":
            break
    return


def main2():
    response = requests.get("http://www.debian.org/CD/http-ftp/")

    li_list = re.findall(r'(<li>.+<a rel=.+</a></li>)', response.text, re.IGNORECASE)
    hostname_list = []
    url_list = []

    for line in li_list:
        country = (line.split(":")[0][4:])  # take the country, remove li
        url_name = (line.split(":")[1][1:])  # take the url_name, remove first space
        hostname_list.append(country + "-" + url_name)
        href_list = line.split('href="')
        line_url = ""
        for href in href_list:
            href_check = re.search(r'.*://.*', href, re.IGNORECASE)
            if href_check != None:
                # print(href.split('">')[0])
                if line_url == "":
                    line_url = href.split('">')[0]
                else:
                    line_url = line_url+", " + href.split('">')[0]
                print(line_url)
                url_list.append(line_url)

    for i in range(0, len(hostname_list)):
        print(hostname_list[i] + "-->" + url_list[i])
    #  Make cursor
    connection = connect("bit")
    cursor = connection.cursor()
    #  Making Table
    query_make_table = "CREATE TABLE academics.Debian_DB(\
                        ID SERIAL PRIMARY KEY , \
                        HostName VARCHAR(70) NOT NULL, \
                        Url VARCHAR(255) NOT NULL)"
    execute_query(cursor=cursor, query=query_make_table, format="none")
    connection.commit()
    # Inserting data into the db
    for i in range(0, len(hostname_list)):
        insert_query = "INSERT INTO academics.Debian_DB(hostname, url) \
                        VALUES ('%s', '%s')" % (hostname_list[i], url_list[i])
        execute_query(cursor=cursor, query=insert_query, format="none")
        connection.commit()
    connection.close()

main2()
