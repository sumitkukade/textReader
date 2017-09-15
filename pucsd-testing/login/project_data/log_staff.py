import MySQLdb
from subprocess import call
from config_path import data
from mod_python import Session

sname=0
def index(req):
    global sname
    session = Session.Session(req)
    session.load()
    session.cleanup()

    try:
       sname=session['sno'];
    except:
           return """<html>Session Expired<p><a href="https://pucsd.online/pucsd-testing/login/staff-login.html"> LOGIN AGAIN</a></html>"""
    ip=session['ipaddr']
   
    count=int(session['cnt'])+1;
    req.content_type="text/html"
    fo=open(data.path+"/project_data/nevtag.html","r");
    fo=fo.read()
    req.write(fo)
    req.write("<label>FOR STAFF<BR><br></label><b>USER: "+sname+"<b><br><p>")
    	
    crpn=""
    
    db = MySQLdb.connect(
    host="localhost",
    user=data.mysql_user,
    passwd=data.mysql_pswd,
    db="userInputDatabase" )
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    
    #table="""create table StudentStatusnew (RollNo int,Document varchar(50),Status varchar(50));""";
    #cursor.execute(table);
    
    ss="""select appDesc from applicationProcess.applicationDomain """
    cursor.execute(ss);
    val=cursor.fetchall()
    appname=map(lambda x:x[0],val) 

   

    
    cursor.execute("""select  appId  from  applicationProcess.applicationDomain ;""");   
    appid=cursor.fetchall()
    appid=map(lambda x:x[0],appid)
   

     
       
    cursor.execute("""select  userId,remark from  applicationProcess.requestStateTransitions where toState= 'ApplicationSubmitted';""");   
    val=cursor.fetchall()
    
    val=map(lambda x:x,val)
    newA=val
    
    
    result=[]
    appl=['Bonafide Certificate','Fee Structure Certificate For Bank','International Bonafide Certificate','No Dues Certificate']
    
   
    arrayid=["Bonafide Certificate,apply for Bonafide Certificate","Fee Structure Certificate For Bank,apply for Fee Structure Certificate For Bank","International Bonafide Certificate,apply for International Bonafide Certificate","No Dues Certificate,apply for No Dues Certificate"]

    cursor.execute("""select  userId,remark from  applicationProcess.requestStateTransitions where toState= 'RequestArrivedInOffice';""");   
    rval=cursor.fetchall()
    rval=map(lambda x:x,rval)
    
    	
    
    	
    for i in range(0,len(newA)):
      
      ss="""select  * from  applicationProcess.requestStateTransitions where userId=%s and remark=%s order by requestId desc limit 1 ;"""
      cursor.execute(ss,(str(val[i][0]),str(val[i][1])));
      val1=cursor.fetchall()
      val1=map(lambda x:x,val1[0])
      result.append(val1)
    d=6;
    
    
    for i,j in val[(len(rval)):]:
             qr="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s",ApplicationSubmitted,RequestArrivedInOffice,"%s","%s);"""
             
             cursor.execute(qr,(sname,str(ip),appid[appl.index(j)],i,arrayid[appl.index(j)]));
             db.commit()
             
             q4 = """select msg from userInputDatabase.outputErrorMsgs where requestId = (select requestId from userInputDatabase.inputRequests where userId=%s  order by requestId desc limit 1);"""       
             
             cursor.execute(q4,(sname,))
             res = cursor.fetchall()
             if len(res)!=0:
             
         	return """</form><html>%s <form value="form" action="#" method="post"><input type=\"submit\"value=\"OK\"></form></html>"""%(res[0])
    
    
    query="""DROP TABLE IF EXISTS userInputDatabase.StudentStatusnew;""";
    cursor.execute(query);
    db.commit()

    table="""create table userInputDatabase.StudentStatusnew(RollNo int,Ref_No varchar(20), Document varchar(50),status varchar(50));""";
    cursor.execute(table);
       
    
    
    for i,j in newA:
      
      
      ss="""select toState from applicationProcess.aux_studentAndState where rollNumber=%s and appId=%s   order by requestId desc limit 1 ;"""

    
      cursor.execute(ss,(i,appid[appl.index(j)]));   
      re=cursor.fetchall()
      

      ss="""select refNo from applicationProcess.applicationFormForStaff where rollNumber=%s and appId=%s;"""


      cursor.execute(ss,(i,appid[appl.index(j)]));   
      rl=cursor.fetchall()
      rl=map(lambda x:x[0],rl)
      
      if len(rl)==0:
          rl=''
      else:
          rl=rl[0]

      
      if len(re)!=0:
       re=map(lambda x:x[0],re)
       ss="""insert into userInputDatabase.StudentStatusnew values(%s,%s,%s,%s)"""
       cursor.execute(ss,(i,"CSD/"+str(rl),j,re[0]))
       db.commit();
    
    
    fp1=open(data.path+"/project_data/json.txt","w");
    fp1.write("[");
    
    cursor.execute(""" select * from userInputDatabase.StudentStatusnew;""");
    val=cursor.fetchall()
    names = list(map(lambda x: x[0], cursor.description))  
    
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
    
     
    fp2=open(data.path+"/project_data/json1.txt","w");
    fp2.write("[");
    
    for n in range(0,len(names)):
                fp2.write("{");
                if n==len(names)-1:
                    fp2.write("count:0}");	
		else:	
		 fp2.write("count:0},");	

    fp2.write("]");
  

    crpn+="""</form><form method="post" action="search-data-in-table.py"><input type="submit" value="Rejected Student List"></form><hr>"""
 
    crp=open(data.path+"/project_data/sample.html","r");
    crpn+=crp.read()
    
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
    
    
    
    db = MySQLdb.connect(
    host="localhost",
    user=data.mysql_user,
    passwd=data.mysql_pswd,
    db="mysql" )
    db.close()



   
    #crpn+="</form><form method=post action=\"newprint.py\" ><input type=\'submit\' align=right value=\"Download zip\"></form>"
    #crpn+="<p>"
    
    for i in names:
	 
		crpn+="<label style=\"padding-left:40px;\">%s<label>"%(i)
    crpn+="<br>"
    for i in names:
	crpn+="<input ng-model=\"ch.%s\" style=\"width:120px;\">"%(i) 
    crpn+="<table border=1>"

    for i in names:
      crpn+="<th style=\"width:80px;\">%s</th>"%(i)    
    crpn+="<tr ng-repeat=\"chrp in chiarperson|filter:ch|filter:fname\">"
    lnt=len(names);
   
   
    ss=""

    ll	="""select Status from userInputDatabase.StudentStatusnew;"""
    cursor.execute(ll)
    aps=cursor.fetchall()
    aps=map(lambda x:x[0],aps);

    
 
    allre="""SELECT count(*) FROM  applicationProcess.studentApplicationQueue""";
    cursor.execute(allre)
    allre=cursor.fetchall();
    
    if allre[0][0]!=0:
       allre=allre[0][0]
    else:
         allre=1;
    #crpn+="<label>Check me to check both: <input type=\"checkbox\" ng-model=\"leader\"></label><br/>" 

    
    ss="""Select * from applicationProcess.studentApplicationQueue order by requestId  limit %s,1;"""%(str(count%allre))
    
    cursor.execute(ss);
    
    que=cursor.fetchall()
    
    qrl='';
    qid='';
    if len(que)!=0:
        que=que[0]
        qrl=que[1]
        qid=que[2]
    
    
    ss="""Select appDesc from applicationProcess.applicationDomain where appId='%s';"""%(str(qid));
    cursor.execute(ss);
    qdc=cursor.fetchall()
    if len(qdc)!=0:
        qdc=qdc[0][0]
    else:
        qdc=''
    for n in range(0,lnt):
      crpn+="<td>{{chrp.%s}}</td>"%(names[n]);
    

      cnt=1;
      
      if('status' in names[n]):
        enb=''      			
    	crpn+="<td ng-if=\"chrp.%s ==\'ApplicationRejectedByOffice\'\" ng-init=\"ststs2=[\'RequestFisnishedWithError\',\'ApplicationModification\']\">"%(names[n])                        
    	crpn+="</form><html><head><body><form value=\"form\" action=\"log_staff.py/okfun\" method=\"post\"> Remark<input type=\"text\" name=\"rmk\"> <input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}></lable><select   name=\"sopt\" ng-model=\"stats2\" name=''ng-options=\"op for op in ststs2\"></select>"
        
        fp=open(data.path+"/project_data/nn.html")
        crpn+=fp.read();
        crpn+="</td>"  





        crpn+="<td  ng-if=\"chrp.%s ==\'ApplicationSubmitted\'\" ng-init=\"ststs3=[\'RequestArrivedInOffice\']\">"%(names[n])                        
    	crpn+="</form><html><head><body><form value=\"form\" action=\"log_staff.py/okfun\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}></lable><select  name=\"sopt\" ng-model=\"stats3\" name=''ng-options=\"op for op in ststs3\"> </select>"
        
        fp=open(data.path+"/project_data/nn.html")
        crpn+=fp.read();
        crpn+="</td>"  




            
        crpn+="<td ng-if=\"chrp.%s ==\'FormPrinted\'\" ng-init=\"ststs4=[\'FormSigned\',\'ApplicationRejectedByOffice \']\" ng-init=\"aa=1\">"%(names[n])                        
    	crpn+="</form><html><head><body><form value=\"form\" action=\"log_staff.py/okfun\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}></lable><select %s name=\"sopt\" ng-model=\"stats4\" name=''ng-options=\"op for op in ststs4\"> </select>"%(enb)
        
        fp=open(data.path+"/project_data/nn.html")
        crpn+=fp.read();
        crpn+="</td><div>" 
        
        

        crpn+="<td ng-if=\"chrp.%s ==\'ApplicationModification\'\" ng-init=\"ststs12=[\'ApplicationRejectedByOffice\',\'ModificationSuccessfully\']\">"%(names[n])                        
    	crpn+="</form><html><head><body><form value=\"form\" action=\"log_staff.py/okfun\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}></lable><select  name=\"sopt\" ng-model=\"stats12\" name=''ng-options=\"op for op in ststs12\"> </select>"
        fp=open(data.path+"/project_data/nn.html")

        crpn+=fp.read();
        crpn+="<form value=\"form\" action=\"refno.py\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}><br><input type=submit value=EDIT></form></td>"  





        
      
        crpn+="<td ng-if=\"chrp.%s ==\'FormSigned\'\" ng-init=\"ststs5=[\'SignedFormArrivedInOffice \',\'ApplicationRejectedByOffice\']\">"%(names[n])                        
    	crpn+="</form><html><head><body><form value=\"form\" action=\"log_staff.py/okfun\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}></lable><select  name=\"sopt\" ng-model=\"stats5\" name=''ng-options=\"op for op in ststs5\"> </select>"
        
        fp=open(data.path+"/project_data/nn.html")
        crpn+=fp.read();
        crpn+="</td>"  
        

        


        crpn+="<td ng-if=\"chrp.%s ==\'CertificateCollectedByStudent\'\" ng-init=\"ststs6=[\'RequestFinishedSuccessfully\']\">"%(names[n])                        
    	crpn+="</form><html><head><body><form value=\"form\" action=\"log_staff.py/okfun\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}></lable><select  name=\"sopt\" ng-model=\"stats6\" name=''ng-options=\"op for op in ststs6\"></select>"
        
        fp=open(data.path+"/project_data/nn.html")
        crpn+=fp.read();
        crpn+="</td>"  
        



        crpn+="<td ng-if=\"chrp.%s ==\'RequestArrivedInOffice\'\" ng-init=\"ststs7=[\'ApplicationRejectedByOffice\']\">"%(names[n])                        
    	crpn+="</form><html><head><body><form value=\"form\" action=\"log_staff.py/okfun\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}></lable><select  %s name='sopt' ng-model=\"stats7\" ng-options=\"op for op in ststs7\">"%(enb)
        fp=open(data.path+"/project_data/nn.html")

        crpn+=fp.read();
        crpn+="<form value=\"form\" action=\"refno.py\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}><br><input type=submit value=EDIT></form></td>"  
        


        crpn+="<td ng-if=\"chrp.%s ==\'RequestFinishedSuccessfully\' || chrp.%s ==\'RequestFisnishedWithError\' \" ng-init=\"ststs8=[\'Finish \']\">"%(names[n],names[n])                        
    	crpn+="</form><html><head><body><form value=\"form\" action=\"log_staff.py/okfun\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}></lable><select name='sopt' value=\"Finish\"><option>Finish</option></select>"
        
        fp=open(data.path+"/project_data/nn.html")
        crpn+=fp.read();
        crpn+="</td>"  

        


        crpn+="<td ng-if=\"chrp.%s ==\'SignedFormArrivedInOffice\'\" ng-init=\"ststs9=[\' ApplicationRejectedByOffice \',\' CertificateCollectedByStudent\']\">"%(names[n])                        
    	crpn+="</form><html><head><body><form value=\"form\" action=\"log_staff.py/okfun\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}></lable><select  name=\"sopt\" ng-model=\"stats9\" name=''ng-options=\"op for op in ststs9\"> </select>"
        
        fp=open(data.path+"/project_data/nn.html")
        crpn+=fp.read();
        crpn+="</td>"  
        

        


        crpn+="<td ng-if=\"chrp.%s ==\'Start\' \" ng-init=\"ststs0=[\'  ApplicationInitiated \']\">"%(names[n])                        
    	crpn+="</form><html><head><body><form value=\"form\" action=\"log_staff.py/staff.py/okfun\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}></lable><select  name=\"sopt\" ng-model=\"stats0\" name=''ng-options=\"op for op in ststs0\"> </select>"
        
        fp=open(data.path+"/project_data/nn.html")
        crpn+=fp.read();
        crpn+="</td>"  
 

        crpn+="<td ng-if=\"chrp.%s ==\'ModificationSuccessfully\' \" ng-init=\"ststs10=[\'FormPrinted \']\">"%(names[n])
                        
    	crpn+="</form><html><head><body><form value=\"form\" action=\"log_staff.py/okfun\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}></lable><select  name=\"sopt\" value='FormPrinted'> <option>FormPrinted</option></select>"
        
        fp=open(data.path+"/project_data/nn.html")
        crpn+=fp.read();
        crpn+="<form value=\"form\" action=\"pdf.py\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}><input type=submit value=PRINT></form>"  

        crpn+="<form value=\"form\" action=\"refno.py\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}><br><input type=submit value=EDIT></form></td>"  

	
         
    #crpn+="<td>{{stats}}<td>"
     
    return """<html>%s</html>"""%(crpn)

def okfun(req):

   session = Session.Session(req)
   session.load()	
   sname=session['sno']
   ip=session['ipaddr']
   info = req.form
   info=req.form
   rolno=info['rono']
   
   docm=info['docm']
   stt=info['sopt']
   
   if len(stt)==0 or len(stt)==1:
           fp=open(data.path+"/project_data/autoclick3.html")
           fp=fp.read()   
           return fp
   db = MySQLdb.connect(
   host="localhost",
   user=data.mysql_user,
   passwd=data.mysql_pswd,
   db="userInputDatabase" )
   cursor = db.cursor()
   ss="""select  appId from applicationProcess.applicationDomain where appDesc='%s';"""%(docm)
   cursor.execute(ss)   
   val=cursor.fetchall()
   val=map(lambda x:x[0],val)
   
   ss="""select status  from StudentStatusnew where RollNo=%s and Document= %s;""";
   cursor.execute(ss,(rolno,docm))   
   sts=cursor.fetchall()
   
   sts=map(lambda x:x[0],sts)
     
   stt=stt.replace("string:","").strip()
   
   arrayid=["Bonafide Certificate,apply for Bonafide Certificate","Fee Structure Certificate For Bank,apply for Fee Structure Certificate For Bank","International Bonafide Certificate,apply for International Bonafide Certificate","No Dues Certificate,apply for No Dues Certificate"]
   for i in arrayid:
        if docm in i:
           if stt=='FormPrinted':

                '''if docm=='International Bonafide Certificate':
                    filename="""%s_International_bonafide.pdf"""%(rolno);
                elif docm=='Bonafide Certificate':
                    filename="""%s_BONAFIDE.pdf"""%(rolno)
                elif docm=='Fee Structure Certificate For Bank':
                     filename="""%s_FEES_STRUCTURE.pdf"""%(rolno);
                elif docm=='No Dues Certificate':
                     filename="""%s_NO_DUES.pdf"""%(rolno)
                     
		try:
	 		s1=open(data.dpath+'/'+filename,"r");
                except:
                	return """<html><b>FIRSTLY PRINT FORM</b> <form method=post action=../log_staff.py><input type=submit value=Back></html>""";
                
		s1=s1.read()'''
                
		db = MySQLdb.connect(
		host="localhost",
		user=data.mysql_user,
		passwd=data.mysql_pswd,
		db="userInputDatabase")
		cursor = db.cursor();


                
                ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s);"""
       
                cursor.execute(ss,(sname,ip,(val[0]+","+sts[0]+","+stt+","+rolno+","+i)))

                    

   
           elif sts[0]=='ApplicationModification' and stt=='ApplicationRejectedByOffice':

                          mds2="""%s,ApplicationModification,ApplicationRejectedByOffice,%s,%s);"""%(val[0],rolno,i);
                          sd2="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s);"""
                          cursor.execute(sd2,(sname,mds2))
                          db.commit()
  
           elif 'CertificateCollectedByStudent'==sts[0]:
                
                 
                 ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s);"""
                 cursor.execute(ss,(sname,ip,(val[0]+","+sts[0]+","+stt+','+rolno+','+i)));
           elif sts[0]=="ApplicationRejectedByOffice":
              remark=info['rmk'];
              ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s);"""
              nr=i.split(',');
              nr[0]=remark+',';
              nr=''.join(nr)
              
              cursor.execute(ss,(sname,ip,(val[0]+","+sts[0]+","+stt+','+rolno+','+nr)));
           elif 'ModificationSuccessfully'==stt:
                          mds="""%s,ApplicationModification,ModificationSuccessfully,%s,%s);"""%(val[0],rolno,i);
                          sd="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s);"""
                          cursor.execute(sd,(sname,mds))
                          db.commit()  
                
           else:    
             ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s);"""
       
             cursor.execute(ss,(sname,ip,(val[0]+","+sts[0]+","+stt+","+rolno+','+i)))
             
            
           ss="""update StudentStatusnew set status=%s where RollNo=%s and Document=%s;"""   
           cursor.execute(ss,(stt,rolno,docm));
           db.commit()
           session['cnt']=int(session['cnt'])+1
           session.save()

           fp=open(data.path+"/project_data/autoclick3.html")
           fp=fp.read()   
           return fp
