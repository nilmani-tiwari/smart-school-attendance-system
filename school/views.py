from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from school.models import *
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import threading

from django.contrib.auth.decorators import login_required

from school.functions import *
import datetime
from json import dumps
import json
import requests

@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username').strip()
		password =request.POST.get('password').strip()

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')
			return redirect('home')

	context = {}
	return render(request, 'SchoolDesign/login.html', context)


def homepage(request):
    return render(request,'homepage.html')


def sachin(request):
    
    return render(request,'sachin.html')

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
	d={}
	today = datetime.date.today()
	try:
		school_code = request.user.last_name
		school_name = SchoolMaster.objects.get(school_code=school_code).school_name
		boys=StudentMaster.objects.values().filter(school_code=school_code,gender="Male").count()
		girls=StudentMaster.objects.values().filter(school_code=school_code,gender="Female").count()
		staff=StaffMaster.objects.values().filter(staff_school_code=school_code).count()
		present_students=Attendance.objects.values().filter(school_code=school_code,group_id="4",date=today).count()
		present_staff=Attendance.objects.values().filter(school_code=school_code,group_id="3",date=today).count()
		absent_students=StudentMaster.objects.values().filter(school_code=school_code).count()-present_students
		absent_staff =staff-present_staff
		student=StudentMaster.objects.values().filter(school_code=school_code).count()
		teacher=StaffMaster.objects.values().filter(staff_school_code=school_code).count()
		parents=ParentsMaster.objects.values().filter(Parents_school_code=school_code).count()
		transport=School_Transport.objects.values().filter(school_code=school_code).count()

		dict={"student":student,"teacher":teacher,"parents":parents,"transport":transport,"boys":boys,"girls":girls,"staff":staff,"school_name":school_name,"present_students":present_students,"absent_students":absent_students,"present_staff":present_staff,"absent_staff":absent_staff}
		d.update(dict)

		x = notice_board_school.objects.values().filter(school_code=school_code).order_by('-created_on')
		time1 = datetime.datetime.now()
		for i in x:
			diff = time1 - i["created_on"].replace(tzinfo=None)

			if diff.days == 0 and diff.seconds // 60 < 60:
				i.update({"diff": str(diff.seconds // 60) + "min ago"})
				i.update({"status": "New"})
			if diff.days == 0 and diff.seconds // 60 > 60:
				i.update({"diff": str(diff.seconds // 3600) + "hours ago"})
				i.update({"status": "New"})
			if diff.days > 0:
				if diff.days == 1:
					i.update({"diff": str(diff.days) + "day ago"})
					i.update({"status": "New"})
				else:
					i.update({"diff": str(diff.days) + "days ago"})
		d.update({"x":x})
	except:
		pass



	if User.objects.filter(groups=2, username=request.user.username).exists():#admin
		return render(request,'SchoolDesign/index.html',d)
	elif User.objects.filter(groups=5, username=request.user.username).exists():#parents
		return redirect('parents')
	elif User.objects.filter(groups=4, username=request.user.username).exists():#student
		return redirect('student')
	elif User.objects.filter(groups=3, username=request.user.username).exists():#teacher
		return 	redirect('staff')

	else:
		return render(request, 'SchoolDesign/index.html', d)



@login_required(login_url='login')
def student(request):
	data= StudentMaster.objects.values().filter(user_name=request.user.username).first()
	print(data["parents_id"])
	data.update(ParentsMaster.objects.values().filter(user=data["parents_id"]).first())
	return render(request,'SchoolDesign/index3.html',data)



@login_required(login_url='login')
def parents(request):
	x =ParentsMaster.objects.get(Parents_mobile=request.user.username)
	child=StudentMaster.objects.values().filter(parents_id=x.user_id)
	for i in child:
		i.update(ParentsMaster.objects.values().filter(user_id=i["parents_id"]).first())

	d={"child":child}
	return render(request,'SchoolDesign/index4.html',d)


from json import dumps
@login_required(login_url='login')
def staff(request):
	
	data=StaffMaster.objects.values().filter(staff_email=request.user.username).first()
	return render(request,'SchoolDesign/index5.html',data  )

@login_required(login_url='login')
def Allstudent(request):
    school_code = request.user.last_name
    mediums = MediumMaster.objects.values('medium_name').filter(school_code=school_code)
    classes = ClassMaster.objects.values('class_name').filter(school_code=school_code)
    division = DivisionMaster.objects.values('division_name').filter(school_code=school_code)
    dictonary={"mediums":mediums,"classes":classes,"division":division}
    data=StudentMaster.objects.values().filter(school_code=school_code)
    n=1
    for i in data:
        if n < 10:
            i.update({'index': '0' + str(n)})
        else:
            i.update({'index': n})
        n += 1
    d = {"data": data}
    dictonary.update(d)
    if request.method == 'POST':
        medium_name = request.POST.get('medium')
        class_name = request.POST.get('class')
        division_name = request.POST.get('section')
        if medium_name=="":
            data=StudentMaster.objects.values().filter(school_code=school_code)
        elif class_name=="" :
            data=StudentMaster.objects.values().filter(medium_name=medium_name,school_code=school_code)
        elif division_name=="":
            data=StudentMaster.objects.values().filter(medium_name=medium_name,class_name=class_name,school_code=school_code)
        else:
            data=StudentMaster.objects.values().filter(medium_name=medium_name,class_name=class_name,division_name=	division_name,school_code=school_code)
        n=1
        for i in data:
            if n < 10:
                i.update({'index': '0' + str(n)})
            else:
                i.update({'index': n})
            n += 1
        d = {"data": data}
        dictonary.update(d)
    return render(request,'SchoolDesign/all-student.html',dictonary)


@login_required(login_url='login')
def  student_delete(request,id):
	school_code = request.user.last_name
	user = User.objects.get(id=id)
	parents_id=StudentMaster.objects.get(pk=id).parents_id
	parents_user = User.objects.get(pk=parents_id)

	total_child=StudentMaster.objects.values().filter(parents_id=parents_id).count()
	print(parents_id,total_child)
	if total_child==1:
		parents_user.delete()
		user.delete()
		messages.success(request, "Successfully 1 student Deleted {} remaining.".format(total_child-1))
		messages.success(request, "Successfully parents Deleted")


	else:
		user.delete()
		messages.success(request, "Successfully 1 student Deleted {} remaining.".format(total_child-1))

	#user.delete()
	
	return redirect('Allstudent')



@login_required(login_url='login')
def Allstaff(request):
	school_code = request.user.last_name
	mediums = MediumMaster.objects.values('medium_name').filter(school_code=school_code)
	dictonary = {"mediums": mediums,}
	data = StaffMaster.objects.values().filter(staff_school_code=school_code)
	n = 1
	for i in data:
		if n < 10:
			i.update({'index': '0' + str(n)})
		else:
			i.update({'index': n})
		n += 1
	d = {"data": data}
	dictonary.update(d)

	if request.method == 'POST':
		medium_name = request.POST.get('medium')
		if medium_name=="":
		    medium_name="English"
		class_name = request.POST.get('class')
		division_name = request.POST.get('section')
		n = 1
		data = StaffMaster.objects.values().filter(staff_medium_name=medium_name,
													staff_school_code=school_code).order_by('staff_class_name','staff_division_name')

		for i in data:
			if n < 10:
				i.update({'index': '0' + str(n)})
			else:
				i.update({'index': n})
			n += 1
		d = {"data": data}
		dictonary.update(d)

	return render(request,'SchoolDesign/all-teacher.html',dictonary)

@login_required(login_url='login')
def staff_delete(request,id):
    school_code = request.user.last_name
    user = User.objects.get(id=id)
    staff=StaffMaster.objects.get(pk=id)
    staff.delete()
    user.delete()
    messages.success(request, "Successfully staff Deleted")
    return redirect('Allstaff')



@login_required(login_url='login')
def student_details(request):
	data={}
	if request.method == 'POST':
		user_name = request.POST.get('username').strip()
		data = StudentMaster.objects.values().filter(user_name=user_name)

		for i in data:
			i.update(ParentsMaster.objects.values().filter(user_id=i["parents_id"]).first())
		return render(request, 'SchoolDesign/admission-detail.html', {"data": data})

	return render(request,'SchoolDesign/admission-detail.html',{"data": data})



@login_required(login_url='login')
def owner_details_update(request):
	data={}
	school_code = request.user.last_name
	school_data = SchoolMaster.objects.values().filter(school_code=school_code).first()
	#owner_data = SchoolMaster.objects.values().filter(school_code=school_code)
	school_data.update(OwnerMaster.objects.values().filter(owner_school_code=school_code).first())
	    
	
	
	if request.method == 'POST':
		user_name = request.POST.get('username').strip()
		data = StudentMaster.objects.values().filter(user_name=user_name)

		for i in data:
			i.update(ParentsMaster.objects.values().filter(user_id=i["parents_id"]).first())
		return render(request, 'SchoolDesign/admission-detail.html', {"data": school_data})

	return render(request,'owner_profil_update.html',{"data": school_data})



@login_required(login_url='login')
def admission_detail(request,id):
    data=StudentMaster.objects.values().filter(user_id=id)
    for i in data:
        i.update({"student_id":i["user_id"]})
        i.update(ParentsMaster.objects.values().filter(user_id=i["parents_id"]).first())
    return render(request,'SchoolDesign/admission-detail.html',{"data":data})






@login_required(login_url='login')
def staff_details(request):
	if request.method == 'POST':
		user_name = request.POST.get('username')
		data = StaffMaster.objects.values().filter(staff_email=user_name)

		return render(request, 'SchoolDesign/teacher-details.html', {"data": data})

	return render(request,'SchoolDesign/teacher-details.html')



@login_required(login_url='login')
def add_staff_detail(request,id):
	data=StaffMaster.objects.values().filter(staff_user_id=id)
	return render(request,'SchoolDesign/teacher-details.html',{"data":data})



@login_required(login_url='login')
def load_parents(request):
	# global class_name
	# school_code = request.user.last_name
	#if User.objects.filter(username=parents_mobile).exists():
	#	pass
	school_code = request.user.last_name
	parents_mobile = request.GET.get('parents_info')
	print(User.objects.filter(username=parents_mobile).exists())
	print(parents_mobile)
	parents_info=ParentsMaster.objects.filter(Parents_mobile=parents_mobile,Parents_school_code=school_code)
	if parents_info.exists():
		#parents_info=parents_info.values()
		data=parents_info.values().first()
		data.update({"existance_status":"Existing parents!!  to change parents details please change mobile number first."} )
		parents_info=[data,]
	else:
		
		parents_info=[{"fathername":"","mothername":"","existance_status":"New parents","father_occupation":"","mother_occupation":"","Parents_email":"","Parents_Address":"","Parents_city":"","Parents_pincode":""},]

	#parents_info=ParentsMaster.objects.values().filter(Parents_mobile=parents_mobile)
	print(parents_info)
	#Division=DivisionMaster.objects.values().filter(medium_name=medium_name,school_code=school_code,class_name=class_name)


	return render(request, 'load-parents_info.html',{"parents_info":parents_info})



@login_required(login_url='login')
def admit_form(request):
    school_code = request.user.last_name
    mediums=MediumMaster.objects.values('medium_name').filter(school_code=school_code)
    classes=ClassMaster.objects.values('class_name').filter(school_code=school_code)
    division = DivisionMaster.objects.values('division_name').filter(school_code=school_code)
    d={"mediums":mediums,"classes":classes,"division":division}
    if request.method == 'POST':
        Full_name= request.POST.get('Full_name').strip()
        gender = request.POST.get('gender').strip()
        date_of_birth=request.POST.get('dob').strip()
        # email = request.POST.get('email').strip()
        #mobile = request.POST.get('mobile')
        #blood_group = request.POST.get('blood_group')
        #reservation = request.POST.get('reservation')
        medium_name = request.POST.get('medium').strip()
        class_name = request.POST.get('class').strip()
        division_name = request.POST.get('section').strip()
        admission_no = request.POST.get('addmission_no').strip()
        try:
            image = request.FILES['image']
        except:
            image=""
        username=Full_name.split()[0]+str(User.objects.values().last()["id"]+2) # creating unique user id for students
        fathername= request.POST.get('fathername').strip()
        mothername= request.POST.get('mothername').strip()
        father_occupation= request.POST.get('father_occupation')
        mother_occupation= request.POST.get('mother_occupation')
        #Religion= request.POST.get('Religion')
        parents_email= request.POST.get('parents_email')
        if parents_email is None:
            parents_email=""
        parents_mobile = request.POST.get('parents_mobile').strip()
        Address = request.POST.get('Address').strip()
        city = request.POST.get('city')
        pincode = request.POST.get('pincode').strip()


        #parents
        parents_info=ParentsMaster.objects.filter(Parents_mobile=parents_mobile)
        parents_info=ParentsMaster.objects.filter(Parents_mobile=parents_mobile,Parents_school_code=school_code)
        #user_exist=User.objects.filter(username=parents_mobile,is_staff=1, is_active=1).count() 
        print("************************************************")
        print(parents_mobile,fathername,school_code,parents_email)
        
        if parents_info.exists(): # user_exist=1 means >0 means parents already exist
            parents_user_id=parents_info.first().pk
            print("*************** parents already exist*********************************")
            students_info=StudentMaster.objects.filter(Full_name=Full_name,school_code=school_code,parents_id=parents_user_id)
            messages.info(request, "parents already exist")


            #parents_user_id = User.objects.get(username=parents_mobile, is_staff=1, is_active=1, first_name=fathername,last_name=school_code, email=parents_email).id
            #user_availble = User.objects.filter(is_staff=1, is_active=1, first_name=Full_name, last_name=school_code,).count()
            if students_info.exists():#students avalable
                print("*************** students already exist*********************************")
                messages.info(request, "student already exist")
            #if user_availble == 1: #students avalable
                #student_id = User.objects.get(is_staff=1, is_active=1, first_name=Full_name, last_name=school_code).id
                student_id=students_info.first().pk
            else:
            #if user_availble == 0:#students not avalable

                user, created = User.objects.get_or_create(username=username, is_staff=1, is_active=1,
                											first_name=Full_name, last_name=school_code)
                user.set_password("12345")
                user.save()
                user.groups.add(4)  # adding group= "studnt" id of group is 4
                user_id = user.pk
                student, created = StudentMaster.objects.get_or_create(user_id=user_id, user_name=username,
                                                                            Full_name=Full_name, gender=gender,
                                                                            date_of_birth=date_of_birth,
                                                                            Address=Address, city=city,
                                                                            pincode=pincode,
                                                                            school_code=school_code,
                                                                            admission_no=admission_no,
                                                                            medium_name=medium_name,
                                                                            class_name=class_name,
                                                                            division_name=division_name,
                                                                            email=""	,														
                                                                            parents_id=parents_user_id, image=image,password='12345')
                student.save()
                
                student_id = student.pk

            return redirect(f'/admission_detail/{student_id}')
	

        elif ParentsMaster.objects.filter(Parents_mobile=parents_mobile).exists():# parents exists in another school
            print("***************  parents exist in another achool *********************************")
            Parents_school_code=ParentsMaster.objects.filter(Parents_mobile=parents_mobile).first().Parents_school_code
            school_name=SchoolMaster.objects.filter(school_code=Parents_school_code).first().school_name
            messages.info(request, "Warning:parents mobile already exists!!!!!!! in {} please provide another number.".format(school_name))
            student_id=1
            return redirect(f'/admit_form/')
        else:
            print("*************** new parents parents *********************************")
            user, created = User.objects.get_or_create(username=parents_mobile, is_staff=1, is_active=1, first_name=fathername,
            											last_name=school_code)
            user.set_password("12345")
            user.save()
            user.groups.add(5)
            parents_user_id = user.pk
            if created:
                parents, created = ParentsMaster.objects.get_or_create(user_id=parents_user_id, fathername=fathername,
                                                                        mothername=mothername,
                                                                        Parents_email= parents_email,
                                                                        father_occupation=father_occupation,
                                                                        mother_occupation=mother_occupation,
                                                                        Parents_mobile=parents_mobile, Parents_Address=Address,
                                                                        Parents_city=city, Parents_pincode=pincode,
                                                                        
                                                                        password='12345',
                                                                        
                                                                        Parents_school_code= school_code)

                parents.save()
                # user_availble=User.objects.filter(is_staff=1, is_active=1,first_name=Full_name,last_name=school_code).count()
                # if user_availble==1:
                # 	student_id= User.objects.get(is_staff=1, is_active=1,first_name=Full_name,last_name=school_code).id	
                # if user_availble==0:
                user, created = User.objects.get_or_create(username=username , is_staff=1, is_active=1,first_name=Full_name,last_name=school_code)
                user.set_password("12345")
                user.save()
                user.groups.add(4) # adding group= "studnt" id of group is 4
                user_id=user.pk
                student,created=StudentMaster.objects.get_or_create(user_id=user_id,user_name=username,Full_name=Full_name,gender=gender,date_of_birth=date_of_birth,email="",
                Address=Address,city=city,pincode=pincode,school_code= school_code ,admission_no=admission_no,medium_name=medium_name,
                class_name=class_name,division_name=division_name,parents_id=parents_user_id,image=image,password='12345')
                student.save()
                student_id=student.pk
                messages.info(request, "New Parents Registered")
                messages.info(request, "New student  Registered")
            return redirect(f'/admission_detail/{student_id}')

    return render(request,'SchoolDesign/admit-form.html',d)



# def parents_form(request,id):
# 	school_code = request.user.last_name
# 	if request.method == 'POST':
# 		print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@okk")
# 		First_name= request.POST.get('First_name')
# 		Last_name = request.POST.get('Last_name')
# 		gender = request.POST.get('gender')
# 		date_of_birth= request.POST.get('dob')
# 		email = request.POST.get('email')
# 		mobile = request.POST.get('mobile')
# 		Address = request.POST.get('Address')
# 		city = request.POST.get('city')
# 		pincode= request.POST.get('pincode')
# 		blood_group = request.POST.get('blood_group')
# 		Religion= request.POST.get('Religion')
# 		occupation = request.POST.get('occupation')
# 		image = request.FILES['image']
# 		print("**********",First_name,Last_name,gender,date_of_birth,email,mobile,Address,city,pincode,blood_group,Religion,occupation,image )
# 		user, created = User.objects.get_or_create(username=mobile, is_staff=1, is_active=1, first_name=First_name,
# 											   last_name=school_code, email=email)
# 		print(created)
# 		user.set_password(First_name + "12345")
# 		user.save()
# 		user.groups.add(5)
# 		user_id = user.pk
# 		print(user_id,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@###########")
# 		if created:
# 			parents, created = ParentsMaster.objects.get_or_create(user_id=user_id, Parents_First_name=First_name,Parents_Last_name=Last_name, Parents_gender=gender,Parents_date_of_birth=date_of_birth, Parents_email=email,
# 			Parents_mobile=mobile, Parents_Address=Address, Parents_city=city,Parents_pincode=pincode, Parents_blood_group=blood_group,Parents_Religion=Religion, Parents_occupation=occupation,Parents_school_code=school_code,
# 															   Parents_image=image)
# 			parents.save()
# 		student = StudentMaster.objects.get(user_id=id)
# 		id=id
# 		student.parents_id=user_id
# 		student.save()
# 		print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Ookkk")
# 		#return render(request, 'SchoolDesign/admit-form.html')
# 		return redirect(f'/admission_detail/{id}')
# 	return render(request, 'SchoolDesign/add-parents.html')






# @login_required(login_url='login')
# def add_staff(request):
# 	school_code = request.user.last_name
# 	mediums = MediumMaster.objects.values('medium_name').filter(school_code=school_code)
# 	classes = ClassMaster.objects.values('class_name').filter(school_code=school_code)
	
# 	division = DivisionMaster.objects.values('division_name').filter(school_code=school_code)

# 	d = {"mediums": mediums, "classes": classes, "division": division}
# 	if request.method == 'POST':
# 		staff_First_name= request.POST.get('First_name')
# # 		staff_Last_name = request.POST.get('Last_name')
# 		staff_gender = request.POST.get('gender')
# 		staff_date_of_birth = request.POST.get('dob')
# 		staff_email = request.POST.get('email')
# 		staff_mobile = request.POST.get('mobile')
# 		staff_Address = request.POST.get('Address')
# 		staff_city = request.POST.get('city')
# 		staff_pincode= request.POST.get('pincode')
# # 		staff_blood_group = request.POST.get('blood_group')
# # 		staff_Religion= request.POST.get('Religion')
# # 		staff_qualification = request.POST.get('qualification')
# 		staff_medium_name = request.POST.get('medium')
# 		staff_class_name = request.POST.get('class')
# 		staff_division_name = request.POST.get('section')
# 		# staff_subject = request.POST.get('subject')
# 		staff_image = request.FILES['image']
# 		user_availble=User.objects.filter(is_staff=1, is_active=1,first_name=staff_First_name,last_name=school_code,email=staff_email).count()
# 		if user_availble==0:
# 			user, created = User.objects.get_or_create(username=staff_email , is_staff=1, is_active=1,first_name=staff_First_name,last_name=school_code,email=staff_email)
# 			user.set_password("12345")
# 			user.save()
# 			user.groups.add(3)
# 			user_id=user.pk
# 			staff,created=StaffMaster.objects.get_or_create( staff_user_id=user_id, staff_First_name= staff_First_name,staff_user_name=staff_email ,  staff_gender= staff_gender, staff_date_of_birth= staff_date_of_birth, staff_email= staff_email,
# 															 staff_mobile= staff_mobile, staff_Address= staff_Address, staff_city= staff_city, staff_pincode= staff_pincode, staff_school_code= school_code ,
# 															 staff_medium_name= staff_medium_name,
# 															 staff_class_name= staff_class_name, staff_division_name= staff_division_name,staff_image= staff_image,password='12345')
# 			staff.save()
# 			staff_id=staff.pk

# 			return redirect(f'/add_staff_detail/{staff_id}')
# 		else:
# 			messages.info(request,"Warning:user already exists!!!!!!!")

# 	return render(request, 'SchoolDesign/add-teacher.html',d)




@login_required(login_url='login')
def add_staff(request):
    school_code = request.user.last_name
    mediums = MediumMaster.objects.values('medium_name').filter(school_code=school_code)
    classes = ClassMaster.objects.values('class_name').filter(school_code=school_code)
    division = DivisionMaster.objects.values('division_name').filter(school_code=school_code)
    d = {"mediums": mediums, "classes": classes, "division": division}
    if request.method == 'POST':
        staff_First_name= request.POST.get('First_name')
        staff_Last_name = request.POST.get('Last_name')
        staff_gender = request.POST.get('gender')
        staff_date_of_birth = request.POST.get('dob')
        staff_email = request.POST.get('email')
        staff_mobile = request.POST.get('mobile')
        staff_Address = request.POST.get('Address')
        staff_city = request.POST.get('city')
        staff_pincode= request.POST.get('pincode')
        staff_blood_group = request.POST.get('blood_group')
        staff_Religion= request.POST.get('Religion')
        staff_qualification = request.POST.get('qualification')
        staff_medium_name = request.POST.get('medium')
        if staff_medium_name=="":
            staff_medium_name="English"
        staff_class_name = request.POST.get('class')
        staff_division_name = request.POST.get('section')
		# staff_subject = request.POST.get('subject')
        try:
            staff_image = request.FILES['image']
        except:
            staff_image=""
        staff_user_info=User.objects.filter(email=staff_email) #test staff user exit or not
        staff_user_info=User.objects.filter( username=staff_email)
        if staff_user_info.exists():
            print("staff already exist")
            print("*************** StudentMaster already exist*********************************")
            #students_info=StudentMaster.objects.filter(Full_name=Full_name,school_code=school_code,parents_id=parents_user_id)
            school_name_exist=staff_user_info.values().first()["first_name"]
            messages.info(request, "staff already exist in "+school_name_exist+" by the email "+staff_email)
            #print(school_info.values().first()["school_name"])
            return redirect('/add_staff')
        user_availble=User.objects.filter(is_staff=1, is_active=1,first_name=staff_First_name,last_name=school_code,email=staff_email).count()
        if user_availble==0:
            user, created = User.objects.get_or_create(username=staff_email , is_staff=1, is_active=1,first_name=staff_First_name,last_name=school_code,email=staff_email)
            user.set_password("12345")
            user.save()
            user.groups.add(3)
            user_id=user.pk
            staff,created=StaffMaster.objects.get_or_create( staff_user_id=user_id, staff_First_name= staff_First_name,staff_user_name=staff_email , staff_Last_name= staff_Last_name, staff_gender= staff_gender, staff_date_of_birth= staff_date_of_birth, staff_email= staff_email,
															 staff_mobile= staff_mobile, staff_Address= staff_Address, staff_city= staff_city, staff_pincode= staff_pincode, staff_blood_group= staff_blood_group, staff_Religion= staff_Religion, staff_school_code= school_code ,
															 staff_qualification=staff_qualification,staff_medium_name= staff_medium_name,
															 staff_class_name= staff_class_name, staff_division_name= staff_division_name,staff_image= staff_image,password='12345')
            staff.save()
            staff_id=staff.pk
            return redirect(f'/add_staff_detail/{staff_id}')
        else:
            messages.info(request,"Warning:user already exists!!!!!!!")
    return render(request, 'SchoolDesign/add-teacher.html',d)




@login_required(login_url='login')
def add_other_staff(request):
    school_code = request.user.last_name
    mediums = MediumMaster.objects.values('medium_name').filter(school_code=school_code)
    classes = ClassMaster.objects.values('class_name').filter(school_code=school_code)
    division = DivisionMaster.objects.values('division_name').filter(school_code=school_code)
    d = {"mediums": mediums, "classes": classes, "division": division}
    if request.method == 'POST':
        staff_First_name= request.POST.get('First_name')
        staff_Last_name = request.POST.get('Last_name')
        staff_gender = request.POST.get('gender')
        staff_date_of_birth = request.POST.get('dob')
        staff_email = request.POST.get('email')
        staff_mobile = request.POST.get('mobile')
        staff_Address = request.POST.get('Address')
        staff_city = request.POST.get('city')
        staff_pincode= request.POST.get('pincode')
        staff_blood_group = request.POST.get('blood_group')
        staff_Religion= request.POST.get('Religion')
        staff_qualification = request.POST.get('qualification')
        staff_medium_name = request.POST.get('medium')
        if staff_medium_name=="":
            staff_medium_name="English"
        staff_class_name = request.POST.get('class')
        staff_division_name = request.POST.get('section')
		# staff_subject = request.POST.get('subject')
        try:
            staff_image = request.FILES['image']
        except:
            staff_image=""
        staff_user_info=User.objects.filter(email=staff_email) #test staff user exit or not
        staff_user_info=User.objects.filter( username=staff_email)
        if staff_user_info.exists():
            print("staff already exist")
            print("*************** StudentMaster already exist*********************************")
            #students_info=StudentMaster.objects.filter(Full_name=Full_name,school_code=school_code,parents_id=parents_user_id)
            school_name_exist=staff_user_info.values().first()["first_name"]
            messages.info(request, "staff already exist in "+school_name_exist+" by the email "+staff_email)
            #print(school_info.values().first()["school_name"])
            return redirect('/add_staff')
        user_availble=User.objects.filter(is_staff=1, is_active=1,first_name=staff_First_name,last_name=school_code,email=staff_email).count()
        if user_availble==0:
            user, created = User.objects.get_or_create(username=staff_email , is_staff=1, is_active=1,first_name=staff_First_name,last_name=school_code,email=staff_email)
            user.set_password("12345")
            user.save()
            user.groups.add(3)
            user_id=user.pk
            staff,created=StaffMaster.objects.get_or_create( staff_user_id=user_id, staff_First_name= staff_First_name,staff_user_name=staff_email , staff_Last_name= staff_Last_name, staff_gender= staff_gender, staff_date_of_birth= staff_date_of_birth, staff_email= staff_email,
															 staff_mobile= staff_mobile, staff_Address= staff_Address, staff_city= staff_city, staff_pincode= staff_pincode, staff_blood_group= staff_blood_group, staff_Religion= staff_Religion, staff_school_code= school_code ,
															 staff_qualification=staff_qualification,staff_medium_name= staff_medium_name,
															 staff_class_name= staff_class_name, staff_division_name= staff_division_name,staff_image= staff_image,password='12345')
            staff.save()
            staff_id=staff.pk
            return redirect(f'/add_staff_detail/{staff_id}')
        else:
            messages.info(request,"Warning:user already exists!!!!!!!")
    return render(request, 'SchoolDesign/add-other-staff.html',d)




@login_required(login_url='login')
def allclass_form(request):
	school_code = request.user.last_name
	n=1
	x =  DivisionMaster.objects.values('division_id','medium_name', 'class_name', 'division_name').filter(school_code=school_code)
	for i in x:
		if n<10:
	         i.update({'index':'0'+str(n)})
		else:
			i.update({'index':n})
		n+=1

	return render(request,'SchoolDesign/all-class.html',{'data':x})






@login_required(login_url='login')
def addclass_form(request):
	school_code=request.user.last_name
	# school_code = UserMaster.objects.get(user_name=username).school_code
	if request.method == "POST":
		medium_name = request.POST.get('medium')
		class_name = request.POST.get('standard')
		division_name = request.POST.get('division_name')
	


		new_class = ClassMaster.objects.filter(school_code=school_code,medium_name=medium_name)
		new_class.update_or_create(school_code=school_code,medium_name=medium_name, class_name=class_name)

		# standard_id=new_class.pk
		new_section =  DivisionMaster.objects.filter(school_code=school_code,medium_name=medium_name, class_name=class_name,division_name=division_name)
		new_section.update_or_create(school_code=school_code,medium_name=medium_name, class_name=class_name,division_name=division_name)
		messages.success(request,"Successfully saved")
		return redirect('addclass_form')
	mediums=MediumMaster.objects.values('medium_name').filter(school_code=school_code)
	return render(request,'SchoolDesign/add-class.html',{"mediums":mediums})





@login_required(login_url='login')
def class_delete(request,id):
	school_code = request.user.last_name
	print(id)
	division = DivisionMaster.objects.get(division_id=id)
	if (DivisionMaster.objects.values().filter(school_code=school_code,class_name=division.class_name).count()==1):
		clas=ClassMaster.objects.get(school_code=school_code,medium_name=division.medium_name,class_name=division.class_name)
		clas.delete()
		division.delete()
	else:
		division.delete()
	return redirect('allclass_form')
	# return render(request,'SchoolDesign/all-class.html')







def attendence(request):
	attendance_update()
	school_code = request.user.last_name
	mediums = MediumMaster.objects.values('medium_name').filter(school_code=school_code)
	classes = ClassMaster.objects.values('class_name').filter(school_code=school_code)
	division = DivisionMaster.objects.values('division_name').filter(school_code=school_code)
	d = {"mediums": mediums, "classes": classes, "division": division,"x":"fas fa-times text-danger"}
	data=StudentMaster.objects.values().filter(school_code=school_code)
	month=datetime.datetime.now().month
	today=int(datetime.datetime.now().strftime("%d"))
	year = int(datetime.datetime.now().strftime("%Y"))
	mon = datetime.date(1900, int(month), 1).strftime('%B')
	mahina=datetime.datetime.now().month
	# getting attendance directly
	for i in data:
		if mahina==int(month):
			for j in range(1,today+1):
				date = f"{year}-{month}-{j}"

				attn = Attendance.objects.values().filter(rf_id=i["student_card_number"],school_code=school_code, date=date)

				if (date[5:9]) == "8-15":
					i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
				elif (date[5:9]) == "1-26":
					i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

				elif school_holiday.objects.values().filter(date=date,school_code=school_code).count():
					i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


				elif attn.first() is not None:
					i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" + str(attn.first()["intime"]),
							  f"{j}out": "OUT:-" + str(attn.first()["outtime"])})

				elif pydate(date).strftime("%a") == "Sun":
					i.update({j: 'fas fa-home',f"{j}in":"sunday"})


				else:
					i.update({j: 'fas fa-times text-danger'})


		elif month=="02" and year % 4==0:
			for j in range(1,30):
				date = f"{year}-{month}-{j}"

				attn = Attendance.objects.values().filter(rf_id=i["student_card_number"],school_code=school_code, date=date)

				if (date[5:9]) == "8-15":
					i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
				elif (date[5:9]) == "1-26":
					i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

				elif school_holiday.objects.values().filter(date=date,school_code=school_code).count():
					i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


				elif attn.first() is not None:
					i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" + str(attn.first()["intime"]),
							  f"{j}out": "OUT:-" + str(attn.first()["outtime"])})

				elif pydate(date).strftime("%a") == "Sun":
					i.update({j: 'fas fa-home', f"{j}in": "sunday"})
					#holiday=fas fa-smile


				else:
					i.update({j: 'fas fa-times text-danger'})

		elif month == "02":
			for j in range(1, 29):
				date = f"{year}-{month}-{j}"

				attn = Attendance.objects.values().filter(rf_id=i["student_card_number"] ,school_code=school_code, date=date)

				if (date[5:9]) == "8-15":
					i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
				elif (date[5:9]) == "1-26":
					i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

				elif school_holiday.objects.values().filter(date=date,school_code=school_code).count():
					i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


				elif attn.first() is not None:
					i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" + str(attn.first()["intime"]),
							  f"{j}out": "OUT:-" + str(attn.first()["outtime"])})

				elif pydate(date).strftime("%a") == "Sun":
					i.update({j: 'fas fa-home', f"{j}in": "sunday"})
				# holiday=fas fa-smile

				else:
					i.update({j: 'fas fa-times text-danger'})


		elif month in ["04","06","07","09","11"]:
			for j in range(1,31):
				date = f"{year}-{month}-{j}"

				attn = Attendance.objects.values().filter(rf_id=i["student_card_number"] ,school_code=school_code, date=date)

				if (date[5:9]) == "8-15":
					i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
				elif (date[5:9]) == "1-26":
					i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

				elif school_holiday.objects.values().filter(date=date,school_code=school_code).count():
					i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


				elif attn.first() is not None:
					i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" +str(attn.first()["intime"]),f"{j}out": "OUT:-" +str(attn.first()["outtime"])})
				elif pydate(date).strftime("%a") == "Sun":
					i.update({j: 'fas fa-home', f"{j}in": "sunday"})


				else:
					i.update({j: 'fas fa-times text-danger'})



		else:
			for j in range(1,32):
				date = f"{year}-{month}-{j}"

				attn = Attendance.objects.values().filter(rf_id=i["student_card_number"] ,school_code=school_code, date=date)

				if (date[5:9]) == "8-15":
					i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
				elif (date[5:9]) == "1-26":
					i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

				elif school_holiday.objects.values().filter(date=date,school_code=school_code).count():
					i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


				elif attn.first() is not None:
					i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" + str(attn.first()["intime"]),
							  f"{j}out": "OUT:-" + str(attn.first()["outtime"])})

				elif pydate(date).strftime("%a") == "Sun":
					i.update({j: 'fas fa-home', f"{j}in": "sunday"})


				else:
					i.update({j: 'fas fa-times text-danger'})
	d.update({"data": data})
	
	if request.method == "POST":# getting attendatce after search or filter
		medium_name = request.POST.get('medium_name')
		if medium_name=="":
		    medium_name="English"
		class_name = request.POST.get('class_name')
		division_name = request.POST.get('division_name')
		month=request.POST.get('month')
		if month=="":
		    month=datetime.datetime.now().month
		#attn=Attendance.objects.values().filter(medium_name=medium_name,class_name=class_name,division_name=division_name,date__range=["2020-08-01","2020-08-31"],school_code=school_code,group_id="4")
		print("medium",medium_name,"class",class_name,"division",division_name,"month",month,"************test*********************")
		data = StudentMaster.objects.values().filter(medium_name=medium_name,class_name=class_name,division_name=division_name,school_code=school_code)
		if class_name is None and division_name is None:
			print("111111111111111111111111111111111")
			data=StudentMaster.objects.values().filter(medium_name=medium_name,school_code=school_code)
				
		elif class_name =="" :
			print("222222222222222222222222222222")
			data=StudentMaster.objects.values().filter(medium_name=medium_name,school_code=school_code)
		elif division_name=="":
			print("3333333")
			data=StudentMaster.objects.values().filter(medium_name=medium_name,class_name=class_name,school_code=school_code)	
		print(data)
		today=int(datetime.datetime.now().strftime("%d"))
		year = int(datetime.datetime.now().strftime("%Y"))
		mon = datetime.date(1900, int(month), 1).strftime('%B')
		req = {"medium_name": medium_name, "class_name": class_name, "division_name": division_name,"month":mon, "year":year}
		print(req)
		d.update(req)
		print(d)
		mahina=datetime.datetime.now().month
		for i in data:
			if mahina==int(month):
				for j in range(1,today+1):
					date = f"{year}-{month}-{j}"

					attn = Attendance.objects.values().filter(rf_id=i["student_card_number"] ,school_code=school_code, date=date)

					if (date[5:9]) == "8-15":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
					elif (date[5:9]) == "1-26":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

					elif school_holiday.objects.values().filter(date=date,school_code=school_code).count():
						i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


					elif attn.first() is not None:
						i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" + str(attn.first()["intime"]),
								  f"{j}out": "OUT:-" + str(attn.first()["outtime"])})

					elif pydate(date).strftime("%a") == "Sun":
						i.update({j: 'fas fa-home',f"{j}in":"sunday"})


					else:
						i.update({j: 'fas fa-times text-danger'})


			elif month=="02" and year % 4==0:
				for j in range(1,30):
					date = f"{year}-{month}-{j}"

					attn = Attendance.objects.values().filter(rf_id=i["student_card_number"] ,school_code=school_code, date=date)

					if (date[5:9]) == "8-15":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
					elif (date[5:9]) == "1-26":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

					elif school_holiday.objects.values().filter(date=date,school_code=school_code).count():
						i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


					elif attn.first() is not None:
						i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" + str(attn.first()["intime"]),
								  f"{j}out": "OUT:-" + str(attn.first()["outtime"])})

					elif pydate(date).strftime("%a") == "Sun":
						i.update({j: 'fas fa-home', f"{j}in": "sunday"})
						#holiday=fas fa-smile


					else:
						i.update({j: 'fas fa-times text-danger'})

			elif month == "02":
				for j in range(1, 29):
					date = f"{year}-{month}-{j}"

					attn = Attendance.objects.values().filter(rf_id=i["student_card_number"] ,school_code=school_code, date=date)

					if (date[5:9]) == "8-15":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
					elif (date[5:9]) == "1-26":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

					elif school_holiday.objects.values().filter(date=date,school_code=school_code).count():
						i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


					elif attn.first() is not None:
						i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" + str(attn.first()["intime"]),
								  f"{j}out": "OUT:-" + str(attn.first()["outtime"])})

					elif pydate(date).strftime("%a") == "Sun":
						i.update({j: 'fas fa-home', f"{j}in": "sunday"})
					# holiday=fas fa-smile

					else:
						i.update({j: 'fas fa-times text-danger'})


			elif month in ["04","06","07","09","11"]:
				for j in range(1,31):
					date = f"{year}-{month}-{j}"

					attn = Attendance.objects.values().filter(rf_id=i["student_card_number"] ,school_code=school_code, date=date)

					if (date[5:9]) == "8-15":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
					elif (date[5:9]) == "1-26":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

					elif school_holiday.objects.values().filter(date=date,school_code=school_code).count():
						i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


					elif attn.first() is not None:
						i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" +str(attn.first()["intime"]),f"{j}out": "OUT:-" +str(attn.first()["outtime"])})
					elif pydate(date).strftime("%a") == "Sun":
						i.update({j: 'fas fa-home', f"{j}in": "sunday"})


					else:
						i.update({j: 'fas fa-times text-danger'})



			else:
				for j in range(1,32):
					date = f"{year}-{month}-{j}"

					attn = Attendance.objects.values().filter(rf_id=i["student_card_number"] ,school_code=school_code, date=date)

					if (date[5:9]) == "8-15":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
					elif (date[5:9]) == "1-26":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

					elif school_holiday.objects.values().filter(date=date,school_code=school_code).count():
						i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


					elif attn.first() is not None:
						i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" + str(attn.first()["intime"]),
								  f"{j}out": "OUT:-" + str(attn.first()["outtime"])})

					elif pydate(date).strftime("%a") == "Sun":
						i.update({j: 'fas fa-home', f"{j}in": "sunday"})


					else:
						i.update({j: 'fas fa-times text-danger'})
		d.update({"data": data})
	return render(request, 'SchoolDesign/student-attendence.html',d)





# from datetime import datetime, timedelta

@login_required(login_url='login')
def manual_attendence(request):
	school_code = request.user.last_name
	if request.method == 'POST':
		user_name = request.POST.get('username')

		import datetime
		#date = datetime.datetime.now()
		date=datetime.datetime.now() + datetime.timedelta(seconds=19800)
		attendance_timestamp=date.strftime("%d-%b-%y %H:%M:%S")
		print(user_name,date, "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
		try:
			if User.objects.filter(groups=4, username=user_name).exists():  # student
				rf_id= StudentMaster.objects.get(user_name=user_name).student_card_number
				data = attendance_api(school_code=school_code, attendance_timestamp=attendance_timestamp, rf_id=rf_id,
									  gwId="manual", )
				data.save()
				messages.success(request, "Successfully attendance saved!! ")
				return redirect('manual_attendence')
			elif User.objects.filter(groups=3, username=user_name).exists():
				rf_id = StaffMaster.objects.get(staff_user_name=user_name).staff_card_number
				data = attendance_api(school_code=school_code, attendance_timestamp=attendance_timestamp, rf_id=rf_id,
									  gwId="manual", )
				data.save()
				messages.success(request, "Successfully attendance saved!! ")
				return redirect('manual_attendence')
			else:
				messages.info(request, "invalid Username!! ")
		except:
			messages.info(request, "Something went wrong!!")


		return redirect('manual_attendence')

	return render(request, 'SchoolDesign/manual-attendence.html')





def staff_attendence(request):
	attendance_update()
	school_code = request.user.last_name
	mediums = MediumMaster.objects.values('medium_name').filter(school_code=school_code)
	classes = ClassMaster.objects.values('class_name').filter(school_code=school_code)
	division = DivisionMaster.objects.values('division_name').filter(school_code=school_code)
	d = {"mediums": mediums, "classes": classes, "division": division,"x":"fas fa-times text-danger"}
	today=int(datetime.datetime.now().strftime("%d"))
	year = int(datetime.datetime.now().strftime("%Y"))
	month=datetime.datetime.now().month
	mon = datetime.date(1900, int(month), 1).strftime('%B')
	mahina=datetime.datetime.now().month
	data = StaffMaster.objects.values().filter(staff_school_code=school_code)
	# getting staff attendance directly
	for i in data:
		if mahina==int(month):
			for j in range(1,today+1):
				date = f"{year}-{month}-{j}"

				attn = Attendance.objects.values().filter(rf_id=i["staff_card_number"] ,school_code=school_code, date=date)

				if (date[5:9]) == "8-15":
					i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
				elif (date[5:9]) == "1-26":
					i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

				elif school_holiday.objects.values().filter(date=date,school_code=school_code).count():
					i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


				elif attn.first() is not None:
					i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" + str(attn.first()["intime"]),
							  f"{j}out": "OUT:-" + str(attn.first()["outtime"])})

				elif pydate(date).strftime("%a") == "Sun":
					i.update({j: 'fas fa-home',f"{j}in":"sunday"})


				else:
					i.update({j: 'fas fa-times text-danger'})

		elif month == "02" and year % 4 == 0:
			for j in range(1, 30):
				date = f"{year}-{month}-{j}"

				attn = Attendance.objects.values().filter(rf_id=i["staff_card_number"] ,school_code=school_code, date=date)

				if (date[5:9]) == "8-15":
					i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
				elif (date[5:9]) == "1-26":
					i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

				elif school_holiday.objects.values().filter(date=date,school_code=school_code).count():
					i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


				elif attn.first() is not None:
					i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" + str(attn.first()["intime"]),
							  f"{j}out": "OUT:-" + str(attn.first()["outtime"])})

				elif pydate(date).strftime("%a") == "Sun":
					i.update({j: 'fas fa-home', f"{j}in": "sunday"})
				# holiday=fas fa-smile

				else:
					i.update({j: 'fas fa-times text-danger'})


		elif month=="02":
			for j in range(1,29):
				date = f"{year}-{month}-{j}"

				attn = Attendance.objects.values().filter(rf_id=i["staff_card_number"] ,school_code=school_code, date=date)

				if (date[5:9]) == "8-15":
					i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
				elif (date[5:9]) == "1-26":
					i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

				elif school_holiday.objects.values().filter(date=date,school_code=school_code).count():
					i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


				elif attn.first() is not None:
					i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" + str(attn.first()["intime"]),
							  f"{j}out": "OUT:-" + str(attn.first()["outtime"])})

				elif pydate(date).strftime("%a") == "Sun":
					i.update({j: 'fas fa-home', f"{j}in": "sunday"})
					#holiday=fas fa-smile


				else:
					i.update({j: 'fas fa-times text-danger'})







		elif month in ["04","06","07" "09","11"]:
			for j in range(1,31):
				date = f"{year}-{month}-{j}"

				attn = Attendance.objects.values().filter(rf_id=i["staff_card_number"] ,school_code=school_code, date=date)

				if (date[5:9]) == "8-15":
					i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
				elif (date[5:9]) == "1-26":
					i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

				elif school_holiday.objects.values().filter(date=date,school_code=school_code).count():
					i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


				elif attn.first() is not None:
					i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" +str(attn.first()["intime"]),f"{j}out": "OUT:-" +str(attn.first()["outtime"])})
				elif pydate(date).strftime("%a") == "Sun":
					i.update({j: 'fas fa-home', f"{j}in": "sunday"})


				else:
					i.update({j: 'fas fa-times text-danger'})



		else:
			for j in range(1,32):
				date = f"{year}-{month}-{j}"

				attn = Attendance.objects.values().filter(rf_id=i["staff_card_number"] ,school_code=school_code, date=date)

				if (date[5:9]) == "8-15":
					i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
				elif (date[5:9]) == "1-26":
					i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

				elif school_holiday.objects.values().filter(date=date,school_code=school_code).count():
					i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


				elif attn.first() is not None:
					i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" + str(attn.first()["intime"]),
							  f"{j}out": "OUT:-" + str(attn.first()["outtime"])})

				elif pydate(date).strftime("%a") == "Sun":
					i.update({j: 'fas fa-home', f"{j}in": "sunday"})


				else:
					i.update({j: 'fas fa-times text-danger'})
	d.update({"data": data})
	
	if request.method == "POST":# getting attendance after filter 
		medium_name = request.POST.get('medium_name')
		if medium_name=="":
		   medium_name="English" 
		class_name = request.POST.get('class_name')
		division_name = request.POST.get('division_name')
		month=request.POST.get('month')
		if month=="":
		    month=datetime.datetime.now().month

		data = StaffMaster.objects.values().filter(staff_medium_name=medium_name, staff_school_code=school_code)

		today=int(datetime.datetime.now().strftime("%d"))
		year = int(datetime.datetime.now().strftime("%Y"))
		mon = datetime.date(1900, int(month), 1).strftime('%B')
		req = {"medium_name": medium_name, "class_name": class_name, "division_name": division_name,"month":mon, "year":year}
		d.update(req)
		mahina=datetime.datetime.now().month
		for i in data:
			if mahina==int(month):
				for j in range(1,today+1):
					date = f"{year}-{month}-{j}"

					attn = Attendance.objects.values().filter(rf_id=i["staff_card_number"] ,school_code=school_code, date=date)

					if (date[5:9]) == "8-15":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
					elif (date[5:9]) == "1-26":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

					elif school_holiday.objects.values().filter(date=date,school_code=school_code).count():
						i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


					elif attn.first() is not None:
						i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" + str(attn.first()["intime"]),
								  f"{j}out": "OUT:-" + str(attn.first()["outtime"])})

					elif pydate(date).strftime("%a") == "Sun":
						i.update({j: 'fas fa-home',f"{j}in":"sunday"})


					else:
						i.update({j: 'fas fa-times text-danger'})

			elif month == "02" and year % 4 == 0:
				for j in range(1, 30):
					date = f"{year}-{month}-{j}"

					attn = Attendance.objects.values().filter(rf_id=i["staff_card_number"] ,school_code=school_code, date=date)

					if (date[5:9]) == "8-15":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
					elif (date[5:9]) == "1-26":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

					elif school_holiday.objects.values().filter(date=date,school_code=school_code).count():
						i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


					elif attn.first() is not None:
						i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" + str(attn.first()["intime"]),
								  f"{j}out": "OUT:-" + str(attn.first()["outtime"])})

					elif pydate(date).strftime("%a") == "Sun":
						i.update({j: 'fas fa-home', f"{j}in": "sunday"})
					# holiday=fas fa-smile

					else:
						i.update({j: 'fas fa-times text-danger'})


			elif month=="02":
				for j in range(1,29):
					date = f"{year}-{month}-{j}"

					attn = Attendance.objects.values().filter(rf_id=i["staff_card_number"] ,school_code=school_code, date=date)

					if (date[5:9]) == "8-15":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
					elif (date[5:9]) == "1-26":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

					elif school_holiday.objects.values().filter(date=date,school_code=school_code).count():
						i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


					elif attn.first() is not None:
						i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" + str(attn.first()["intime"]),
								  f"{j}out": "OUT:-" + str(attn.first()["outtime"])})

					elif pydate(date).strftime("%a") == "Sun":
						i.update({j: 'fas fa-home', f"{j}in": "sunday"})
						#holiday=fas fa-smile


					else:
						i.update({j: 'fas fa-times text-danger'})







			elif month in ["04","06","07" "09","11"]:
				for j in range(1,31):
					date = f"{year}-{month}-{j}"

					attn = Attendance.objects.values().filter(rf_id=i["staff_card_number"] ,school_code=school_code, date=date)

					if (date[5:9]) == "8-15":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
					elif (date[5:9]) == "1-26":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

					elif school_holiday.objects.values().filter(date=date,school_code=school_code).count():
						i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


					elif attn.first() is not None:
						i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" +str(attn.first()["intime"]),f"{j}out": "OUT:-" +str(attn.first()["outtime"])})
					elif pydate(date).strftime("%a") == "Sun":
						i.update({j: 'fas fa-home', f"{j}in": "sunday"})


					else:
						i.update({j: 'fas fa-times text-danger'})



			else:
				for j in range(1,32):
					date = f"{year}-{month}-{j}"

					attn = Attendance.objects.values().filter(rf_id=i["staff_card_number"] ,school_code=school_code, date=date)

					if (date[5:9]) == "8-15":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
					elif (date[5:9]) == "1-26":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

					elif school_holiday.objects.values().filter(date=date,school_code=school_code).count():
						i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


					elif attn.first() is not None:
						i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" + str(attn.first()["intime"]),
								  f"{j}out": "OUT:-" + str(attn.first()["outtime"])})

					elif pydate(date).strftime("%a") == "Sun":
						i.update({j: 'fas fa-home', f"{j}in": "sunday"})


					else:
						i.update({j: 'fas fa-times text-danger'})
		d.update({"data": data})
	return render(request, 'SchoolDesign/staff-attendance.html',d)






@login_required(login_url='login')
def  notice_board(request):
	school_code=request.user.last_name

	x = notice_board_school.objects.values().filter(school_code=school_code).order_by('-created_on')
	d={'x': x}
	time1=datetime.datetime.now()
	for i in x:
		diff=time1-i["created_on"].replace(tzinfo=None)

		if diff.days==0 and diff.seconds//60<60:
			i.update({"diff":str(diff.seconds//60)+"min ago"})
			i.update({"status": "New"})
		if diff.days==0 and diff.seconds//60>60:
			i.update({"diff":str(diff.seconds//3600)+"hours ago"})
			i.update({"status": "New"})
		if diff.days>0:
			if diff.days==1:
				i.update({"diff":str(diff.days)+"day ago"})
				i.update({"status": "New"})
			else:
				i.update({"diff": str(diff.days) + "days ago"})


	if request.method == 'POST':
		Title = request.POST.get('title')
		Details = request.POST.get('details')
		Posted_by = request.POST.get('posted_by')
		Date= request.POST.get('date')
		data= notice_board_school(school_code=school_code,Title=Title,Posted_by=Posted_by,Date=datetime.datetime.strptime(Date, "%d/%m/%Y"),Details=Details)
		# notice_board_school.update_or_create(school_code=school_code,Title=Title,Posted_by=Posted_by,Date=pydate(Date),Details=Details)
		data.save()
		messages.success(request,"Successfully Created")
		return redirect('notice_board')
	return render(request, 'SchoolDesign/notice-board.html',d)



@login_required(login_url='login')
def  notice_board_delete(request,id):
	school_code = request.user.last_name
	notice = notice_board_school.objects.get(notice_id=id)
	notice.delete()
	messages.success(request, "Successfully Deleted")
	return redirect('notice_board')





@login_required(login_url='login')
def transport(request):
	school_code=request.user.last_name
	x =School_Transport.objects.values().filter(school_code=school_code)
	d={'x': x}
	if request.method == 'POST':
		Route_Name= request.POST.get('Route_Name')
		Vehicle_Number= request.POST.get('Vehicle_Number')
		Driver_Name = request.POST.get('Driver_Name')
		License_Number= request.POST.get('License_Number')
		Phone_Number= request.POST.get('Phone_Number')
		print(Route_Name,Vehicle_Number,Driver_Name,License_Number,Phone_Number)
		data=School_Transport(Route_Name=Route_Name,Vehicle_Number=Vehicle_Number,Driver_Name=Driver_Name,License_Number=License_Number,Phone_Number=Phone_Number,school_code=school_code)
		data.save()
		messages.success(request, "Successfully Created")
		return redirect('transport')
	return render(request, 'SchoolDesign/transport.html',d)


@login_required(login_url='login')
def  transport_delete(request,id):
	school_code = request.user.last_name
	transport = School_Transport.objects.get(transport_id=id)
	transport.delete()
	messages.success(request, "Successfully Deleted")
	return redirect('transport')

@login_required(login_url='login')
def library(request):
	school_code = request.user.last_name
	classes = ClassMaster.objects.values('class_name').filter(school_code=school_code)
	n=1
	x = school_library.objects.values().filter(school_code=school_code)
	for i in x:
		if n<10:
	         i.update({'index':'0'+str(n)})
		else:
			i.update({'index':n})
		n+=1
	d = {'classes': classes,"x":x}
	print(d)
	if request.method == 'POST':
		Book_Name= request.POST.get('Book_Name')
		Subject= request.POST.get('Subject')
		Writter_Name = request.POST.get('Writter_Name')
		Class= request.POST.get('Class')
		print(Book_Name,Subject,Writter_Name,Class)
		data=school_library(Book_Name=Book_Name,Subject=Subject,Writter_Name=Writter_Name,Class=Class,school_code=school_code)
		data.save()
		messages.success(request, "Successfully Created")
		return redirect('library')
	return render(request, 'SchoolDesign/add-book.html',d)



@login_required(login_url='login')
def all_book(request):
	school_code = request.user.last_name
	n=1
	x = school_library.objects.values().filter(school_code=school_code)
	for i in x:
		if n<10:
	         i.update({'index':'0'+str(n)})
		else:
			i.update({'index':n})
		n+=1
	return render(request, 'SchoolDesign/all-book.html',{"x":x})




@login_required(login_url='login')
def  book_delete(request,id):
	school_code = request.user.last_name
	book = school_library.objects.get(school_library_id=id,school_code=school_code)
	book.delete()
	messages.success(request, "Successfully Deleted")
	return redirect('all_book')




@login_required(login_url='login')
def alot_rfid(request):
	data={}

	if request.method == 'POST':
		user_name = request.POST.get('username')

		if User.objects.filter(groups=4, username=user_name).exists():
			data = StudentMaster.objects.values().filter(user_name=user_name)
			data.update(student_card_number=read_rfid())
			for i in data:
				i.update(ParentsMaster.objects.values().filter(user_id=i["parents_id"]).first())
		elif User.objects.filter(groups=3, username=user_name).exists():
			data = StaffMaster.objects.values().filter(staff_user_name=user_name)
			data.update(staff_card_number=read_rfid())

		return render(request, 'SchoolDesign/alotrfid.html', {"data": data})

	return render(request,'SchoolDesign/alotrfid.html',{"data": data})


def commands(request,user_contact):
	print(user_contact)
	user_commands=user_command.objects.values().filter(user_contact=user_contact).last()
	

	print(user_commands,"******&&&&&&&&&&&*******************")

	return render(request, 'SchoolDesign/user_commands.html', {"user_commands": user_commands})


def submit_commands(request):
	user="9060555656"
	if 'Bulb' in request.POST:

		if 'on' == request.POST.get('Bulb'):
			print("**************Bulb***********",request.POST.get('Bulb'))
			user_commands=user_command.objects.filter(user_contact=user)
			user_commands.update(pin_no="18")
			user_commands.update(command="on")
			print(user_commands)
			#user_commands.save()
		elif 'off' == request.POST.get('Bulb'):
			print("&&&&&&&&&&&&&&&&&&Bulb&&&&&&&&&&&&&&&&&",request.POST.get('Bulb'))
			user_commands=user_command.objects.filter(user_contact=user)
			user_commands.update(pin_no="18")
			user_commands.update(command="off")
			print(user_commands)
	elif 'Fan' in request.POST: 

		if 'on' == request.POST.get('Fan'):
			print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$Fan$$$$$$$$$$",request.POST.get('Fan'))
			user_commands=user_command.objects.filter(user_contact=user)
			user_commands.update(pin_no="19")
			user_commands.update(command="on")
			print(user_commands)
			#user_commands.save()
		elif 'off' == request.POST.get('Fan'):
			print("############################Fan##############",request.POST.get('Fan'))
			user_commands=user_command.objects.filter(user_contact=user)
			user_commands.update(pin_no="19")
			user_commands.update(command="off")
			print(user_commands)

	return render(request, 'SchoolDesign/submit_user_commands.html')

@login_required(login_url='login')
def add_holiday(request):
	school_code = request.user.last_name
	x = school_holiday.objects.values().filter(school_code=school_code).order_by('-created_on')
	if request.method == 'POST':
		holiday_Name = request.POST.get('holiday_Name')
		date = request.POST.get('date')
		details=request.POST.get('details')
		print(holiday_Name,date,school_code)
		data = school_holiday(holiday_name=holiday_Name, date=datetime.datetime.strptime(date, "%d/%m/%Y"),
							  school_code=school_code,details=details)
		data.save()
		messages.success(request, "Successfully Created")
		return redirect('add_holiday')
	return render(request,'SchoolDesign/add-holiday.html',{"x":x})




@login_required(login_url='login')
def view_holidays(request):
	school_code = request.user.last_name
	x=school_holiday.objects.values().filter(school_code=school_code).order_by('-created_on')
	return render(request,'SchoolDesign/view-holiday.html',{"x":x})





@login_required(login_url='login')
def holiday_delete(request,id):
	school_code = request.user.last_name
	holiday = school_holiday.objects.get(school_holiday_id=id)
	holiday.delete()
	messages.success(request, "Successfully Deleted")
	return redirect('add_holiday')





@login_required(login_url='login')
def kids_attendence(request):
	attendance_update()
	school_code = request.user.last_name
	d={}

	if request.method == "POST":
		month=request.POST.get('month')
		x = ParentsMaster.objects.get(Parents_mobile=request.user.username)
		data  = StudentMaster.objects.values().filter(parents_id=x.user_id)
		today=int(datetime.datetime.now().strftime("%d"))
		year = int(datetime.datetime.now().strftime("%Y"))
		print(year//4,"#####################")
		mon = datetime.date(1900, int(month), 1).strftime('%B')
		req = {"month":mon, "year":year}
		print(req)
		d.update(req)
		print(d)
		mahina=datetime.datetime.now().month
		for i in data:
			if mahina == int(month):
				for j in range(1, today + 1):
					date = f"{year}-{month}-{j}"

					attn = Attendance.objects.values().filter(rf_id=i["student_card_number"], date=date)

					if (date[5:9]) == "8-15":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
					elif (date[5:9]) == "1-26":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

					elif school_holiday.objects.values().filter(date=date).count():
						i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


					elif attn.first() is not None:
						i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" + str(attn.first()["intime"]),
								  f"{j}out": "OUT:-" + str(attn.first()["outtime"])})

					elif pydate(date).strftime("%a") == "Sun":
						i.update({j: 'fas fa-home', f"{j}in": "sunday"})


					else:
						i.update({j: 'fas fa-times text-danger'})


			elif month == "02" and year % 4 == 0:
				for j in range(1, 30):
					date = f"{year}-{month}-{j}"

					attn = Attendance.objects.values().filter(rf_id=i["student_card_number"], date=date)

					if (date[5:9]) == "8-15":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
					elif (date[5:9]) == "1-26":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

					elif school_holiday.objects.values().filter(date=date).count():
						i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


					elif attn.first() is not None:
						i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" + str(attn.first()["intime"]),
								  f"{j}out": "OUT:-" + str(attn.first()["outtime"])})

					elif pydate(date).strftime("%a") == "Sun":
						i.update({j: 'fas fa-home', f"{j}in": "sunday"})
					# holiday=fas fa-smile

					else:
						i.update({j: 'fas fa-times text-danger'})

			elif month == "02":
				for j in range(1, 29):
					date = f"{year}-{month}-{j}"

					attn = Attendance.objects.values().filter(rf_id=i["student_card_number"], date=date)

					if (date[5:9]) == "8-15":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
					elif (date[5:9]) == "1-26":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

					elif school_holiday.objects.values().filter(date=date).count():
						i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


					elif attn.first() is not None:
						i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" + str(attn.first()["intime"]),
								  f"{j}out": "OUT:-" + str(attn.first()["outtime"])})

					elif pydate(date).strftime("%a") == "Sun":
						i.update({j: 'fas fa-home', f"{j}in": "sunday"})
					# holiday=fas fa-smile

					else:
						i.update({j: 'fas fa-times text-danger'})


			elif month in ["04", "06", "07", "09", "11"]:
				for j in range(1, 31):
					date = f"{year}-{month}-{j}"

					attn = Attendance.objects.values().filter(rf_id=i["student_card_number"], date=date)

					if (date[5:9]) == "8-15":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
					elif (date[5:9]) == "1-26":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

					elif school_holiday.objects.values().filter(date=date).count():
						i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


					elif attn.first() is not None:
						i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" + str(attn.first()["intime"]),
								  f"{j}out": "OUT:-" + str(attn.first()["outtime"])})
					elif pydate(date).strftime("%a") == "Sun":
						i.update({j: 'fas fa-home', f"{j}in": "sunday"})


					else:
						i.update({j: 'fas fa-times text-danger'})



			else:
				for j in range(1, 32):
					date = f"{year}-{month}-{j}"

					attn = Attendance.objects.values().filter(rf_id=i["student_card_number"], date=date)

					if (date[5:9]) == "8-15":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
					elif (date[5:9]) == "1-26":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

					elif school_holiday.objects.values().filter(date=date).count():
						i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


					elif attn.first() is not None:
						i.update({j: 'fas fa-check text-success', f"{j}in": "IN:-" + str(attn.first()["intime"]),
								  f"{j}out": "OUT:-" + str(attn.first()["outtime"])})

					elif pydate(date).strftime("%a") == "Sun":
						i.update({j: 'fas fa-home', f"{j}in": "sunday"})


					else:
						i.update({j: 'fas fa-times text-danger'})
		d.update({"data": data})
	return render(request, 'parents_kids_attendance.html',d)






@login_required(login_url='login')
def my_attendence(request):
	attendance_update()
	school_code = request.user.last_name
	d = {}

	if request.method == "POST":
		month = request.POST.get('month')
		if User.objects.filter(groups=3, username=request.user.username).exists():
			data = StaffMaster.objects.values().filter(staff_user_name=request.user.username)
		else:
			data=StudentMaster.objects.values().filter(user_name=request.user.username)
		today = int(datetime.datetime.now().strftime("%d"))
		year = int(datetime.datetime.now().strftime("%Y"))
		mon = datetime.date(1900, int(month), 1).strftime('%B')
		req = {"month": mon, "year": year}
		d.update(req)
		mahina = datetime.datetime.now().month
		for i in data:
			if mahina == int(month):
				for j in range(1, today + 1):
					date = f"{year}-{month}-{j}"
					if User.objects.filter(groups=3, username=request.user.username).exists():
						attn = Attendance.objects.values().filter(rf_id=i["staff_card_number"], date=date)
					else:
						attn = Attendance.objects.values().filter(rf_id=i["student_card_number"], date=date)
					if (date[5:9]) == "8-15":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
					elif (date[5:9]) == "1-26":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

					elif school_holiday.objects.values().filter(date=date).count():
						i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


					elif attn.first() is not None:
						i.update({j: 'fas fa-check text-success', f"{j}in": str(attn.first()["intime"]),
								  f"{j}out": str(attn.first()["outtime"])})

					elif pydate(date).strftime("%a") == "Sun":
						i.update({j: 'fas fa-home', f"{j}in": "sunday"})


					else:
						i.update({j: 'fas fa-times text-danger'})

			elif month == "02" and year % 4 == 0:
				for j in range(1, 30):
					date = f"{year}-{month}-{j}"

					if User.objects.filter(groups=3, username=request.user.username).exists():
						attn = Attendance.objects.values().filter(rf_id=i["staff_card_number"], date=date)
					else:
						attn = Attendance.objects.values().filter(rf_id=i["student_card_number"], date=date)

					if (date[5:9]) == "8-15":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
					elif (date[5:9]) == "1-26":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

					elif school_holiday.objects.values().filter(date=date).count():
						i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


					elif attn.first() is not None:
						i.update({j: 'fas fa-check text-success', f"{j}in": str(attn.first()["intime"]),
								  f"{j}out": str(attn.first()["outtime"])})

					elif pydate(date).strftime("%a") == "Sun":
						i.update({j: 'fas fa-home', f"{j}in": "sunday"})
					# holiday=fas fa-smile

					else:
						i.update({j: 'fas fa-times text-danger'})


			elif month == "02":
				for j in range(1, 29):
					date = f"{year}-{month}-{j}"

					if User.objects.filter(groups=3, username=request.user.username).exists():
						attn = Attendance.objects.values().filter(rf_id=i["staff_card_number"], date=date)
					else:
						attn = Attendance.objects.values().filter(rf_id=i["student_card_number"], date=date)

					if (date[5:9]) == "8-15":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
					elif (date[5:9]) == "1-26":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

					elif school_holiday.objects.values().filter(date=date).count():
						i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


					elif attn.first() is not None:
						i.update({j: 'fas fa-check text-success', f"{j}in": str(attn.first()["intime"]),
								  f"{j}out": str(attn.first()["outtime"])})

					elif pydate(date).strftime("%a") == "Sun":
						i.update({j: 'fas fa-home', f"{j}in": "sunday"})
					# holiday=fas fa-smile

					else:
						i.update({j: 'fas fa-times text-danger'})





			elif month in ["04", "06", "07", "09", "11"]:
				for j in range(1, 31):
					date = f"{year}-{month}-{j}"

					if User.objects.filter(groups=3, username=request.user.username).exists():
						attn = Attendance.objects.values().filter(rf_id=i["staff_card_number"], date=date)
					else:
						attn = Attendance.objects.values().filter(rf_id=i["student_card_number"], date=date)

					if (date[5:9]) == "8-15":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
					elif (date[5:9]) == "1-26":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

					elif school_holiday.objects.values().filter(date=date).count():
						i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


					elif attn.first() is not None:
						i.update({j: 'fas fa-check text-success', f"{j}in": str(attn.first()["intime"]),
								  f"{j}out": str(attn.first()["outtime"])})
					elif pydate(date).strftime("%a") == "Sun":
						i.update({j: 'fas fa-home', f"{j}in": "sunday"})


					else:
						i.update({j: 'fas fa-times text-danger'})



			else:
				for j in range(1, 32):
					date = f"{year}-{month}-{j}"

					if User.objects.filter(groups=3, username=request.user.username).exists():
						attn = Attendance.objects.values().filter(rf_id=i["staff_card_number"], date=date)
					else:
						attn = Attendance.objects.values().filter(rf_id=i["student_card_number"], date=date)

					if (date[5:9]) == "8-15":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy Independance day"})
					elif (date[5:9]) == "1-26":
						i.update({j: 'fas fa-flag', f"{j}in": "Happy republic Day"})

					elif school_holiday.objects.values().filter(date=date).count():
						i.update({j: 'fas fa-home', f"{j}in": "Holiday"})


					elif attn.first() is not None:
						i.update({j: 'fas fa-check text-success', f"{j}in": str(attn.first()["intime"]),
								  f"{j}out": str(attn.first()["outtime"])})

					elif pydate(date).strftime("%a") == "Sun":
						i.update({j: 'fas fa-home', f"{j}in": "sunday"})


					else:
						i.update({j: 'fas fa-times text-danger'})
		d.update({"data": data})
	return render(request, 'my-attendance.html', d)






from django import template
from django.contrib.auth.models import Group
register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)

    return True if group in user.groups.all() else False






#views of api*********************************************************

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from school.models import attendance_api,gpsrestapi,Bikeapi,Pumpapi
from school.serializer import attendanceSerializer,gpsrestapiSerializer,BikeapiSerializer,pumpapiSerializer,school_machine_apiSerializer,BusapiSerializer

class attendanceCRUDCBV(ModelViewSet):

    queryset = attendance_api.objects.all()
    serializer_class = attendanceSerializer


class gpsrestapiCRUDCBV(ModelViewSet):

    queryset = gpsrestapi.objects.all()
    serializer_class = gpsrestapiSerializer


class BikeapiCRUDCBV(ModelViewSet):

    queryset = Bikeapi.objects.all()
    serializer_class = BikeapiSerializer   
    
    

class BusapiCRUDCBV(ModelViewSet):

    queryset = Busapi.objects.all()
    serializer_class = BusapiSerializer 
    
class school_machine_apiCRUDCBV(ModelViewSet):

    queryset = school_machine_api.objects.all()
    serializer_class = school_machine_apiSerializer      
    
    
class pumpapiCRUDCBV(ModelViewSet):

    queryset = Pumpapi.objects.all()
    serializer_class = pumpapiSerializer  
    
    
    
    
from django.shortcuts import render
from json import dumps



#send data from view.py to html javascript testing
#
@login_required(login_url='login')
def load_class(request):
	global medium_name
	school_code = request.user.last_name
	medium_name = request.GET.get('medium_name')
	# class_name = request.GET.get('class_name')
	class_name=ClassMaster.objects.values().filter(medium_name=medium_name,school_code=school_code)

	return render(request, 'load-class.html',{"class_name":class_name})

@login_required(login_url='login')
def load_division(request):
	global class_name
	school_code = request.user.last_name

	class_name = request.GET.get('class_name')


	Division=DivisionMaster.objects.values().filter(medium_name=medium_name,school_code=school_code,class_name=class_name)


	return render(request, 'load-class.html',{"Division":Division})



@login_required(login_url='login')
def load_student(request):
	school_code = request.user.last_name
	section_name = request.GET.get('section_name')
	students = StudentMaster.objects.values().filter(medium_name=medium_name, school_code=school_code, class_name=class_name, division_name = section_name)
	print(students)
	return render(request, 'load-class.html',{"students":students})




@login_required(login_url='login')
def msg(request):
	school_code = request.user.last_name
	date = datetime.datetime.now()
	if request.method == "POST":
		medium_name = request.POST.get('medium_name')
		class_name = request.POST.get('class_name')
		division_name = request.POST.get('division_name')
		user_name= request.POST.get('student')
		message=request.POST.get('message')
		parent_id = StudentMaster.objects.values().filter(medium_name=medium_name, school_code=school_code,class_name=class_name, division_name=division_name,user_name=user_name).first()["parents_id"]
		parents_number=ParentsMaster.objects.get(pk=parent_id).Parents_mobile


		#sendSMS(message,parents_number)
		status = sendsms(request, school_code, date, message, parents_number)
		if status is not None:
			if status[0]:
				messages.success(request, f"Message send successfully ! Remaining message : {status[1]} ")

		return redirect('msg')
		# messages.success(request, "sent successfully")
		# return redirect('msg')
	mediums = MediumMaster.objects.values('medium_name').filter(school_code=school_code)
	return render(request,'SchoolDesign/messaging.html',{"mediums":mediums,})





@login_required(login_url='login')
def absent_Student(request):
	school_code = request.user.last_name
	students = StudentMaster.objects.values().filter(school_code=school_code)
	mediums = MediumMaster.objects.values('medium_name').filter(school_code=school_code)
	d={"mediums":mediums}
	date = datetime.datetime.now()


	if request.method == "POST":
		medium_name = request.POST.get('medium_name')
		ch = request.POST.getlist('checks[]')

		print(medium_name,ch)
		students = StudentMaster.objects.values().filter(school_code=school_code,medium_name=medium_name)
		n = 1
		x = school_library.objects.values().filter(school_code=school_code)

		for i in students:
			if Attendance.objects.values().filter(rf_id=i["student_card_number"], date="2020-08-29").exists() == False:
				try:
					i.update({"father_mobile_number": ParentsMaster.objects.get(pk=i["parents_id"]).Parents_mobile})

				except:pass
				if n < 10:
					i.update({'index': '0' + str(n)})
				else:
					i.update({'index': n})
				n += 1


		#absentmsg(ch)

		absent_msg(request, school_code, date, ch)

		d.update({"x": students})

		return render(request, 'absent_student_msg.html', d)

		# d.update({"x": students})
		# print(ch)
		# # messages.success(request, "Successfully recieved")
		#
		# return render(request, 'absent_Student_msg.html', d)

	# messages.success(request, "data not recieved ")
	return render(request, 'absent_student_msg.html', d)



@login_required(login_url='login')
def change_password(request):
	school_code = request.user.last_name
	if request.method == "POST":
		username = request.POST.get('Username')
		New_Password = request.POST.get('New_Password')
		Confirm_New_Password = request.POST.get('Confirm_New_Password')
		if username==request.user.username:
			if Confirm_New_Password==New_Password:
				u, created = User.objects.get_or_create(username=username, is_staff=1, is_active=1, first_name=request.user.first_name,last_name=school_code,email=request.user.email)
				u.set_password(Confirm_New_Password)
				u.save()
				if User.objects.filter(groups=2, username=request.user.username).exists():  # admin
					x = SchoolMaster.objects.values().filter(school_code=school_code)
					x.update(password=Confirm_New_Password)
					#print("password changed in SchoolMaster)******************admin*********")
				elif User.objects.filter(groups=5, username=request.user.username).exists():  # parents
					x = ParentsMaster.objects.values().filter(Parents_mobile=username)
					x.update(password=Confirm_New_Password)
					print("password changed )*****parents**********parents************")
				elif User.objects.filter(groups=4, username=request.user.username).exists():  # student
					x = StudentMaster.objects.values().filter(user_name=username)
					x.update(password=Confirm_New_Password)
					print("password changed )***ParentsMaster***************student*********")
				elif User.objects.filter(groups=3, username=request.user.username).exists():  # teacher
					x = StaffMaster.objects.values().filter(staff_user_name=username)
					x.update(password=Confirm_New_Password)
					print("password changed )*StaffMaster*****************teacher*********")




				messages.success(request, "Successfully Password changed!!!")
			else:
				messages.info(request, "New password does't match the confirm password")
				return redirect('change_password')
		else:
			messages.info(request, "Unauthenticated username!!!")
	return render(request, 'change-password.html')




def forget_password(request):
	return render(request, 'Forget-password.html')
	
	
@login_required(login_url='login')
def student_id_view(request):
    school_code = request.user.last_name
    student=""
    #if request.method == "POST":
        #user_name = request.POST.get('user_name')
    #school_code = UserMaster.objects.get(user_name=username).school_code

    student=StudentMaster.objects.all().filter(school_code=school_code)
    #student=StudentMaster.objects.values().filter(school_code=school_code)
    #for i in student:
    #    i.update(ParentsMaster.objects.values().filter(user_id=i["parents_id"]).first())
    return render(request,"SchoolDesign/student_id_view.html",{"students":student})

@login_required(login_url='login')
def student_idcard(request,id):
    school_code = request.user.last_name
    student=""
    #if request.method == "POST":
        #user_name = request.POST.get('user_name')
    #school_code = UserMaster.objects.get(user_name=username).school_code
    school_info=SchoolMaster.objects.get(school_code=school_code)
    student=StudentMaster.objects.all().filter(school_code=school_code)
    student=StudentMaster.objects.values().filter(school_code=school_code)
    student_html_file="SchoolDesign/id_card_view/student_id_view"+str(id)+".html"
    for i in student:
        i.update(ParentsMaster.objects.values().filter(user_id=i["parents_id"]).first())
    return render(request,student_html_file,{"data":student,"school_info":school_info})
    
@login_required(login_url='login')
def staff_id_view(request):
	school_code = request.user.last_name
	mediums = MediumMaster.objects.values('medium_name').filter(school_code=school_code)
	dictonary = {"mediums": mediums,}

	if 1 == 1:
		#medium_name = request.POST.get('medium')
		#class_name = request.POST.get('class')
		#division_name = request.POST.get('section')
		n = 1
		#data = StaffMaster.objects.values().filter(staff_medium_name=medium_name,staff_school_code=school_code).order_by('staff_class_name','staff_division_name')
		data = StaffMaster.objects.values().filter(staff_school_code=school_code).order_by('staff_class_name','staff_division_name')


		for i in data:
			if n < 10:
				i.update({'index': '0' + str(n)})
			else:
				i.update({'index': n})
			n += 1
		d = {"data": data}
		dictonary.update(d)

	return render(request,'SchoolDesign/id_card_view/staff_id_view1.html',dictonary)

@login_required(login_url='login')
def staff_id_view3(request):
	school_code = request.user.last_name
	mediums = MediumMaster.objects.values('medium_name').filter(school_code=school_code)
	dictonary = {"mediums": mediums,}

	if 1 == 1:
		#medium_name = request.POST.get('medium')
		#class_name = request.POST.get('class')
		#division_name = request.POST.get('section')
		n = 1
		#data = StaffMaster.objects.values().filter(staff_medium_name=medium_name,staff_school_code=school_code).order_by('staff_class_name','staff_division_name')
		data = StaffMaster.objects.values().filter(staff_school_code=school_code).order_by('staff_class_name','staff_division_name')


		for i in data:
			if n < 10:
				i.update({'index': '0' + str(n)})
			else:
				i.update({'index': n})
			n += 1
		d = {"data": data}
		dictonary.update(d)

	return render(request,'SchoolDesign/id_card_view/staff_id_view3.html',dictonary)


@login_required(login_url='login')
def Edit_student(request,id):
    school_code = request.user.last_name
    mediums=MediumMaster.objects.values('medium_name').filter(school_code=school_code)
    std=StudentMaster.objects.get(pk=id)
    print(std.date_of_birth)
    std_next=StudentMaster.objects.filter(school_code=school_code, pk=id).order_by('pk').first()
    parents=ParentsMaster.objects.get(pk=std.parents_id)

    classes = ClassMaster.objects.values('class_name').filter(medium_name=std.medium_name,school_code=school_code)

    division = DivisionMaster.objects.values('division_name').filter(medium_name=std.medium_name,school_code=school_code,class_name=std.class_name)
    d = {"mediums": mediums, "classes": classes, "division": division,"std_next":std_next}

    d.update({"std":std})
    d.update({"parents": parents})
    if request.method == 'POST':

        std.Full_name = request.POST.get('Full_name').strip()
        std.gender = request.POST.get('gender').strip()
        std.date_of_birth = request.POST.get('dob').strip()
        std.email = request.POST.get('email').strip()
        std.mobile = request.POST.get('mobile').strip()
        std.blood_group = request.POST.get('blood_group').strip()
        std.reservation = request.POST.get('reservation').strip()
        std.medium_name = request.POST.get('medium').strip()
        std.class_name = request.POST.get('class').strip()
        std.division_name = request.POST.get('section').strip()
        std.admission_no = request.POST.get('addmission_no').strip()
        try:
            stu_image=request.FILES['image']
            if std.image!=stu_image:
                std.image.delete()
                std.image =stu_image
            else:
                std.image =stu_image
        except:
            try:
                std.image =stu_image
            except:pass
        
        print(std.image,"0000000000000000000000000000000")
        student_user = User.objects.get(pk=std.pk)
        student_user.username =std.Full_name.split()[0]+ str(std.pk)
        student_user.first_name=std.Full_name
        student_user.email=std.email
        std.user_name=student_user.username
        std.save()
        student_user.save()

        parents.fathername = request.POST.get('fathername').strip()
        parents.mothername = request.POST.get('mothername').strip()
        parents.father_occupation = request.POST.get('father_occupation').strip()
        parents.mother_occupation = request.POST.get('mother_occupation').strip()
        parents.Parents_Religion = request.POST.get('Religion').strip()
        parents.Parents_email = request.POST.get('parents_email').strip()
        parents.Parents_mobile = request.POST.get('parents_mobile').strip()
        parents.Parents_Address = request.POST.get('Address').strip()
        parents.Parents_city = request.POST.get('city').strip()
        parents.Parents_pincode = request.POST.get('pincode').strip()

        parents_user=User.objects.get(pk=std.parents_id)
        try:
            parents_user.username=parents.Parents_mobile
            parents_user.email = parents.Parents_email
            parents_user.first_name = parents.fathername
            parents_user.save()
            parents.save()
            messages.success(request, "successfully saved!!")

        except:
            messages.info(request, "parents mobile already exist!!!")

        return redirect(f'/Edit_student/{id}')
    return render(request, 'Edit_student.html',d)




@login_required(login_url='login')
def Edit_staff(request, id):
	school_code = request.user.last_name
	staff=StaffMaster.objects.get(pk=id)
	mediums = MediumMaster.objects.values('medium_name').filter(school_code=school_code)
	classes = ClassMaster.objects.values('class_name').filter(medium_name=staff.staff_medium_name,school_code=staff.staff_school_code)
	print(classes)
	division = DivisionMaster.objects.values('division_name').filter(medium_name=staff.staff_medium_name,school_code=staff.staff_school_code,class_name=staff.staff_class_name)
	print(division)
	d = {"mediums": mediums, "classes": classes, "division": division}
	d.update({"staff": staff})
	if request.method == 'POST':
		staff.staff_First_name = request.POST.get('First_name')
		staff.staff_Last_name = request.POST.get('Last_name')
		staff.staff_gender = request.POST.get('gender')
		staff.staff_date_of_birth = request.POST.get('dob')
		staff.staff_email = request.POST.get('email')
		staff.staff_mobile = request.POST.get('mobile')
		staff.staff_Address = request.POST.get('Address')
		staff.staff_city = request.POST.get('city')
		staff.staff_pincode = request.POST.get('pincode')
		staff.staff_blood_group = request.POST.get('blood_group')
		staff.staff_Religion = request.POST.get('Religion')
		staff.staff_qualification = request.POST.get('qualification')
		staff.staff_medium_name = request.POST.get('medium')
		staff.staff_class_name = request.POST.get('class')
		staff.staff_division_name = request.POST.get('section')
		# staff.staff_subject = request.POST.get('subject')
		try:
			staff.staff_image = request.FILES['image']
		except:pass
		try:
			staff_user = User.objects.get(pk=staff.pk)
			staff_user.username = staff.staff_email
			staff_user.first_name = staff.staff_First_name
			staff_user.email = staff.staff_email
			staff.user_name = staff_user.username
			staff_user.save()
			staff.save()
			messages.success(request, "successfully saved!!")
		except:
			messages.info(request, "Email already exist!!!")

		return redirect(f'/Edit_staff/{id}')


	return render(request, 'Edit-staff.html', d)


#@login_required(login_url='login')
def alot_verify(request, user, rfid, password):
    # user="rahul19"
    if password == "nilmani12345":
        data = {}
        rfid_data = rfid

        # user_name = request.POST.get('username')

        if User.objects.filter(groups=4, username=user).exists():
            data = StudentMaster.objects.values().filter(user_name=user)
            data.update(student_card_number=rfid_data)
            for i in data:
                i.update(ParentsMaster.objects.values().filter(user_id=i["parents_id"]).first())
                
            file='SchoolDesign/alot_verify_data.html'
        elif User.objects.filter(groups=3, username=user).exists():
            uuid=User.objects.filter(groups=3, username=user).first().id
            data = StaffMaster.objects.values().filter(staff_user=uuid)
            data.update(staff_card_number=rfid_data)
            file='SchoolDesign/alot_verify_data_staff.html'
        
    return render(request,file , {"data": data})


def bike_data_update(request, machine_id,):
    # user="rahul19"
   
    if "nilmani12345" == "nilmani12345":
        data = {}
       
        if bike_user.objects.values().filter(machine_id=machine_id).exists():
            data = bike_user.objects.values().filter(machine_id=machine_id)

          
                
            file='SchoolDesign/bike_data_update.html'
     
        
    return render(request,file , {"data": data})
       

def bike_save_update(request):
    # user="rahul19"
    # student,created=StudentMaster.objects.get_or_create(user_id=user_id,user_name=username,Full_name=Full_name,gender=gender,date_of_birth=date_of_birth,
				# Address=Address,city=city,pincode=pincode,school_code= school_code ,admission_no=admission_no,medium_name=medium_name,
				# class_name=class_name,division_name=division_name,parents_id=parents_user_id,image=image,password='12345')
				# student.save()
   
    if "nilmani12345" == "nilmani12345":
        data = {}
        num = Bikeapi.objects.values("machine_id").count()
        file='SchoolDesign/bike_data_update.html'
        for i in range(num):
            first = Bikeapi.objects.first()
            if first.machine_id is not None:
                #bike_user,created=bike_user.objects.get_or_create(machine_id =first.machine_id,
                bike_user_data,created=bike_user.objects.get_or_create(machine_id =first.machine_id)
                bike_user_data.name =first.name
                bike_user_data.mobile_no =first.mobile_no
                bike_user_data.vechile_no =first.vechile_no
                bike_user_data.address = first.address,
                bike_user_data.ssid= first.ssid
                bike_user_data.password=first.password
                bike_user_data.rf_id1=first.rf_id1
                bike_user_data.rf_id2=first.rf_id2
                bike_user_data.dealer=first.dealer
                bike_user_data.save()   
                first.delete()
            else:
                first.delete()
        # if bike_user.objects.values().filter(machine_id=machine_id).exists():
        #     data = bike_user.objects.values().filter(machine_id=machine_id
        #     file='SchoolDesign/bike_data_update.html'
     
        
    return render(request,file )

def add_school(request):
	if request.method == 'POST':
		school_name= request.POST.get('Schoolname')
		school_code = request.POST.get('schoolcode')
		registration_number= request.POST.get('registration_number')
		affiliated_by = request.POST.get('affiliated_by')
		email = request.POST.get('email')
		mobile = request.POST.get('mobile')
		address = request.POST.get('school_Address')
		city= request.POST.get('school_city')
		pincode = request.POST.get('school_pincode')
		#last_name=school_code,

		image = request.FILES['image']
		
		data=SchoolMaster(school_name=school_name,registration_number=registration_number,affiliated_by=affiliated_by,email=email,mobile=mobile,
						  address=address,city=city,pincode=pincode,image=image,password='12345')
		
		owner_name = request.POST.get('owner_name')
		owner_gender = request.POST.get('owner_gender')
		owner_date_of_birth = request.POST.get('owner_dob')
		owner_qualification = request.POST.get('owner_qualification')
		owner_email = request.POST.get('owner_email')
		owner_mobile = request.POST.get('owner_mobile')
		owner_address = request.POST.get('owner_Address')
		owner_city = request.POST.get('owner_city')
		owner_pincode = request.POST.get('owner_pincode')
		owner_image = request.FILES['owner_image']



		user, created = User.objects.get_or_create(username=email, is_staff=1, is_active=1,
												   first_name=school_name, 
												   email=owner_email)

		user.set_password("12345")
		user.save()
		data.save()
		user.groups.add(2)


		data1 = OwnerMaster(user_id=user.pk,owner_name=owner_name, owner_gender=owner_gender,owner_school_code=school_code, owner_date_of_birth=pydate(owner_date_of_birth),
							owner_qualification=owner_qualification, owner_email=owner_email, owner_mobile=owner_mobile,
							owner_address=owner_address, owner_city=owner_city, owner_pincode=owner_pincode, owner_image=owner_image)

		data1.save()



		medium_name1= request.POST.get('Medium1').capitalize().strip()
		data2=MediumMaster(school_code=school_code, medium_name=medium_name1)
		data2.save()

		medium_name2 = request.POST.get('Medium2').capitalize().strip()
		if medium_name2 is not None:
			data3 = MediumMaster(school_code=school_code, medium_name=medium_name2)
			data3.save()


		messages.success(request, "successfully saved!!")
		return redirect('/')



	return render(request, 'Add_School.html')
	
	
def add_school(request):
    if request.method == 'POST':
        school_name= request.POST.get('Schoolname') #-------------------required
        school_code = request.POST.get('schoolcode')
        registration_number= request.POST.get('registration_number')
        affiliated_by = request.POST.get('affiliated_by')
        email = request.POST.get('email')    #-------------------------required
        mobile = request.POST.get('mobile')  #------------------------required
        address = request.POST.get('school_Address')
        city= request.POST.get('school_city')
        pincode = request.POST.get('school_pincode')

		
        try:
            image = request.FILES['image']   #trying to get image means school image
        except:
            image=""
		
		
        owner_name = request.POST.get('owner_name') #--------------------required
        owner_gender = request.POST.get('owner_gender')
        try:                  #trying to get owner_date_of_birth
            owner_date_of_birth = request.POST.get('owner_dob')
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",type(owner_date_of_birth),len(owner_date_of_birth),owner_date_of_birth)
            if len(owner_date_of_birth)!=0 :
                print("convertingggggggggggggggggggggggggggggg")
                #owner_date_of_birth=pydate(owner_date_of_birth)
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        except:
            owner_date_of_birth=""
        owner_qualification = request.POST.get('owner_qualification')
        owner_email = request.POST.get('owner_email')
        owner_mobile = request.POST.get('owner_mobile')
        owner_address = request.POST.get('owner_Address')
        owner_city = request.POST.get('owner_city')
        owner_pincode = request.POST.get('owner_pincode')
        
        try:
            owner_image = request.FILES['owner_image']   #trying to get owner image
        except:
            owner_image=""
		
        #print(User.objects.filter(username=parents_mobile).exists())   last_name=school_code,
		
        try:
            owner_signature = request.FILES['owner_signature']#trying to get owner_signature
        except:
            owner_signature=""

        school_info=SchoolMaster.objects.filter(email=email)
        print(school_info)
        
        if school_info.exists(): # user_exist=1 means >0 means StudentMaster already exist
            #parents_user_id=parents_info.first().pk
            print("*************** StudentMaster already exist*********************************",owner_date_of_birth)
            #students_info=StudentMaster.objects.filter(Full_name=Full_name,school_code=school_code,parents_id=parents_user_id)
            school_name_exist=school_info.values().first()["school_name"]
            messages.info(request, school_name_exist+" already exist by the email "+email)
            print(school_info.values().first()["school_name"])
            return redirect('/add_school')

        #,registration_number=registration_number,affiliated_by=affiliated_by,address=address,city=city,pincode=pincode,image=image,password='12345',principal_sign_image=owner_signature
        else:#else means new email so we understand new school so going to add school 

            school_data, created=SchoolMaster.objects.get_or_create(school_name=school_name,email=email,mobile=mobile,registration_number=registration_number,affiliated_by=affiliated_by,address=address,city=city,pincode=pincode,image=image,password='12345',principal_sign_image=owner_signature)
            
            
            
            
            user, created = User.objects.get_or_create(username=email, is_staff=1, is_active=1,
            										first_name=school_name, 
            										email=owner_email)
            
            user.set_password("12345")
            user.save()
            school_data.save()
            new_school_code="sbsy"+str(school_data.pk)
            school_data.school_code=new_school_code
            school_data.save()
            print(new_school_code,"MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
            user.groups.add(2)
            user.last_name=new_school_code
            user.save()
            
            print("okkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
            data1 ,created= OwnerMaster.objects.get_or_create(user_id=user.pk,owner_name=owner_name, owner_gender=owner_gender,owner_school_code=new_school_code, owner_date_of_birth=owner_date_of_birth,
            					owner_qualification=owner_qualification, owner_email=owner_email, owner_mobile=owner_mobile,
            					owner_address=owner_address, owner_city=owner_city, owner_pincode=owner_pincode, owner_image=owner_image)
            
            
            
            
            data1.save()# owner details saving by data1
            medium_name1= request.POST.get('Medium1').capitalize().strip()   #trying to get medium1
            #medium_name2 = request.POST.get('Medium2').capitalize().strip()   ##trying to get medium2
            def add_class(medium_name): # function to add class up to 8 section A default
            	for class_name in range(1,9):
            		new_class = ClassMaster.objects.filter(school_code=new_school_code,medium_name=medium_name)
            		new_class.update_or_create(school_code=new_school_code,medium_name=medium_name, class_name=class_name)
            
            		new_section =  DivisionMaster.objects.filter(school_code=new_school_code,medium_name=medium_name, class_name=class_name,division_name="A")
            		new_section.update_or_create(school_code=new_school_code,medium_name=medium_name, class_name=class_name,division_name="A")

            if medium_name1 !="" and medium_name1 !="Both": # case1 means medium1 found also calling add_class function in this medium
                medium_name1=medium_name1
                data2=MediumMaster(school_code=new_school_code, medium_name=medium_name1)
                data2.save()
                print("medium 11111111111 found*************")
                add_class(medium_name1)
                print("class added up to 8 in ",medium_name1,"medium1")

			
            if medium_name1 =="Both" :# case2 means medium2 found also calling add_class up to 8 in this medium also
                medium_name2="English"
                data3 = MediumMaster(school_code=new_school_code, medium_name=medium_name2)
                data3.save()
                print("medium222222222found**********")
                add_class(medium_name2)
                print("class added up to 8 in ",medium_name2,"medium2")
                medium_name2="Hindi"
                data3 = MediumMaster(school_code=new_school_code, medium_name=medium_name2)
                data3.save()
                print("medium222222222found**********")
                add_class(medium_name2)
                print("class added up to 8 in ",medium_name2,"medium2")
                                
            if medium_name1=="": # case3 no medium found above then adding default medium English only if medium1 not found also medium2 not found
                medium_name3="English"
                data3 = MediumMaster(school_code=new_school_code, medium_name=medium_name3)
                data3.save()
                add_class(medium_name3)     # adding class upto 8 section A
                print("No medium found*****so****English added*")
                print("class added up to 8 in ",medium_name3,"medium3")
                

			
            print(medium_name1,medium_name2,"KKKKKKKKKKKKLLLLLLLLLLLLL")	
            messages.success(request, "New School Successfully Saved!!")
            print("dk((((((((((((((((((((((((((((")	
            return redirect('/add_school')
            

    
    return render(request, 'Add_School.html')	

	
def school_data_update(request, machine_no,):
    # user="rahul19"
   
    if "nilmani12345" == "nilmani12345":
        data = {}
       
        if school_machine_update.objects.values().filter(machine_no=machine_no).exists():
            data = school_machine_update.objects.values().filter(machine_no=machine_no)

          
                
            file='SchoolDesign/school_data_update.html'
     
        
    return render(request,file , {"data": data})
       

def school_save_update(request):
    # user="rahul19"
    # student,created=StudentMaster.objects.get_or_create(user_id=user_id,user_name=username,Full_name=Full_name,gender=gender,date_of_birth=date_of_birth,
				# Address=Address,city=city,pincode=pincode,school_code= school_code ,admission_no=admission_no,medium_name=medium_name,
				# class_name=class_name,division_name=division_name,parents_id=parents_user_id,image=image,password='12345')
				# student.save()
   
    if "nilmani12345" == "nilmani12345":
        data = {}
        num = school_machine_api.objects.values("machine_no").count()
        file='SchoolDesign/school_data_update.html'
        for i in range(num):
            first = school_machine_api.objects.first()
            if first.machine_no is not None:
                #bike_user,created=bike_user.objects.get_or_create(machine_id =first.machine_id,
                school_user_data,created=school_machine_update.objects.get_or_create(machine_no =first.machine_no)
                school_user_data.school_code =first.school_code
                school_user_data.gwid =first.gwid
                school_user_data.password =first.password
                school_user_data.ssid =first.ssid
                school_user_data.machine_status ="Active"
                school_user_data.save()   
                first.delete()
            else:
                first.delete()
        # if bike_user.objects.values().filter(machine_id=machine_id).exists():
        #     data = bike_user.objects.values().filter(machine_id=machine_id
        #     file='SchoolDesign/bike_data_update.html'
     
        
    return render(request,file )

@login_required(login_url='login')
def alot_machine_no_school_code(request):
	school_code = request.user.last_name
	x =school_machine_update.objects.values().filter(school_code=school_code)
	student=""
	if request.method == "POST":
		school_code = request.POST.get('school_code')
		machine_no = request.POST.get('machine_no')
		gwid = request.POST.get('gwid')
		ssid = request.POST.get('ssid')
		password = request.POST.get('password')
		#data=school_machine_update.objects.filter(machine_no=machine_no)
		data,created=school_machine_update.objects.get_or_create(machine_no=machine_no)
	
		if data is not None:
			data.machine_no=machine_no
			data.school_code=school_code
			data.gwid=gwid
			data.ssid=ssid
			data.password=password
			data.machine_status="inactive"
			data.save()
			print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
			messages.success(request, "New Machine Successfully Saved!!")
			return redirect('/alot_machine_no_school_code')
		else:
			data = school_machine_update.objects.filter(machine_no=machine_no)
			data.update_or_create(school_code=school_code,gwid=gwid,machine_no=machine_no)
			print("22222222222222222222222222222222")



		print(school_code,machine_no,gwid)
	#school_code = UserMaster.objects.get(user_name=username).school_code
	school_info=SchoolMaster.objects.filter(school_code=school_code)
	#student=StudentMaster.objects.all().filter(school_code=school_code)
	return render(request,"alot_machine_no_school_code.html",{"school_info":school_info,"school_code":school_code,"x":x})
  

def delete_gps_data(request):
    gpsrestapi.objects.all().delete()
    
   
   
   
"""
data = StudentMaster.objects.values().filter(user_name=user)
data.update(student_card_number=rfid_data)
for i in data:
    i.update(ParentsMaster.objects.values().filter(user_id=i["parents_id"]).first())
    
    busmap.objects.values().filter(rf_id=i["rf_id"],date="18/03/2021).exist()
    i["rf_id"]
                
"""    
def show_map(request):
    gps_data_update()
    mdata=busmap.objects.values().filter(bus_no=5,machine_no=5,school_code="s001",date="19/03/2021")
   
    for i in mdata:
        i.update({"display":"none"})
        if busmap.objects.values().filter(rf_id=i["rf_id"],date="20/03/2021").exists():
            i.update({"arrived":"trainArrived"})
            i.update({"whiteindicator":"whiteIndicator"})
            i.update({"display":"none"})
            if i["rf_id"]==busmap.objects.values().filter(date="20/03/2021").last()["rf_id"]:
                i.update({"ripple":"ripple"})
                i.update({"display":""})
        
    
    return render(request,"showmap.html",{"mdata":mdata})

from django.http import JsonResponse
def server_run(request):
    f=open("datafile.txt","a")
    f.write(str("server running")+"\n")
    f.close()
    print("**************************")
    from school import tcpserver1
    print("running")
    return JsonResponse({'status': 'OK'})






def visit_demo_school(request):
	from selenium import webdriver 
	from time import sleep 
	from webdriver_manager.chrome import ChromeDriverManager 
	from selenium.webdriver.chrome.options import Options 

	usr="nilmani085@gmail.com"
	pwd="12345"

	driver = webdriver.Chrome(ChromeDriverManager().install()) 
	driver.get('https://www.sbsy.co.in/') 
	print ("Opened sbsy") 
	sleep(1) 

	username_box = driver.find_element_by_name('username') 
	username_box.send_keys(usr) 
	print ("Email Id entered") 
	sleep(1) 

	password_box = driver.find_element_by_name('password') 
	password_box.send_keys(pwd) 
	print ("Password entered") 

	login_box = driver.find_element_by_class_name("login-btn")
	login_box.click() 

	print ("Done") 
	return JsonResponse({'status': 'OK'})



def login_demo(self, browser, user):
	# change password
	#password = 'q'
	#user.set_password(password)
	#user.save()
	usr="nilmani085@gmail.com"
	pwd="12345"

	browser.get(self.live_server_url + '/')
	username_field = browser.find_element_by_name('username') 
	password_field = browser.find_element_by_name('password') 
	#username_field.send_keys(user.username)
	#password_field.send_keys(password)
	username_field.send_keys(usr)
	password_field.send_keys(pwd)

	submit = browser.find_element_by_class_name("login-btn")
	submit.click()
	return JsonResponse({'status': 'OK'})


@unauthenticated_user
def login_demo(request):
	logout(request)
	if 1==1:
		username = "nilmani085@gmail.com"
		password ="12345"

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')
			return redirect('home')

	context = {}
	return render(request, 'SchoolDesign/login.html', context)






def chat(request):
    return render(request,'chat/home.html')#this is sachin


def camchat(request):
    return render(request,'camchat/index.html')#this is sachin


def cam(request):
    # chat = ChatMessage.objects.all()
    chat={}
    return render(request,'camra.html', {'chat':chat})


def screen(request):
    # chat = ChatMessage.objects.all()
    chat={}
    return render(request,'chat/screen.html', {'chat':chat})




def screen1(request):
    # chat = ChatMessage.objects.all()
    chat={}
    return render(request,'chat/index.html', {'chat':chat})


def cam(request):
	# chat = ChatMessage.objects.all()
	from django.core import files
	from django.core.files.base import ContentFile

	import requests
	# from .models import MyModel

	def download_img():
		r = requests.get("https://sexsmartfilms.com/videos/0_1800.mp4", allow_redirects=True)
		filename = "https://sexsmartfilms.com/videos/0_1800.mp4".split("/")[-1]

		my_model = ModelWithImage(
			file=files.File(ContentFile(r.content), filename)
		)
		my_model.save()

		# return
	chat={}
	download_img()
	return render(request,'camra.html', {'chat':chat})