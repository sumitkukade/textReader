import sqlite3,sys,time
import fractions
import textwrap
import json
import os


def findLcmOfTwoNum(num1,num2):
    return (num1*num2)/fractions.gcd(num1,num2)

def lcm(numList):
    return reduce(lambda x,y:findLcmOfTwoNum(x,y),numList)

def findLineCount(numList):
    lcmNum =lcm(numList)
    return map(lambda x : lcmNum/x,numList)

def findCharacterWithinLine(numList):
    lcmNum = lcm(numList)
    divList = []
    gcdNum = reduce(lambda x,y:fractions.gcd(x,y),numList)
    divList = map(lambda x: x/gcdNum ,numList)
    return map(lambda x : lcmNum/x,divList)

def maketextWraperList(numList):
    lineCountList = findLineCount(numList)
    characterCountList = findCharacterWithinLine(numList)
    return zip(numList,lineCountList,characterCountList)


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
    textList = []
    textWrapWidthList = []
    textWrapWidthList = maketextWraperList([10,15,20,25,30])
    textList = filter(lambda x: x[0]==fontSize ,textWrapWidthList)[0][1:]
    n = (textList[0]*textList[1])
    wrapper = textwrap.TextWrapper(width=n)
    dedented_text = textwrap.dedent(text=data)
    original = wrapper.fill(text=dedented_text)
    originalList = original.split("\n")
    oLen = len(originalList)
    json_data = []
    dataList = {}
    dataList["sizeOfFile"] = oLen - 1
    json_data.append(dataList)
    index = 0
    for elem in originalList:
        dataList[str(index)] = elem
        index = index + 1
    fileDetails = json.dumps(dataList)
    return fileDetails



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
    fontSize = data_dict["fontSize"] 
    fileName = data_dict["fileName"]
    pageCount = data_dict["pageCount"]
    fontSize = int(fontSize)
    pageCount = int(pageCount)
    if(fileExists(fileName) == 0):
        return 0
    else:
        fileContent = ""
        data = fetchFileContent(fileName)
        return makePageWiseContent(data,fontSize,pageCount)

def fileContentWithPageNumber(data):
    data_dict = json.loads(data)
    fontSize = data_dict["fontSize"]
    fileName = data_dict["fileName"]
    pageCount = data_dict["pageCount"]
    fileContent = fetchFileContent(fileName)
    return makePageWiseContent(fileContent,fontSize,pageCount)


