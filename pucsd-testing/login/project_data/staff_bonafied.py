from config_path import data
import MySQLdb
import time;
from mod_python import Session
from config_path import data
import student
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
         cursor.execute(ss2,(Rollno,'APBN'))
         valq=cursor.fetchall()
               
         statess=valq[len(valq)-1]
         
    
         
         
         if statess==('ApplicationSubmitted', 'RequestArrivedInOffice') and flag==0:
                 flag=1;
        	 ss2="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s);"""
         	 cursor.execute(ss2,(sname,ip,"APBN,RequestArrivedInOffice,ApplicationModification,"+str(Rollno)+",Bonafide Certificate,apply for Bonafide Certificate"))
         	 db.commit()       
         
         
         if statess==('RequestArrivedInOffice', 'ApplicationModification') or flag==1 or statess==('ApplicationRejectedByOffice', 'ApplicationModification'):

        	 dd="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s);"""
         	 cursor.execute(dd,(sname,ip,"APBN,ApplicationModification,ModificationSuccessfully,"+str(Rollno)+",Bonafide Certificate,apply for Bonafide Certificate"))
         	 db.commit()
         fp=open(data.path+"/project_data/autoclick3.html")
         fp=fp.read()   
         return fp
def index(req):
         info=req.form;
         refn=info['dossss']
         dat=info['date']
         purp1=info['purp']
         Rollno=info['rln']
         fp=open(data.path+"/project_data/staff_bonafied.html");
         
         fp=fp.read();
         doc='';
         db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="applicationProcess")

         cursor = db.cursor()
        
              

         
	 ss="""select * from  studentDetailsDomain where rollNumber=%s;"""%(Rollno)
    	 cursor.execute(ss)
       	 val=cursor.fetchall()
         
         y="""select year from courseSemesterDomain where courseId = (select courseId from studentDetailsDomain where rollNumber=%s) and semId = (select semId from studentDetailsDomain where rollNumber=%s);"""
         cursor.execute(y,(Rollno,Rollno))
         val1=cursor.fetchall()
         yy= map(lambda x:x[0],val1)
         d=time.strftime("%d/%m/%Y")
         year=int(d.split('/')[2])
         pe="""select applicationPurpose from applicationForm where appId='APBN' and rollnumber=%s;"""%(Rollno)
         cursor.execute(pe)
         val23=cursor.fetchall()
         
         per= map(lambda x:x[0],val23)
         
         if(len(purp1)!=0):
            ss= """update applicationProcess.applicationForm set applicationPurpose=%s where appId="APBN" and rollnumber=%s;"""
            cursor.execute(ss,(purp1,Rollno)) 
            db.commit()
            p=purp1
         else:
             p=per[0]
         a=int(refn)
         
         ss3="""select gender from  studentDetailsDomain where rollNumber=%s;"""%(Rollno)
    	 cursor.execute(ss3)
       	 val3=cursor.fetchall()
         g = map(lambda x:x[0],val3)         
         if (g[0]=='m'):
             gen='Mr.'
             hh="his"
         else:
             gen='Miss.'
             hh="her"
         ss= """select * from applicationProcess.applicationFormForStaff where rollNumber=%s and appId='APBN';"""%(Rollno)
         cursor.execute(ss)
         valu=cursor.fetchall(); 
         db.commit()


         if(len(valu)==0):
             ss= """insert into applicationProcess.applicationFormForStaff values(%s,'APBN',%s,%s,0,0,0,'') ;"""
             cursor.execute(ss,(Rollno,p,a)) 
             db.commit()
         else:
		ss="""update applicationProcess.applicationFormForStaff set applicationPurpose=%s,refNo=%s where rollNumber=%s and appId='APBN'"""
                cursor.execute(ss,(p,a,Rollno))
                db.commit()     	
         dt="""select  dateOfBirth from studentDetailsDomain where rollNumber=%s;"""%(Rollno)
         cursor.execute(dt)
         valdt=cursor.fetchall()    
         bdt= map(lambda x:x[0],valdt)
         dt=str(bdt[0]).split('-')
         dt.reverse()
         dt='-'.join(dt)
         doc+=fp%(refn,dat,gen,val[0][4]+" "+val[0][5]+" "+val[0][6],int(val[0][0]),val[0][1],yy[0],year,year+1,hh,p,val[0][12],val[0][13],val[0][14],dt);

        



         doc+="""<html><head><body><form value="form" action="staff_bonafied.py/submit_success" method="post"><input type=\"hidden\" name=\"rol\" value=%s><input type=\"submit\" value=\"Submit\"></form><span style="margin-left:0.5em;"></span><form value="form" action=\"refno.py\"><input type=\"hidden\" name=\"rono\" value=%s><input type=\"hidden\" name=\"docm\" value=\"APBN\"><input type=\"submit\"  value=\"Edit\"></form><span style="margin-left:0.5em;"></span><form value=\"form\" action=\"reject.py\" method=\"post\"><input type=hidden name=\"rono\" value=%s><input type=hidden name=\"docm\" value=\"APBN\"><input type=\"submit\" value=\"REJECT\"></form></body></head></html>"""%(Rollno,Rollno,Rollno)   
         return doc






