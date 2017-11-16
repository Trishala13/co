import MySQLdb

db=MySQLdb.connect(user="root",host="localhost",passwd="12345",db="COC")
cursor=db.cursor()

cursor.execute("""create table if not exists zone(zone_id int primary key,name char(30),area decimal,population int);""")
db.commit()

cursor.execute("""create table if not exists division(div_id int primary key,name char(20),area decimal,num_dump int,num_cans int,zone int,foreign key (zone) references zone(zone_id));""")
db.commit()

cursor.execute("""create table if not exists employee(emp_id int primary key,name char(50),Aadhar_no int, designation char(40),class char(2),Phone int , address char(50),Z_id int ,D_id int,password char(20),foreign key (Z_id) references zone(zone_id),foreign key (D_id) references division(div_id));""")
db.commit()

cursor.execute("""create table if not exists supervise(supervisor_id int ,supervisee_id int,primary key(supervisor_id,supervisee_id));""")
db.commit()

cursor.execute("""create table if not exists user(aadhar_no int,fname char(20),lname char(20),email char(50) primary key,phone int, address char(50),password char(20));""")
db.commit()

cursor.execute("""create table if not exists complaint(id int primary key auto_increment,dept char(20),detail char(150),status char(30),usr_id char(50),incharge_id int,division_id int,foreign key (incharge_id) references employee(emp_id), foreign key (division_id) references division(div_id));""")
db.commit()

cursor.execute("""create table if not exists feedback(feed_id int primary key auto_increment,Satis_level int ,reason char(150),complaint_id int ,foreign key (complaint_id) references complaint(id));""")
db.commit()

cursor.execute("""create table if not exists contractor(c_id int primary key,name char(50),start_date date,end_date date,phone int,address int ,budget int);""")
db.commit()

cursor.execute("""create table if not exists vehicle(v_id int primary key,type char(30),capacity decimal,shift char(20),contractor int,foreign key (contractor) references contractor(c_id));""")
db.commit()

cursor.execute("""create table if not exists gar_collect(d_id int,v_id int,num_trip int,date_collect date,amount int,primary key(d_id,v_id,date_collect),foreign key (d_id) references division(div_id),foreign key (v_id) references vehicle(v_id));""")
db.commit()

cursor.execute("""create table if not exists news(id int primary key auto_increment,detail char(100),date_valid date default NULL);""")
db.commit()

cursor.execute("""create table if not exists admin(username char(40) primary key,eid int,password char(4),foreign key(eid) references employee(emp_id));""")
db.commit()

db.close()
