from config_path import data
from mod_python import Session
from config_path import data
import MySQLdb
import time;
import refno
from mod_python import Session
from config_path import data
import student
def addr_split(nn):
               cnt=0
               cntt=0
          
               nn=list(nn)
               for i in range(0,len(nn)):
                   if nn[i]==',':
                        nn[i]='</br>';
                        cntt=1
                   elif nn[i]==' ':
                       cntt+=1;
                       if cntt%3==0:
                           nn[i]='</br>';


               return nn;
def index(req):
         fp=open(data.path+"/project_data/pdf.html","r");
         fp=fp.read()
         info=req.form
         Rollno=info['rono']
         docm=info['docm']
         


         doc="";
         db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="applicationProcess")

         cursor = db.cursor()
         ss="""select  appId from applicationProcess.applicationDomain where appDesc='%s';"""%(docm)
         cursor.execute(ss)   
         val22=cursor.fetchall()
         app=map(lambda x:x[0],val22)[0]

         ss= """select refNo from applicationProcess.applicationFormForStaff where rollNumber=%s and appId=%s;"""
         cursor.execute(ss,(Rollno,app))
         refn=cursor.fetchall(); 
         refn= map(lambda x:x[0],refn)[0]
         d=time.strftime("%d/%m/%Y")
         if app=='APBN':         

         
	 	ss="""select * from  studentDetailsDomain where rollNumber=%s;"""%(Rollno)
    	 	cursor.execute(ss)
       	 	val=cursor.fetchall()
         
         	y="""select year from courseSemesterDomain where courseId = (select courseId from studentDetailsDomain where rollNumber=%s) and semId = (select semId from studentDetailsDomain where rollNumber=%s);"""
         	cursor.execute(y,(Rollno,Rollno))
         	val1=cursor.fetchall()
         	yy= map(lambda x:x[0],val1)
         	
         	year=int(d.split('/')[2])

         	p="""select applicationPurpose from applicationForm where appId=%s and rollnumber=%s;"""
         	cursor.execute(p,(app,Rollno))
         	val2=cursor.fetchall()
         	purpose= map(lambda x:x[0],val2)[0]
          

         
         	ss= """select * from applicationProcess.applicationFormForStaff where rollNumber=%s and appId=%s;"""
         	cursor.execute(ss,(Rollno,app))
         	valu=cursor.fetchall(); 
         

         	
         	dat=str(time.strftime("%d/%m/%Y"));         

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
                dt="""select  dateOfBirth from studentDetailsDomain where rollNumber=%s;"""%(Rollno)
         	cursor.execute(dt)
         	valdt=cursor.fetchall()    
       		bdt= map(lambda x:x[0],valdt)
        	dt=str(bdt[0]).split('-')
         	dt.reverse()
         	dt='-'.join(dt)

       		doc+=fp%(Rollno,refn,dat,gen,val[0][4]+" "+val[0][5]+" "+val[0][6],int(val[0][0]),val[0][1],yy[0],year,year+1,hh,purpose,val[0][12],val[0][13],val[0][14],dt);

        

  


                return doc

         if app=='APFS':
   
	         doc='';
	         db = MySQLdb.connect(
	    	 host="localhost",
	    	 user=data.mysql_user,
	    	 passwd=data.mysql_pswd,
	    	 db="applicationProcess")
	   	 # prepare a cursor object using cursor() method
	    	 cursor = db.cursor()
	         p="""select applicationPurpose from applicationProcess.applicationForm where appId='APFS' and rollnumber=%s;"""%(Rollno)
	         cursor.execute(p)
	         val2=cursor.fetchall()
	         add= map(lambda x:x[0],val2)
	          
	
	         fp=open(data.path+"/project_data/pdf1.html","r")
	         fp1=open(data.path+"/project_data/pdf2.html","r")
	         fp1=fp1.read()
	         fp=(fp.read());
         

	         p="""select applicationPurpose from applicationForm where appId='APFS' and rollnumber=%s;"""%(Rollno)
	         cursor.execute(p)
	         val2=cursor.fetchall()
	         purpose= map(lambda x:x[0],val2)[0]
	         
	
	         purpose=''.join(addr_split(purpose))


	         ss="""select * from applicationProcess.feesStructureForm where rollNumber=%s ;"""%(Rollno)
	    	 cursor.execute(ss)
	       	 val6=cursor.fetchall()
	         val=val6
                 

                 ss3="""select gender from  studentDetailsDomain where rollNumber=%s;"""%(Rollno)
    	         cursor.execute(ss3)
       	         val3=cursor.fetchall()
                 g = map(lambda x:x[0],val3)         
                 if (g[0]=='m'):
                    gen='Mr.'
                 else:
                    gen='Miss.'

                 
	    	 if val[0][4]=='MCA':  
	           doc+=fp1%(Rollno,refn,d,purpose,gen,val[0][1]+" "+val[0][2]+" "+val[0][3],val[0][4],val[0]	[6],val[1][6],val[2][6],val[3][6],val[4][6],val[5][6],val[0][7],val[1][7],val[2][7],val[3][7],val[4][7],val[5][7],val[0][8],val[1][8],val[2][8],val[3][8],val[4][8],val[5][8],val[0][9],val[1][9],val[2][9],val[3][9],val[4][9],val[5][9])
	         else:
			doc+=fp%(Rollno,refn,d,purpose,gen,val[0][1]+" "+val[0][2]+" "+val[0][3],val[0][4],val[0][6],val[1][6],val[2][6],val[3][6],val[0][7],val[1][7],val[2][7],val[3][7],val[0][8],val[1][8],val[2][8],val[3][8],val[0][9],val[1][9],val[2][9],val[3][9])

                 return doc
 
         if app=="APND":
 
                fp=open(data.path+"/project_data/pdf3.html","r")
                fp=(fp.read()); 
        	ss="""select * from  studentDetailsDomain where rollNumber=%s;;"""%(Rollno)
    	 	cursor.execute(ss)
       	 	val=cursor.fetchall()
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
         	doc+=fp%(Rollno,refn,d,gen,val[0][4]+" "+val[0][5]+" "+val[0][5]+" ",int(val[0][0]),val[0][1],on_print_gender,hh);
 
                return doc
         if app=="APIB":

	        doc='';
	                 
	         
		db = MySQLdb.connect(
 	   	host="localhost",
 	   	user=data.mysql_user,
 	   	passwd=data.mysql_pswd,
 	   	db="applicationProcess" )
 	        # prepare a cursor object using cursor() method
 	   	cursor = db.cursor()
 	            
 	         
 	        fp=open(data.path+"/project_data/pdf4.html","r")
 	        fp=(fp.read());
 	        
	
 	        
		ss = """select * from applicationProcess.studentDetailsDomain where rollNumber=%s ;"""%(Rollno)
 	   	cursor.execute(ss)
 	      	val=cursor.fetchall()
	
 	        ss1 = """select * from applicationProcess.internationalStudentInformationDomain where rollNumber=%s ;"""%(Rollno)
 	   	cursor.execute(ss1)
 	      	val1=cursor.fetchall()


 	        ss= """select * from applicationProcess.applicationFormForStaff where rollNumber=%s and appId='APIB';"""%(Rollno)
 	        cursor.execute(ss)
 	        valu=cursor.fetchall(); 
 	        db.commit()
                
	        rfno=valu[0][3];
                rpno=valu[0][4];
                unino=valu[0][5];
                svup=valu[0][6]
                rob=valu[0][7]
                
 	        d=time.strftime("%d/%m/%Y")
 	        doc+=fp%(Rollno,rfno,d,val[0][4]+" "+val[0][5]+" "+val[0][6],val[0][4]+" "+val[0][5]+" "+val[0][6],val1[0][1],val1[0][2],int(val[0][9]), rpno,unino,int(val1[0][4]),int(val1[0][7]),val1[0][5],val1[0][8],val1[0][6],val1[0][9],val1[0][10],svup,val1[0][3],val[0][1],val[0][1],d,rob,str(d));

 	   

 	        return doc
                             
                     
  
        















             




