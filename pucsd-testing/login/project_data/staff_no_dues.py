import MySQLdb
from subprocess import call
from config_path import data
from mod_python import Session

def submit_success(req):

         flag=0;   
         info=req.form
         session = Session.Session(req);
         
         try:
            sname=session['sno'];
         except:
           return """<html>Session Expired<p><a href="https://pucsd.online/pucsd-testing/login/staff-login.html"> LOGIN AGAIN</a></html>"""

         ip=session['ipaddr']
         session.save()
         session.cleanup()
         db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="userInputDatabase")

         cursor = db.cursor()
         Rollno=info['rol']
         
         ss2="""select fromState,toState from applicationProcess.aux_studentAndState where rollNumber=%s and appId= %s;"""
         cursor.execute(ss2,(Rollno,'APND'))
         valq=cursor.fetchall()
              
         statess=valq[len(valq)-1]
         

         
         
         if statess==('ApplicationSubmitted', 'RequestArrivedInOffice') and flag==0:
                 flag=1;
         	 ss="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s);"""
                 cursor.execute(ss,(sname,ip,"APND,RequestArrivedInOffice,ApplicationModification,"+str(Rollno)+",No Dues Certificate,apply for No Dues Certificate"))
         	 db.commit()       
         
         

         if statess==('RequestArrivedInOffice', 'ApplicationModification') or flag==1 or statess==('ApplicationRejectedByOffice', 'ApplicationModification'):

         	dd="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s);"""
         	cursor.execute(dd,(sname,ip,"APND,ApplicationModification,ModificationSuccessfully,"+str(Rollno)+",No Dues Certificate,apply for No Dues Certificate"))
         	db.commit()
        
         fp=open(data.path+"/project_data/autoclick3.html")
         fp=fp.read()   
         return fp







def index(req):
         
         info=req.form
         db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="applicationProcess")
         refn=info['dossss']
         d=info['dd']
         cursor = db.cursor()
         Rollno=info['rln']   
         doc=''
         
         fp=open(data.path+"/project_data/staff_no_dues_docoment.html","r")
         fp=(fp.read());





         ss= """select * from applicationProcess.applicationFormForStaff where rollNumber=%s and appId='APND';"""%(Rollno)
         cursor.execute(ss)
         valu=cursor.fetchall(); 
         db.commit()


         a=refn;
         if(len(valu)==0):
             ss= """insert into applicationProcess.applicationFormForStaff values(%s,'APND','',%s,0,0,0,'') ;"""
             cursor.execute(ss,(Rollno,a)) 
             db.commit()
         else:
		ss="""update applicationProcess.applicationFormForStaff set refNo=%s where rollNumber=%s and appId='APND'"""
                cursor.execute(ss,(a,Rollno))
                db.commit()     	



         ss3="""select gender from  studentDetailsDomain where rollNumber=%s;"""%(Rollno)
    	 cursor.execute(ss3)
       	 val3=cursor.fetchall()
         g = map(lambda x:x[0],val3)         
         if (g[0]=='m'):
             gen='Mr.'
             hh="his"
             on_print_gender="him"
         else:
             gen='Miss.'
             hh="her"
	     on_print_gender="her"


         
    
         ss="""select * from  studentDetailsDomain where rollNumber=%s;;"""%(Rollno)
    	 cursor.execute(ss)
       	 val=cursor.fetchall()
         doc+=fp%(refn,d,gen,val[0][4]+" "+val[0][5]+" "+val[0][6]+" ",int(val[0][0]),val[0][1],on_print_gender,hh);
         doc+="""<html><head><body><form value="form" action="staff_no_dues.py/submit_success" method="post"><input type=\"hidden\" name=\"rol\" value=%s><input type=\"submit\" value=\"Submit\"></form><span style="margin-left:0.5em;"></span><form value="form" action=\"refno.py\"><input type=\"hidden\" name=\"rono\" value=%s><input type=\"hidden\" name=\"docm\" value=\"APND\"><input type=\"submit\"  value=\"Edit\"></form><span style="margin-left:0.5em;"></span><form value=\"form\" action=\"reject.py\" method=\"post\"><input type=hidden name=\"rono\" value=%s><input type=hidden name=\"docm\" value=\"APND\"><input type=\"submit\" value=\"REJECT\"></form></body></head></html>"""%(Rollno,Rollno,Rollno)
         return doc
