import MySQLdb
from subprocess import call
from config_path import data
from mod_python import Session
import zipfile
def index():
    db = MySQLdb.connect(
    host="localhost",
    user=data.mysql_user,
    passwd=data.mysql_pswd,
    db="userInputDatabase" )
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # prepare a cursor object using cursor() method
    cursor = db.cursor();
    ss="""select *from applicationProcess.studentApplicationQueue  where tostate="ModificationSuccessfully";"""
    
    cursor.execute(ss);
    rs=cursor.fetchall();
    

    flall=[]
    zf = zipfile.ZipFile(data.path+'/project_data/new_zip.zip', mode='w')
    for i in rs:
               
                docm=str(i[2]);
                
                if docm=='APIB':
                    filename="""%s_International_bonafide.pdf"""%(i[1]);
                elif docm=='APBN':
                    filename="""%s_BONAFIDE.pdf"""%(i[1])
                elif docm=='APFS':
                     filename="""%s_FEES_STRUCTURE.pdf"""%(i[1]);
                elif docm=='APND':
                     filename="""%s_NO_DUES.pdf"""%(i[1])
                flall.append(filename);

    for i in flall:
                 try:
                     fp=open(data.dpath+"/"+i,"r")
                 except:
                       return "First  print "+i+"""<html><form method=post action=./log_staff.py><input type=submit value=Back></html>"""
    for i in flall:            
           zf.write(data.dpath+"/"+i, arcname=i)
    		

    fp=open(data.path+"/project_data/autoclick.html")
    fp=fp.read()   
    return fp
