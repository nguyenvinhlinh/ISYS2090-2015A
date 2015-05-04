__author__ = 'Nguyen Vinh Linh & Nguyen Duy Kien'

def checkFileSQL():
    fileName = raw_input("Enter file name: ")
    if fileName[-4:] != ".sql":
        print("Invalid choosen file. File must be .sql")
        return False
    try:
        thefile = open(fileName, "r")
        return True
    except IOError as ex:
        print("File not found")
        return False


validFile = checkFileSQL()
print("return value: "+str(validFile))