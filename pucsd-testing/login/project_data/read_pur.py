import MySQLdb
import datetime;
from mod_python import Session
from config_path import data
newflag=0
def index(req):
   
    session = Session.Session(req);
    global Rollno
    try:
            Rollno=session['rno']
    except:
            return """<html>Session Expired<p><a href="https://pucsd.online/pucsd-testing/login/student-login.html"> LOGIN AGAIN</a></html>"""

    ip=session['ipaddr']
    session.save()
    session.cleanup()
    flg=0
    db = MySQLdb.connect(
    host="localhost",
    user=data.mysql_user,
    passwd=data.mysql_pswd,
    db="userInputDatabase" )
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    tabid="ApplicationRequests"

    ss=""" select max(appcnt) from applicationProcess.studentApplicationCount where rollNumber=%s and appId=%s;"""
    cursor.execute(ss,(Rollno,'APBN'))
    count1=cursor.fetchall()
    count1= map(lambda x:x[0],count1);

    ss=""" select max(appcnt) from applicationProcess.studentApplicationCount where rollNumber=%s and appId=%s;"""
    cursor.execute(ss,(Rollno,'APBN'))
    count2=cursor.fetchall()
    count2= map(lambda x:x[0],count2);
    




    ss="""select rollnumber from applicationProcess.studentApplicationQueue where rollnumber=%s and appId=%s;"""
    cursor.execute(ss,(Rollno,'APBN'))
    val1=cursor.fetchall()
    rn= map(lambda x:x[0],val1)
    if len(rn)!=0:
         tabid="ApplicationRequests"
         
           
          
         ss="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APBN,start,ApplicationInitiated,Bonafide Certificate,apply for Bonafide Certificate");"""

         cursor.execute(ss,(Rollno,tabid,ip))
         db.commit();
         
         q4 = """select msg from userInputDatabase.outputErrorMsgs where requestId = (select requestId from userInputDatabase.inputRequests where userId=%s  order by requestId desc limit 1);"""
         cursor.execute(q4,(Rollno,))
         res = cursor.fetchall()
          
             
         return """</form><html>%s <form value="form" action="./st_loh.py" method="post"><input type=\"submit\"value=\"OK\"></form></html>"""%(res[0])
    fp=open(data.path+"/project_data/purpose.html","r")
    fp=fp.read()
    return fp


 
