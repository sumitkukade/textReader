from config_path import data
import MySQLdb
import time;
import refno
from mod_python import Session
from config_path import data
import student
def index(req):
   session = Session.Session(req);
   try:
       sname=session['sno'];
   except:
           return """<html>Session Expired<p><a href="https://pucsd.online/pucsd-testing/login/staff-login.html"> LOGIN AGAIN</a></html>"""

   ip=session['ipaddr']
   session.save()
   session.cleanup() 
   info=req.form
   app=info['docm']
   Rollno=info['rono']
   db = MySQLdb.connect(
   host="localhost",
   user=data.mysql_user,
   passwd=data.mysql_pswd,
   db="userInputDatabase" )
   cursor = db.cursor()

   appid=["APBN","APFS","APIB","APND"]
   arrayid=["Bonafide Certificate,apply for Bonafide Certificate","Fee Structure Certificate For Bank,apply for Fee Structure Certificate For Bank","International Bonafide Certificate,apply for International Bonafide Certificate","No Dues Certificate,apply for No Dues Certificate"]
   
   ss="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s",RequestArrivedInOffice,ApplicationRejectedByOffice,"%s);"""
   cursor.execute(ss,(sname,ip,app,arrayid[appid.index(app)]))
   db.commit()
   fp=open(data.path+"/project_data/autoclick.html")
   fp=fp.read()   
   return fp
