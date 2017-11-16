from __future__ import unicode_literals
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
import datetime,MySQLdb,random,string

val1=''
val2=''

def complaint_list_generate(complaint_list,mail):
	complaints=[]
	for x in complaint_list:
			x=list(x)
			x.remove(str(mail))
			complaints.append(x)
	date_today=datetime.date.today()
	complaint_list=[]
	for y in range(len(complaints)):
		x=complaints[y]
		month=x[-1].month
		year=x[-1].year
		if(x[3]=="Submitted" and (date_today.year-year>1 or date_today.month-month>1)):	
			hurl="""resubmit?id=%d"""%(x[0])
			x.append(hurl)
			x.append("Resubmit")	
		elif(x[3]=="Resolved"):
				hurl="""feedback?id=%d"""%(x[0])				
				x.append(hurl)
				x.append("Fill Feedback")
		else:
			x.append(0)
			x.append("No action")
		complaint_list.append(x)
	return complaint_list

def complaint_list_generate_official(complaint_list,mail):
	complaints=[]
	for x in complaint_list:
			x=list(x)
			x.remove(mail)
			complaints.append(x)
	date_today=datetime.date.today()
	complaint_list=[]
	for y in range(len(complaints)):
		x=complaints[y]
		month=x[-1].month
		year=x[-1].year
		if(x[3]=="Submitted"):
			hurl="""complaint_resolve?id=%d"""%(x[0])
			x.append(hurl)
			x.append("Resolved")	
		else:
			x.append(0)
			x.append("No action")
		complaint_list.append(x)
	return complaint_list

def set_val(types):
	global val1,val2
	if(types=='official'):
		val1=0
		val2=1
	elif(types=='user'):
		val1=1
		val2=0
	else:
		val1=0
		val2=0

def news_val(request):
	types=request.session['type']
	if(types=='admin'):
		request.session['type']=''
		request.session['password']=''
		request.session['user']=''
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	curr_date=datetime.date.today()
	cursor.execute("""Select detail,date_valid,types from news where date_valid>="%s" order by date_valid"""%(curr_date))
	result=cursor.fetchall()
	news=''
	for x in result:
		if(x[2]=='A'):
			news=news+str(x[0])+'.'
		elif(x[2]=='V'):
			news=news+str(x[0])+' on or before '+str(x[1])+'.'
	if(news==''):
		news='No Latest News'
	db.close()
	return news
	

def home(request):
	request.session['type']=''
	request.session['password']=''
	request.session['user']=''
	news=news_val(request)
	return render(request,'info/home.html',{'site':'Home','news':news})

def user_site(request):
	news=news_val(request)
	mail=request.session['user']
	password=request.session['password']
	types=request.session['type']
	if(mail=='' or types=="official"):
		request.session['user']=''
		request.session['password']=''
		request.session['type']=''
		return render(request,'users/sign-in.html',{'message':'','site':'Sign-In','news':news})

    	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from user where email=%s and password=%s """,(mail,password))
	result=cursor.fetchone()
	cursor.execute("""Select * from complaint where usr_id='%s' order by id"""%mail)
	complaint_list=cursor.fetchall()
	complaint_list=complaint_list_generate(complaint_list,mail)
	request.session['user']=mail
	request.session['password']=password
	request.session['type']='user'
	db.close()
	return render(request, 'users/user_site.html', {'complaint_list':complaint_list,'site':'User Site','val1':1,'val2':0,'news':news})

def sign_in(request):
	news=news_val(request)
	message=""
	request.session['user']=''
	request.session['password']=''
	request.session['type']=''
	return render(request, 'users/sign-in.html', {'message':message,'site':'Sign-In','val1':0,'val2':0,'news':news})

def sign_up(request):
	news=news_val(request)
    	request.session['user']=''
	request.session['password']=''
	request.session['type']=''    
	return render(request, 'users/sign-up.html', {'site':'Sign-Up','val1':0,'val2':0,'news':news})

def complaint(request):
	news=news_val(request)
	types=request.session['type']
	if(types=='' or types=='official'):
		request.session['user']=''
		request.session['password']=''
		request.session['type']=''
		return render(request,'users/sign-in.html',{'message':'You have to login/sign-up as User to register a complaint','site':'Sign-In','news':news})

	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from division """)
	result=cursor.fetchall()
	div_list=[]
	division=[]
	for x in result:
		division.append(str(x[0]))
		div_list.append(str(x[0])+'.'+x[1])
	cursor.execute("""Select * from zone """)
	result=cursor.fetchall()
	zone_list=[]
	zone=[]
	for x in result:
		zone.append(str(x[0]))
		zone_list.append(str(x[0])+'.'+x[1])
	db.close()
    	return render(request, 'users/complaint.html', {'site':'Complaint','val1':1,'val2':0,'division_list':zip(division,div_list), 'zone_list' : zip(zone,zone_list),'news':news})
 
def sign_up_form(request):
	news=news_val(request)
	firstname=str(request.POST.get("firstname",None))
	lastname=str(request.POST.get("lastname",None))
	aadhar=int(request.POST.get("aadhar",None))
	password=str(request.POST.get("password",None))
	mail=str(request.POST.get("email",None))
	phone=str(request.POST.get("phone",None))
	address=str(request.POST.get("address",None))

	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from user where email='%s' """%mail)

	if(cursor.fetchone()==None):
		cursor.execute("""Insert into user values(%s,%s,%s,%s,%s,%s,%s)""",(int(aadhar), firstname, lastname, mail, str(phone), address, password))
		request.session['user']=mail
		request.session['password']=password
		request.session['type']='user'
		try:
			db.commit()
			db.close()
			return render(request, 'users/user_site.html', {'site':'User Site','val1':1,'val2':0,'news':news})
		except:
			db.close()
			db.rollback()
			return render(request, 'users/sign-up.html', {'site':'Sign-Up','news':news})

	else:
		db.close()
		return render(request, 'users/sign-up.html', {'site':'Sign-Up','val1':0,'val2':0,'news':news})
	

def sign_in_form(request):
	news=news_val(request)
	mail=request.POST.get("mail",None)
	password=request.POST.get("password",None)

	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from user where email=%s and password=%s """,(mail,password))
	result=cursor.fetchone()

	if(result!=None):
		cursor.execute("""Select * from complaint where usr_id='%s' order by id"""%mail)
		complaint_list=cursor.fetchall()
		complaint_list=complaint_list_generate(complaint_list,mail)
		request.session['user']=mail
		request.session['password']=password
		request.session['type']='user'
		db.close()
		return render(request, 'users/user_site.html', {'complaint_list':complaint_list,'site':'User Site','val1':1,'val2':0, 'news':news})
	else:
	    db.close()
	    message="Username or Password is Incorrect"
	    return render(request, 'users/sign-in.html', {'message':message,'site':'Sign-In','val1':0,'val2':0,'news':news})

def complaint_form(request):
	news=news_val(request)
	mail=request.session['user']
	zone=request.POST.get("zone",None)
	division=request.POST.get("division",None)
	department=request.POST.get("department",None)
	details=request.POST.get("details",None)
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	if(department=="Health"):
		designation="Sanitary Inspector";
	elif(department=="Solid"):
		designation="Conservancy Inspector";
	else:
		designation="Assistant Engineer";
	print designation
	query="""Select e.emp_id from ((Select emp_id,0 from employee where Z_id=%d and D_id=%d and designation="%s" and emp_id not in (Select incharge_id as emp_id from complaint)) union (select incharge_id as emp_id,count(*) as "0" from complaint ,employee where emp_id= incharge_id and designation="%s" group by incharge_id)) as e order by "0" limit 1;"""%(int(zone),int(division),designation,designation)
	cursor.execute(query)
	result=cursor.fetchone()
	incharge_id=result[0]
	
	query="""Insert into complaint(id,dept,detail,status,usr_id,incharge_id,division_id) values(95,"%s","%s","Submitted","%s",%d,%d);"""%(department, details,mail, int(incharge_id), int(division))
	
	cursor.execute(query)
	try:
		db.commit()
		lists=[mail,]
		cursor.execute("""Select name,phone from employee where emp_id=%d""",int(incharge_id))
		result=cursor.fetchone()
		message="""Dear User,\nThis mail is to inform you that your complaint has been registered.The details regarding the complaint are:\nDepartment: %s\nDetails: %s\n Incharge Employee Name: %s\nIncharge Employee Contact:%s\nRegards\nThe Admin Team\nGreater Corporation Of Chennai"""%(department,details,result[0],result[1])
		send_mail('Complaint Registeration Details',message, settings.EMAIL_HOST_USER,lists,fail_silently=False,)

		cursor.execute("""Select email from employee where emp_id=%d""",int(incharge_id))
		result=cursor.fetchone()
		message="""Dear User,\nThis mail is to inform you that your complaint has been registered and you are requested to resolve the complaint at the earliest.The details regarding the complaint are:\nDepartment: %s\nDetails: %s\n Regards\nThe Admin Team\nGreater Corporation Of Chennai"""%(department,details)
		send_mail('Complaint Registeration Details',message, settings.EMAIL_HOST_USER,[result[0],],fail_silently=False,)

	except:
		db.rollback()
	cursor.execute("""Select * from division """)
	result=cursor.fetchall()
	div_list=[]
	division=[]
	for x in result:
		division.append(str(x[0]))
		div_list.append(str(x[0])+'.'+x[1])
	cursor.execute("""Select * from zone """)
	result=cursor.fetchall()
	zone_list=[]
	zone=[]
	for x in result:
		zone.append(str(x[0]))
		zone_list.append(str(x[0])+'.'+x[1])
	db.close()
    	return render(request, 'users/complaint.html', {'site':'Complaint','val1':1,'val2':0,'division_list':zip(division, div_list), 'zone_list':zip(zone,zone_list),'news':news})

def update(request):
	news=news_val(request)
	password=request.session['password']
	mail=request.session['user']
	passwd=request.POST.get("password",None)
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	if(password==passwd):
		cursor.execute("""Select * from user where email=%s and password=%s """,(mail,password))
		result=cursor.fetchone()
		aadhar=result[0]
		fname=result[1]
		lname=result[2]
		phone=result[4]
		address=result[5]
		db.close()
		return render(request,'users/update.html',{'aadhar':aadhar,'fname':fname,'lname':lname,'phone':phone, 'address':address, 'password': password,'mail':mail,'site':'Update Profile','val1':1,'val2':0,'news':news})
	else:
		cursor.execute("""Select * from complaint where usr_id='%s' order by id"""%mail)
		complaint_list=cursor.fetchall()
		complaints=[]
		for x in complaint_list:
			x=list(x)
			x.remove(str(mail))
			complaints.append(x)
		db.close()
		return render(request, 'users/user_site.html', {'complaint_list':complaints,'site':'User Site','val1':1,'val2':0,'news':news})

def update_fill(request):
	news=news_val(request)
	password=request.session['password']
	mail=request.session['user']
	passwd=request.POST.get("password",None)
	address=request.POST.get("address",None)
	phone=request.POST.get("phone",None)
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	if(address!=''):
		query="""Update user set address='%s' where password='%s' and email='%s'"""%(address,password, mail)
		cursor.execute(query)
	if(phone!=''):
		phone=int(phone)
		query="""Update user set phone='%d' where password='%s' and email='%s'"""%(phone, password, mail)
		cursor.execute(query)
	if(passwd!=''):
		query="""Update user set password='%s' where password='%s' and email='%s'"""%(passwd, password, mail)
		cursor.execute(query)
	cursor.execute("""Select * from complaint where usr_id='%s' order by id"""%mail)
	complaint_list=cursor.fetchall()	
	complaints=[]
	for x in complaint_list:
		x=list(x)
		x.remove(str(mail))
		complaints.append(x)
	try:
		db.commit()
		if(password==''):
			db.close()
			return render(request, 'users/user_site.html', {'complaint_list':complaints,'site':'User Site','val1':1,'val2':0, 'news':news})
		else:
			request.session['user']=''
			request.session['password']=''
			request.session['type']=''
			db.close()
			return render(request,'users/sign-in.html',{'message':'Password Changed!.Sign-In Again','site':'Sign-In', 'val1':0, 'val2':0,'news':news})
	except:
		db.rollback()
		return render(request, 'users/user_site.html', {'complaint_list':complaints,'site':'User Site','val1':1,'val2':0 ,'news':news})


def official_login(request):
	news=news_val(request)
	request.session['user']=''
	request.session['password']=''
	request.session['type']=''
    	return render(request, 'employee/official-login.html', {'site': 'Official Login','val1':0,'val2':0,'news':news})

def emp_site(request):
	news=news_val(request)
	emp_id=int(request.session['user'])
	password=request.session['password']
	types=request.session['type']
	if(emp_id=='' or types=="user"):
		request.session['user']=''
		request.session['password']=''
		request.session['type']=''
		return render(request,'employee/official-login.html', {'site': 'Official Login','news':news})

	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	query="""Select * from employee where emp_id=%d and password='%s' """%(int(emp_id),password)
	cursor.execute(query)
	result=cursor.fetchone()

	if(result!=None):
		cursor.execute("""Select * from complaint where incharge_id=%d"""%emp_id)
		complaint_list=cursor.fetchall()
		complaint_list=complaint_list_generate_official(complaint_list,emp_id)
		request.session['user']=emp_id
		request.session['password']=password
		request.session['type']='official'
		db.close()
		return render(request, 'employee/employee_site.html', {'complaint_list':complaint_list, 'site': 'Employee Site','val1':0,'val2':1,'news':news})
	else:
	    db.close()
	    message="Employee Id or Password No Longer Valid. Sign-In Again."
	    return render(request, 'employee/official-login.html', {'message':message,'site':'Official Log-In','val1':0,'val2':0,'news':news})

def official_login_form(request):
	news=news_val(request)
	emp_id=request.POST.get("empid",None)
	emp_id=int(emp_id)
	password=request.POST.get("password",None)
    	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	query="""Select * from employee where emp_id=%d and password='%s' """%(int(emp_id),password)
	cursor.execute(query)
	result=cursor.fetchone()

	if(result!=None):
		cursor.execute("""Select * from complaint where incharge_id=%d"""%emp_id)
		complaint_list=cursor.fetchall()
		complaint_list=complaint_list_generate_official(complaint_list,emp_id)
		request.session['user']=emp_id
		request.session['password']=password
		request.session['type']='official'
		db.close()
		return render(request, 'employee/employee_site.html', {'complaint_list':complaint_list,'site': 'Employee Site','val1':0,'val2':1,'news':news})
	else:
	    db.close()
	    message="Employee ID or Password is Incorrect"
	    return render(request, 'employee/official-login.html', {'message':message,'site':'Sign-In','val1':0,'val2':0 ,'news':news})

def zone(request):
	news=news_val(request)
	types=request.session['type']
	set_val(types)
	global val1,val2
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from zone """)
	result=cursor.fetchall()
	zone_list=[]
	zone=[]
	for x in result:
		zone.append(str(x[0]))
		zone_list.append(str(x[0])+'.'+x[1])
	db.close()
	return render(request, 'info/zone.html', {'zone_list':zip(zone,zone_list),'site':'Zone Details','val1':val1,'val2':val2 ,'news':news})

def zone_fill(request):
	news=news_val(request)
	types=request.session['type']
	set_val(types)
	global val1,val2
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	zone_id=request.GET.get("zone",None)
	zone_id=int(zone_id)
	query="""Select * from zone where zone_id=%d;"""%(zone_id)
	cursor.execute(query)
	x=cursor.fetchone()
	zone=str(x[0])
	zone_list=str(x[0])+'.'+x[1]
	area=str(x[2])
	population=str(x[3])
	zone_details=zip(zone,zone_list,area,population)
	cursor.execute("""Select * from zone """)
	result=cursor.fetchall()
	zone_list=[]
	zone=[]
	for x in result:
		zone.append(str(x[0]))
		zone_list.append(str(x[0])+'.'+x[1])
	db.close()
	return render(request, 'info/zone_fill.html', {'zone':zone_details,'zone_list':zip(zone,zone_list),'site':'Zone Details', 'val1':val1, 'val2':val2,'news':news})

def division(request):
	news=news_val(request)
	types=request.session['type']
	set_val(types)
	global val1,val2
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from division """)
	result=cursor.fetchall()
	div_list=[]
	division=[]
	for x in result:
		division.append(str(x[0]))
		div_list.append(str(x[0])+'.'+x[1])
	cursor.execute("""Select * from zone """)
	result=cursor.fetchall()
	zone_list=[]
	zone=[]
	for x in result:
		zone.append(str(x[0]))
		zone_list.append(str(x[0])+'.'+x[1])
	db.close()
	return render(request, 'info/division.html', {'division_list':zip(division, div_list),'zone_list':zip(zone,zone_list),'site':'Division Details', 'val1':val1, 'val2':val2,'news':news})

def division_fill(request):
	news=news_val(request)
	types=request.session['type']
	set_val(types)
	global val1,val2
	zone_id=int(request.GET.get("zone",None))
	division_id=int(request.GET.get("division",None))
	zone_id=int(zone_id)
	division_id=int(division_id)
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	query="""Select * from division where div_id=%d and zone=%d """%(division_id,zone_id)
	cursor.execute(query)
	x=cursor.fetchone()
	division=(str(x[0]))
	div_list=(str(x[0])+'.'+x[1])
	area=(str(x[2]))
	num_dump=(str(x[3]))
	num_cans=(str(x[4]))
	zone=(str(x[5]))
	cursor.execute("""Select * from division """)
	result=cursor.fetchall()
	div_list=[]
	division=[]
	for x in result:
		division.append(str(x[0]))
		div_list.append(str(x[0])+'.'+x[1])
	cursor.execute("""Select * from zone """)
	result=cursor.fetchall()
	zone_list=[]
	zone=[]
	for x in result:
		zone.append(str(x[0]))
		zone_list.append(str(x[0])+'.'+x[1])
	division_list=zip(division, div_list, area, num_dump, num_cans,zone )
	d=zip(division, div_list)
	z=zip(zone,zone_list)
	db.close()
	return render(request, 'info/division_fill.html', {'division':division_list,'division_list':d,'zone_list':z,'site':'Division Details','val1':val1,'val2':val2,'news':news})
  
def garbage(request):
	news=news_val(request)
	types=request.session['type']
	set_val(types)
	global val1,val2
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from division """)
	result=cursor.fetchall()
	div_list=[]
	division=[]
	for x in result:
		division.append(str(x[0]))
		div_list.append(str(x[0])+'.'+x[1])
	div=zip(division,div_list)

	cursor.execute("""Select distinct type from vehicle """)
	result=cursor.fetchall()
	vehicle=[]
	for x in result:
		vehicle.append(str(x[0]))
	db.close()
	return render(request,'info/garbage_Report.html',{'division_list':div,'vehicle_list':vehicle,'site':'Garbage Details', 'val1':val1, 'val2':val2,'news':news})

def garbage_fill(request):
	news=news_val(request)
	types=request.session['type']
	set_val(types)
	global val1,val2
	division=int(request.GET.get("division",None))
	start=request.GET.get("s_date",None)
	end=request.GET.get("e_date",None)
	vehicle=request.GET.get("vehicle",None)
	message=''
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	query="""Select g.d_id,g.v_id,g.num_trip,g.date_collect,g.amount from gar_collect g,vehicle v where g.v_id=v.v_id and v.type='%s' and g.d_id=%d and g.date_collect<='%s' and g.date_collect>='%s' """%(vehicle,division,end,start)
	cursor.execute(query)
	result=cursor.fetchall()
	db.close()
	return render(request,'info/garbage.html',{'garbage_list':result,'site':'Garbage Details' , 'val1':val1, 'val2':val2,'news':news})

def garbage_form(request):
	news=news_val(request)
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from division """)
	result=cursor.fetchall()
	div_list=[]
	division=[]
	for x in result:
		division.append(str(x[0]))
		div_list.append(str(x[0])+'.'+x[1])
	div=zip(division,div_list)

	cursor.execute("""Select distinct type from vehicle """)
	result=cursor.fetchall()
	vehicle=[]
	for x in result:
		vehicle.append(str(x[0]))
	db.close()
	return render(request,'employee/garbage_form.html',{'division_list':div,'vehicle_list':vehicle,'site':'Garbage Details', 'val1':0, 'val2':1 ,'news':news})

def garbage_entries(request):
	news=news_val(request)
	if(request.session['type']!='official'):
		return render(request,'employee/official-login.html',{'site':'Official Login','news':news})
	division=int(request.GET.get("division",None))
	dates=request.GET.get("s_date",None)
	num_trip=int(request.GET.get("num_trip",None))
	vehicle=request.GET.get("vehicle",None)
	amount=request.GET.get("amount",None)
	message=''
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	query="""Insert into gar_collect values(%d,%d,%d,'%s',%f)""" %(division,int(vehicle),num_trip,dates,float(amount))
	cursor.execute(query)
	try:
		db.commit()
	except:
		db.rollback()
	db.close()
	return render(request,'employee/employee_site.html',{'site': 'Employee Site','val1':0,'val2':1,'news':news})


def reset_passwrd(request):
	news=news_val(request)
	mail=request.GET.get("email",None)
	lists=[mail,]
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from user where email='%s';"""%(mail))
	result=cursor.fetchone()
	if(result==None):
		message="Invalid E-mail"
	else:
		message="Mail sent to Valid Id"
		passwrd=str(''.join(random.choice(string.ascii_uppercase + string.digits+string.ascii_lowercase) for x in range(10)))
		query="""Update user set password='%s' where email='%s';"""%(passwrd,mail)
		cursor.execute(query)
		db.commit()
		mail_message="""Dear User,\nYour Generated Password : %s.\nYou can change your password afterwards if you want.\nRegards,\nAdmin Team\nGreater Chennai Corporation"""%(passwrd)
		send_mail('Reset Password',mail_message, settings.EMAIL_HOST_USER,lists,fail_silently=False,)
	db.close()
	return render(request,'users/sign-in.html', {'message':message,'site':'Sign-In','val1':0,'val2':0,'news':news})


def feedback(request):
	news=news_val(request)
	cid=request.GET.get("id",None)
	request.session['cid']=cid
	return render(request,'users/feedback.html',{'val1':1,'val2':0,'news':news})

def feedback_form(request):
	news=news_val(request)
	cid=request.session['cid']
	mail=request.session['user']
	request.session['cid']=0
	email=request.GET.get("email",None)
	if(email!=mail):
		return render(request,'users/feedback.html',{'val1':0,'val2':0,'news':news})
	else:
		db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
		cursor=db.cursor()
		satis=request.POST.get("satisfaction",None)
		suggest=request.POST.get("suggest",None)
		cursor.execute("""Insert into feedback(Satis_level,reason,complaint_id) values(%s,%s,%d)""",(satis, suggest,int(cid)))
		cursor.execute("""Update complaint set Status="Feedback Filled" where id=%d"""%(int(cid)))
		db.commit()
		cursor.execute("""Select * from complaint where usr_id='%s' order by id"""%mail)
		complaint_list=cursor.fetchall()
		complaint_list=complaint_list_generate(complaint_list,mail)
		db.close()
		return render(request, 'users/user_site.html', {'complaint_list':complaint_list,'site':'User Site','val1':1, 'val2':0, 'news':news})

def resubmit(request):
	news=news_val(request)
	mail=request.session['user']
	lists=[mail,]
	cid=request.GET.get("id",None)
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	query="""Select incharge_id,dept,detail from complaint where id=%d"""%(int(cid))
	cursor.execute(query)
	result=cursor.fetchone()
	supervisee=result[0]
	department=result[1]
	details=result[2];
	query="""Select supervisor from supervise where supervisee=%d;"""%(int(supervisee))
	cursor.execute(query)
	result=cursor.fetchone()
	if(result==None):
		incharge_id=supervisee
	else:
		incharge_id=int(result[0])
	query="""Update complaint set incharge_id=%d where id=%d;"""%(int(incharge_id),int(cid))
	cursor.execute(query)
	db.commit()
	cursor.execute("""Select name,phone,designation from employee where emp_id=%d"""%int(incharge_id))
	result=cursor.fetchone()
	message="""Dear User,\nThis mail is to inform you that your complaint has been resubmitted to the supervisor of the previous incharge.We hope to resolve the inconvenience caused at the earliest.The details regarding the complaint are:\nDepartment: %s\nDetails: %s\n Incharge Employee Name: %s\n Incharge Designation : %s\nIncharge Employee Contact:%s\nRegards\nThe Admin Team\nGreater Corporation Of Chennai"""%(department,details,result[0],result[2],result[1])
	send_mail('Complaint Resubmission Details',message, settings.EMAIL_HOST_USER,[mail,],fail_silently=False,)
	cursor.execute("""Select name from employee where emp_id=%d"""%int(supervisee))
	result=cursor.fetchone()
	supervisee=result[0]
	cursor.execute("""Select email from employee where emp_id=%d"""%int(incharge_id))
	result=cursor.fetchone()
	message="""Dear User,\nThis mail is to inform you that your complaint has been resubmitted as it had not yet been resolved by your Supervisee:%s and you are requested to resolve the complaint at the earliest.The details regarding the complaint are:\nDepartment: %s\nDetails: %s\n Regards\nThe Admin Team\nGreater Corporation Of Chennai"""%(supervisee,department,details)
	send_mail('Complaint Registeration Details',message, settings.EMAIL_HOST_USER,[result[0],],fail_silently=False,)
	cursor.execute("""Select * from complaint where usr_id='%s' order by id"""%mail)
	complaint_list=cursor.fetchall()
	complaint_list=complaint_list_generate(complaint_list,mail)
	db.close()
	return render(request, 'users/user_site.html', {'complaint_list':complaint_list,'site':'User Site','val1':1,'val2':0,'news':news})

def resolve(request):
	news=news_val(request)
	cid=request.GET.get("id",None)
	emp_id=request.session['user']
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Update complaint set Status="Resolved" where id=%d"""%(int(cid)))
	db.commit()
	cursor.execute("""Select * from complaint where incharge_id=%d"""%emp_id)
	complaint_list=cursor.fetchall()
	complaint_list=complaint_list_generate_official(complaint_list,emp_id)
	db.close()
	return render(request, 'employee/employee_site.html', {'complaint_list':complaint_list, 'site': 'Employee Site ' ,'val1':0,'val2':1 , 'news':news})
	

def signout(request):
	news=news_val(request)
	types=request.session['type']
	request.session['user']=''
	request.session['password']=''	
	request.session['type']=''
	if(types=="official"):
	    	return render(request, 'employee/official-login.html', {'site': 'Official Login','val1':0,'val2':0,'news':news})
	else:
		return render(request,'users/sign-in.html',{'val1':0,'val2':0,'site':'User Login','news':news})

def delete_account(request):
	news=news_val(request)
	mail=request.session['user']
	if(mail==''):
		return render(request, 'users/sign-in.html', {'message':'','site':'Sign-In','val1':0,'val2':0,'news':news})
	request.session['user']=''
	request.session['password']=''	
	request.session['type']=''
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""delete from user where email='%s' """%mail)
	try:
		db.commit()
		message="Account Deleted"
	except:
		db.rollback()
		message="Error!! Account could not be deleted"
	db.close()	
	return render(request, 'users/sign-in.html', {'message':message,'site':'Sign-In','val1':0,'val2':0,'news':news})

