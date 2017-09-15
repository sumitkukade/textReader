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
    ss="""select rollnumber from applicationProcess.studentApplicationQueue where rollnumber=%s and appId=%s;"""
    cursor.execute(ss,(Rollno,'APFS'))
    val=cursor.fetchall()
    rollno= map(lambda x:x[0],val)
    
    if len(rollno)==0:
                rollno=0
    elif  rollno[0]==Rollno:
         tabid="ApplicationRequests"
         ss="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params)    values (NOW(),"insert",%s,%s,%s,"APND,start,ApplicationInitiated,No Dues Certificate,apply for No Dues Certificate");"""

         cursor.execute(ss,(Rollno,tabid,ip))
         db.commit();

  
       	 
         q4 = """select msg from userInputDatabase.outputErrorMsgs where requestId = (select requestId from userInputDatabase.inputRequests where userId=%s  order by requestId desc limit 1);"""
         cursor.execute(q4,(Rollno,))
         res = cursor.fetchall()
             
         return """</form><html>%s <form value="form" action="./st_loh.py" method="post"><input type=\"submit\"value=\"OK\"></form></html>"""%(res[0])

    fp=open(data.path+"/project_data/bank_addr.html","r")
    fp=fp.read()
    
    return fp
