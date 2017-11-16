from __future__ import unicode_literals
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
import MySQLdb,datetime

def news_val(request):
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
	return news

def admin_home(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	return render(request,'admin_page/admin_home.html',{})

def view_zone(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from zone""")
	result=cursor.fetchall()
	return render(request, 'admin_page/view_zone.html', {'zone_list':result})

def view_division(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from division""")
	result=cursor.fetchall()
	return render(request, 'admin_page/view_division.html', {'division_list':result})

def view_user(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from user""")
	result=cursor.fetchall()
	user=[]
	for x in result:
		lists=[]
		for y in range(len(x)) :
			if(y!=len(x)-1):
				lists.append(x[y])
		user.append(lists)
	result=user
	return render(request, 'admin_page/view_user.html', {'user_list':result})

def view_employee(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from employee""")
	result=cursor.fetchall()
	user=[]
	for x in result:
		lists=[]
		for y in range(len(x)) :
			if(y!=len(x)-2):
				lists.append(x[y])
		user.append(lists)
	db.close()
	return render(request, 'admin_page/view_employee.html', {'employee_list':user})

def view_complaint(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from complaint""")
	result=cursor.fetchall()
	return render(request, 'admin_page/view_complaint.html' , {'complaint_list':result})

def view_feedback(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from feedback""")
	result=cursor.fetchall()
	return render(request, 'admin_page/view_feedback.html', {'feedback_list':result})

def view_news(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from news""")
	result=cursor.fetchall()
	return render(request, 'admin_page/view_news.html', {'news_list':result})

def view_report(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from gar_collect""")
	result=cursor.fetchall()
	print result
	db.close()
	return render(request, 'admin_page/view_garbage.html', {'garbage_list':result})

def add_zone(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	return render(request,'admin_page/add_zone.html',{'message':''})

def add_zone_form(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	zone_id=int(request.GET.get("zone",None))
	name=request.GET.get("zname",None)
	area=float(request.GET.get("area",None))
	population=int(request.GET.get("pop",None))

	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from zone where zone_id=%d """%zone_id)
	
	if(cursor.fetchone()==None):
		query="""Insert into zone values(%d,"%s",%f,%d)"""%(zone_id,name,area,population)
		cursor.execute(query)
		try:
			db.commit()
			message="Succesfully Added Record!!"
		except:
			db.rollback()
			message="Error!! Could Not Add Record!!"
	else:
		message="Zone Id already exists"
	db.close()
	return render(request,'admin_page/add_zone.html',{'message':message})

def add_division(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	return render(request,'admin_page/add_division.html',{'message':''})

def add_division_form(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	div_id=int(request.GET.get("division",None))
	name=request.GET.get("dname",None)
	area=float(request.GET.get("area",None))
	n_can=int(request.GET.get("can",None))
	num=int(request.GET.get("num",None))
	zone=int(request.GET.get("zone",None))

	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from division where div_id=%d """%div_id)
	
	if(cursor.fetchone()==None):
		query="""Insert into division values(%d,"%s",%f,%d,%d,%d)"""%(int(div_id),str(name),float(area),int(num),int(n_can),int(zone) )
		print query
		cursor.execute(query)
		try:
			db.commit()
			message="Succesfully Added Record!!"
		except:
			db.rollback()
			message="Error!! Could Not Add Record!!"

	else:
		message="Division Id already exists"
	db.close()
	return render(request,'admin_page/add_division.html',{'message':message})

def add_employee(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	return render(request,'admin_page/add_employee.html',{'message':''})	

def add_employee_form(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	emp_id=int(request.POST.get("eid",None))
	name=request.POST.get("name",None)
	aadhar=int(request.POST.get("aadhar",None))
	designation=request.POST.get("designation", None)      
	clas=request.POST.get("class",None)
	phone=int(request.POST.get("phone",None))
	address=request.POST.get("address",None)
     	zone=int(request.POST.get("zid",None))
	division=int(request.POST.get("did",None))
	password=request.POST.get("password",None)
	email=request.POST.get("email",None)

	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from employee where emp_id=%d """%emp_id)
	
	if(cursor.fetchone()==None):
		query="""Insert into employee values(%d,"%s",%d,"%s","%s",%d,"%s",%d,%d,"%s","%s");"""%(emp_id,name,int(aadhar), designation, clas, phone, address,zone,division,password,email)
		print query
		cursor.execute(query)
		try:
			db.commit()
			message="Succesfully Added Record!!"
		except:
			db.rollback()
			message="Error!! Could Not Add Record!!"
	else:
		message="Employee Id already exists"
	db.close()
	return render(request,'admin_page/add_employee.html',{'message':message})

def add_news(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	return render(request,'admin_page/news.html',{})

def delete_employee(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	emp_id=request.GET.get("emp_id",None)
	return render(request,'admin_page/employee.html',{})

def update_zone(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	return render(request,'admin_page/update_zone.html',{'message':'Leave fields blank if value is to be not changed'})

def update_zone_form(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	zone_id=int(request.GET.get("zone",None))
	area=request.GET.get("area",None)
	population=request.GET.get("pop",None)

	db=MySQLdb.connect(user="root", host="localhost", passwd= "12345", db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from zone where zone_id=%d """%zone_id)
	
	if(cursor.fetchone()!=None):
		if(area!=''):
			query="""Update zone set area=%f where zone_id=%d"""%(float(area),zone_id)
			cursor.execute(query)
		if(population!=''):
			query="""Update zone set population=%d where zone_id=%d"""%(int(population),zone_id)
			cursor.execute(query)
		try:
			db.commit()
			message="Succesfully Updated Record!!"
		except:
			db.rollback()
			message="Error!!Could Not Update Record!!"
	else:
		message="Zone Id doesn't exists"
	db.close()
	return render(request,'admin_page/update_zone.html',{'message':message})

def update_division(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	return render(request,'admin_page/update_division.html',{'message':''})

def update_division_form(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	div_id=request.GET.get("division",None)
	area=request.GET.get("area",None)
	n_can=request.GET.get("can",None)
	num=request.GET.get("num",None)

	if(div_id==''):
		return render(request,'admin_page/update_division.html',{'message':'Enter Division ID to update!'})
	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from division where div_id=%d """%(int(div_id)))
	
	if(cursor.fetchone()!=None):
		print "EXIT"
		if(area!=''):
			query="""Update division set area=%f where div_id=%d"""%(float(area),int(div_id))
			cursor.execute(query)
		if(n_can!=''):
			query="""Update division set num_cans=%d where div_id=%d"""%(int(n_can),int(div_id))
			print query
			cursor.execute(query)
		if(num!=''):
			query="""Update division set num_dump=%d where div_id=%d"""%(int(num),int(div_id))
			cursor.execute(query)
		try:
			db.commit()
			message="Succesfully Updated Record!!"
		except:
			db.rollback()
			message="Error!!Could Not Update Record!!"

	else:
		message="Division Id doesn't exists"
	db.close()
	return render(request,'admin_page/update_division.html',{'message':message})

def update_employee(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	return render(request,'admin_page/update_employee.html',{'message':''})	

def update_employee_form(request):
	if(request.session['type']!='admin'):
		news=news_val(request)
		return render(request,'info/home.html',{'site':'Home','news':news})
	emp_id=int(request.POST.get("eid",None))
	designation=request.POST.get("designation", None)      
	clas=request.POST.get("class",None)
	phone=int(request.POST.get("phone",None))
	address=request.POST.get("address",None)
     	zone=int(request.POST.get("zid",None))
	division=int(request.POST.get("did",None))
	password=request.POST.get("password",None)

	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from employee where emp_id=%d """%emp_id)
	
	if(cursor.fetchone()==None):
		query="""Insert into employee values(%d,"%s",%d,"%s","%s",%d,"%s",%d,%d,"%s","%s");"""%(emp_id,name,int(aadhar), designation, clas, phone, address,zone,division,password,email)
		print query
		cursor.execute(query)
		try:
			db.commit()
			message="Succesfully Added Record!!"
		except:
			db.rollback()
			message="Error!! Could Not Add Record!!"
	else:
		message="Employee Id already exists"
	db.close()
	return render(request,'admin_page/update_employee.html',{'message':message})

def admin_login(request):
	return render(request, 'admin_page/login.html', {'message':'','site':'Admin Login'})

def admin_login_fill(request):
	mail=request.POST.get("mail",None)
	password=request.POST.get("password",None)

	db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
	cursor=db.cursor()
	cursor.execute("""Select * from admin where username=%s and password=%s """,(mail,password))
	result=cursor.fetchone()

	if(result!=None):
		request.session['user']=mail
		request.session['password']=password
		request.session['type']='admin'
		db.close()
		return render(request, 'admin_page/admin_home.html', {})
	else:
	    db.close()
	    message="Username or Password is Incorrect"
	    return render(request, 'admin_page/login.html', {'message':message})

