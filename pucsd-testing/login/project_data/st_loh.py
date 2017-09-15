import MySQLdb  
from mod_python import Session
from config_path import data
def index(req):
    crpn=""

      
    session = Session.Session(req)
    try:
      rollno=session['rno']
    except:
        	return """<html>Session Expired<p><a href="https://pucsd.online/pucsd-testing/login/student-login.html"> LOGIN AGAIN</a></html>"""
  
    ip=session['ipaddr']
    session.save()
    session.cleanup()
    req.content_type = 'text/html'
    db = MySQLdb.connect(
    host="localhost",
    user=data.mysql_user,
    passwd=data.mysql_pswd,
    db="applicationProcess" )
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    
    q="""select fname,mname,lname from applicationProcess.studentDetailsDomain where rollNumber=%s;"""%(rollno)
    cursor.execute(q);
    nm=cursor.fetchall()
    if len(nm)==0:
       return """access denied!!"""	
    nm=nm[0]
    nm=' '.join(nm);
    
    req.write("<a align=\"right\" href=\"https://pucsd.online\">HOME<p></a><b><label>FOR STUDENT<p></label><label>Name:</b></label><label>"+nm+"</label>")


    req.write('<b><p><label>Rollno: %s\n</b></label>' % session['rno'])

    
    db = MySQLdb.connect(
    host="localhost",
    user=data.mysql_user,
    passwd=data.mysql_pswd,
    db="userInputDatabase" )
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # prepare a cursor object using cursor() method

    
    query="""DROP TABLE IF EXISTS StudentStatus;""";
    cursor.execute(query);
    table="""create table StudentStatus (RollNumber int,Documents varchar(50),Status varchar(50));""";
    cursor.execute(table);
   
    ss="""select appDesc from applicationProcess.applicationDomain """
    cursor.execute(ss);
    val=cursor.fetchall()
    appname=map(lambda x:x[0],val)
    
    
    ss="""select appId from applicationProcess.applicationDomain """
    cursor.execute(ss);
    val=cursor.fetchall()
    appid=map(lambda x:x[0],val)
        
    
    appl=['Bonafide Certificate','Fee Structure Certificate For Bank','International Bonafide Certificate','No Dues Certificate']

    
    for i in range(0,len(appid)):
       ss="""select params from applicationProcess.requestStateTransitions where userId=%s and params like %s"""
       cursor.execute(ss,(rollno,appid[i]+'%'));
       val=cursor.fetchall()
       
       if len(val)!=0:  
                stsfm=str(val[len(val)-1]).split(',')[1]
                ststo=str(val[len(val)-1]).split(',')[2]
               
                if ststo=='ApplicationSubmitted':
                             	
                         
                              ss="""select fromState,toState from applicationProcess.aux_studentAndState where rollNumber=%s and appId=%s   order by requestId desc limit 1 ;"""
                              cursor.execute(ss,(rollno,appid[i]));   
                              re=cursor.fetchall()
                              re=map(lambda x:x,re)
                              
                              if len(re)!=0:
                   
                                      ss="""insert into StudentStatus values(%s,%s,%s)"""
                                      cursor.execute(ss,(rollno,appname[i],re[0][1]))
                                      db.commit();
                                
                else:
                
                  ss="""insert into StudentStatus values(%s,%s,%s)"""
                  cursor.execute(ss,(rollno,appname[i],ststo));

       db.commit();
    
   
    
  
            
    cursor.execute(""" select * from StudentStatus;""");
    val=cursor.fetchall()
    names = list(map(lambda x: x[0], cursor.description))
    db.close() 
    fp1=open(data.path+"/project_data/json.txt","w");
    fp1.write("[");
    for i in range(0,len(val)):
        fp1.write("{");
    	for n in range(0,len(names)):
		fp1.write("\""+str(names[n])+"\":");
		if str(val[i][n]).isdigit():
                	fp1.write(str(val[i][n]));
		else:
	                fp1.write("\""+str(val[i][n])+"\"");
		
		if not n==len(names)-1:
		  fp1.write(",\n");
	if not i==len(val)-1:
        	fp1.write("},\n");
	else:
		fp1.write("}	\n");
		

    fp1.write("]");
   
    
    #crp=open(data.path+"/project_data/sample.html","r");
    #crpn+=crp.read()
    db = MySQLdb.connect(
    host="localhost",
    user=data.mysql_user,
    passwd=data.mysql_pswd,
    db="userInputDatabase" )
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    ss="""select output from outputResults;"""
    cursor.execute(ss)
    apsts=cursor.fetchall()
    req.content_type="text/html"
    
    db = MySQLdb.connect(
    host="localhost",
    user=data.mysql_user,
    passwd=data.mysql_pswd,
    db="userInputDatabase" )
    db.close()
    




            


    ss=""" select rollNumber from applicationProcess.internationalStudentInformationDomain;"""
    cursor.execute(ss)
    rnoarray=cursor.fetchall()
    rno=map(lambda x:x[0],rnoarray)
    
    if str(rollno)in rno:
            fp=open(data.path+"/project_data/NewAppInter.html","r")
            crpn+=fp.read()
            
    else:
            fp=open(data.path+"/project_data/Newapplication.html","r")
            crpn+=fp.read()
     
    crpn2=open(data.path+"/project_data/student.html","r");
    crpn+=crpn2.read()

    for i in names:
		crpn+=" <label style=\"padding-left:40px;\">%s<label>"%(i)
    crpn+="<br>"
    for i in names:
	crpn+="<input ng-model=\"ch.%s\" style=\"width:120px;\">"%(i) 
    crpn+="<table border=1>"
    
    for i in names:
      crpn+="<th style=\"width:80px;\">%s </th>"%(i)    
    crpn+="<tr ng-repeat=\"chrp in chiarperson|filter:ch|filter:statuspa|filter:fname\">"
    
    lnt=len(names);
    
                         
    for n in range(0,len(names)):
                               	 crpn+="<td>{{chrp.%s}}</td>"%(names[n]);
                                 if names[n]=="Status":
                                   crpn+="<td ng-if=\"chrp.Status==\'ApplicationFormFilled\' && chrp.Documents==\'Bonafide Certificate\'\"></form><form value=\"form\" action=\"read_pur.py\" method=\"post\"><input type=submit value=Edit></form><form value=\"form\" action=\"st_loh.py/print_Application_stud\" method=\"post\"><input type=submit value=Submit><input type=hidden name=\"ff\" value=\"0\"></form><form value=\"form\" action=\"./delete.py\" method=\"post\"><input type=\"submit\" value=\"Delete\"><input type=\"hidden\" name=\"appid\" value=\"APBN\"></form></td>"
                                   
                                   crpn+="<td ng-if=\"chrp.Status==\'ApplicationFormFilled\' && chrp.Documents==\'Fee Structure Certificate For Bank\'\"></form><form value=\"form\" action=\"read_bank.py\" method=\"post\"><input type=submit value=Edit></form><form value=\"form\" action=\"st_loh.py/print_Application_stud\" method=\"post\"><input type=submit value=Submit><input type=hidden name=\"ff\" value=\"2\"></form><form value=\"form\" action=\"./delete.py\" method=\"post\"><input type=\"submit\" value=\"Delete\"><input type=\"hidden\" name=\"appid\" value=\"APFS\"></form></td>" 
                                   crpn+="<td ng-if=\"chrp.Status==\'ApplicationFormFilled\' && chrp.Documents==\'No Dues Certificate\'\"><form value=\"form\" action=\"st_loh.py/print_Application_stud\" method=\"post\"><input type=submit value=Submit><input type=hidden name=\"ff\" value=\"1\"></form><form value=\"form\" action=\"./delete.py\" method=\"post\"><input type=\"submit\" value=\"Delete\"><input type=\"hidden\" name=\"appid\" value=\"APND\"></form></td>"
                                   crpn+="<td ng-if=\"chrp.Status==\'ApplicationFormFilled\' && chrp.Documents==\'International Bonafide Certificate\'\"><form value=\"form\" action=\"st_loh.py/print_Application_stud\" method=\"post\"><input type=submit value=Submit><input type=hidden name=\"ff\" value=\"3\"></form><form value=\"form\" action=\"./delete.py\" method=\"post\"><input type=\"submit\" value=\"Delete\"><input type=\"hidden\" name=\"appid\" value=\"APIB\"></form></td>"
                                   
                                   crpn+="<td ng-if=\"chrp.Status==\'ApplicationFormPartiallyFilled\' && chrp.Documents==\'Bonafide Certificate\'\"><form value=\"form\" action=\"read_pur.py\" method=\"post\"><input type=submit value=Edit></form><form value=\"form\" action=\"./delete.py\" method=\"post\"><input type=\"submit\" value=\"Delete\"><input type=\"hidden\" name=\"appid\" value=\"APBN\"></form></td>"
                                   
                                   crpn+="<td ng-if=\"chrp.Status==\'ApplicationFormPartiallyFilled\' && chrp.Documents==\'Fee Structure Certificate For Bank\'\"><form value=\"form\" action=\"read_bank.py\" method=\"post\"><input type=submit value=Edit></form><form value=\"form\" action=\"./delete.py\" method=\"post\"><input type=\"submit\" value=\"Delete\"><input type=\"hidden\" name=\"appid\" value=\"APFS\"></form></td>"
                                   return """<html>%s</html>"""%(crpn)
                                  
def print_Application_stud(req):
           
           session = Session.Session(req);
           Rollno=session['rno']
           ip=session['ipaddr']
           session.save()
           session.cleanup()
           tabid="ApplicationRequests"
           db = MySQLdb.connect(
    	   host="localhost",
    	   user=data.mysql_user,
    	   passwd=data.mysql_pswd,
    	
           db="userInputDatabase" )
   	   #prepare a cursor object using cursor() method
    	   cursor = db.cursor()
           info=req.form
           ff=int(info['ff'])
          
           arrayid=["APBN,ApplicationFormFilled,ApplicationSubmitted,Bonafide Certificate,apply for Bonafide Certificate","APND,ApplicationFormFilled,ApplicationSubmitted,No Dues Certificate,apply for No Dues Certificate"
,"APFS,ApplicationFormFilled,ApplicationSubmitted,Fee Structure Certificate For Bank,apply for Fee Structure Certificate For Bank","APIB,ApplicationFormFilled,ApplicationSubmitted,International Bonafide Certificate,apply for International Bonafide Certificate","APBN,ApplicationFormFilled,ApplicationSubmitted,Bonafide Certificate,apply for Bonafide Certificate"]
           
           psid=arrayid[ff]
           appid=psid.split(',')[0]
           aplydc=psid.split(',');
           aplydc=aplydc[3:]
           	
           ss="""select fromState,toState from applicationProcess.requestStateTransitions where userId=%s and params like %s;"""
           cursor.execute(ss,(Rollno,appid+'%'))
           val=cursor.fetchall()
           states=val[len(val)-1]
          
           if states==('ApplicationFormFilled','ApplicationFormPartiallyFilled'):
           	 flg=1
	  	 ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,%s);"""

                 cursor.execute(ss,(Rollno,tabid,iplog,appid+",ApplicationFormFilled,ApplicationFormFilled,"+aplydc[0]))
         	 db.commit();




           ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,%s);"""
           cursor.execute(ss,(Rollno,tabid,ip,psid))
       	   db.commit();
           
           
           fp=open(data.path+"/project_data/autoclick4.html")
           fp=fp.read()   
           return fp

