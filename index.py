import sqlite3,sys,time
import textwrap
import json
import os

textWrapWidthList = [(10,145,30),(15,100,20),(20,70,15),(25,55,12)]

def sqliteConnection():
    conn = sqlite3.connect("/home/reshma/InternShip/textReader/file.db")
    c = conn.cursor()
    return conn,c

def sqliteCloseConnection(conn):
    conn.commit()
    conn.close()

def fileExists(fileName):
    conn,c = sqliteConnection()
    c.execute("select ? in  (select filename from fileDomain)",(fileName,))
    fileExists = c.fetchall()
    sqliteCloseConnection(conn)
    isfileExist = fileExists[0][0]
    return isfileExist



def makePageWiseContent(data,fontSize,cnt):
    textList = filter(lambda x: x[0]==fontSize ,textWrapWidthList)[0][1:]
    n = (textList[0]*textList[1])+10
    wrapper = textwrap.TextWrapper(width=n)
    dedented_text = textwrap.dedent(text=data)
    original = wrapper.fill(text=dedented_text)
    originalList = original.split("\n")
    o = []
    index = 0
    for elem in originalList:
        fileData = {}
        fileData[str(index)] = elem
        index = index + 1
        o.append(fileData)
    print o
    return originalList[cnt]



def fetchFileContent(fileName):
    conn,c = sqliteConnection()
    c.execute("select fileContent from fileDomain where filename =?",(fileName,))
    data = c.fetchall()
    sqliteCloseConnection(conn)
    dataList = ""
    for elem in data[0][0]:
        dataList = dataList + elem
    return dataList

def getFontSize():
    conn,c = sqliteConnection()
    c.execute("select fontSize from fontSizeDomain")
    data = c.fetchall()
    sqliteCloseConnection(conn)
    dataList = []
    dataList = map(lambda x : x[0],data)
    return dataList


def main(data):
    data_dict = json.loads(data)
    fontSize = data_dict["Size"] 
    fileName = data_dict["fileName"]
    fontSize = int(fontSize)
    if(fileExists(fileName) == 0):
        return 0
    else:
        fileContent = ""
        data = fetchFileContent(fileName)
        return makePageWiseContent(data,fontSize,0)

def fileContentWithPageNumber(data):
    data_dict = json.loads(data)
    fontSize = data_dict["fontSize"]
    fileName = data_dict["fileName"]
    pageCount = data_dict["pageCount"]
    fileContent = fetchFileContent(fileName)
    return makePageWiseContent(fileContent,fontSize,pageCount)

def fileContentWithbackPageNumber(req):
    req.content_type="Content-Type: application/text"
    fileDetails = req.form.getfirst("FormData","no form parameter")
    fileName,pageCount,fontSize = fileDetails.split(" ")
    fontSize = int(fontSize)
    pageCount = int(pageCount)
    if(pageCount == -1):
        return "ERROR"
    data = fetchFileContent(fileName)
    return pageCount
    #return makePageWiseContent(data,fontSize,pageCount)


