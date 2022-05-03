from django.db import models

from django.contrib.auth.models import User
from django_resized import ResizedImageField
from django.db import models
from datetime import datetime,date
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class SchoolMaster(models.Model):
    school_id = models.AutoField(primary_key=True)
    school_name = models.CharField(max_length=200, blank=True, null=True)
    school_code = models.CharField(unique=True, max_length=200, blank=True, null=True)
    registration_number=models.CharField( max_length=200, blank=True, null=True)
    affiliated_by=models.CharField( max_length=200, blank=True, null=True)
    email = models.CharField(unique=True, max_length=200, blank=True, null=True)
    mobile = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    pincode = models.CharField(max_length=20,blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    principal_sign_image = models.ImageField(upload_to='images/', blank=True, null=True)
    logo_of_school = models.ImageField(upload_to='images/', blank=True, null=True)
    password=models.CharField(max_length=200, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.school_name+" "+str(self.school_code)




class Posts(models.Model):
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    post_image = ResizedImageField(size=[640, 480], upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.title
        
        
class MediumMaster(models.Model):
    medium_id = models.AutoField(primary_key=True)
    school_code= models.CharField( max_length=200, blank=True, null=True)
    medium_name = models.CharField( max_length=200, blank=True, null=True)
    created_on = models.DateTimeField(default=datetime.now, blank=True, null=True)



    def __str__(self):
        return self.medium_name+"  "+self.school_code

class ClassMaster(models.Model):
    standard_id = models.AutoField(primary_key=True)
    school_code = models.CharField(max_length=200, blank=True, null=True)
    medium_name = models.CharField(max_length=200, blank=True, null=True)
    class_name = models.CharField(max_length=200, blank=True, null=True)
    created_on = models.DateTimeField(default=datetime.now, blank=True, null=True)

    def __str__(self):
        return self.class_name+"  "+self.medium_name+"  "+self.school_code


class DivisionMaster(models.Model):
    division_id = models.AutoField(primary_key=True)
    school_code = models.CharField(max_length=200, blank=True, null=True)
    medium_name = models.CharField(max_length=200, blank=True, null=True)
    class_name = models.CharField(max_length=200, blank=True, null=True)
    division_name = models.CharField(max_length=200, blank=True, null=True)
    created_on = models.DateTimeField(default=datetime.now, blank=True, null=True)


    def __str__(self):
        return self.class_name+"  "+self.division_name+"  "+self.medium_name+"  "+self.school_code



class OwnerMaster(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    owner_name = models.CharField(max_length=200, blank=True, null=True)
    owner_gender = models.CharField(max_length=10, blank=True, null=True)
    #owner_date_of_birth=models.DateField(blank=True,null=True)
    owner_date_of_birth=models.CharField(max_length=10, blank=True, null=True)
    owner_email = models.CharField( max_length=200, blank=True, null=True)
    owner_mobile = models.CharField(max_length=10,  blank=True, null=True)
    owner_image = models.ImageField(upload_to='images/', blank=True, null=True)
    owner_qualification = models.CharField(max_length=200, blank=True, null=True)
    owner_address = models.CharField(max_length=200, blank=True, null=True)
    owner_city = models.CharField(max_length=200, blank=True, null=True)
    owner_pincode = models.CharField(max_length=20,blank=True, null=True)
    owner_school_code=models.CharField(max_length=200, null=True,blank=True)
    created_on = models.DateTimeField(default=datetime.now, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.owner_name

   



class StudentMaster(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    user_name = models.CharField(max_length=200, blank=True, null=True)
    Full_name = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    date_of_birth=models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField( max_length=200, blank=True, null=True)
    #mobile= models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    mobile= models.CharField(max_length=10, blank=True, null=True)
    blood_group = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    Address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    pincode = models.CharField(max_length=20,blank=True, null=True)
    admission_no = models.CharField(max_length=15, blank=True, null=True)
    Religion = models.CharField(max_length=200, blank=True, null=True)
    reservation_category=models.CharField(max_length=200, blank=True, null=True)
    school_code=models.CharField(max_length=200, null=True,blank=True)
    medium_name = models.CharField(max_length=200, blank=True, null=True)
    class_name = models.CharField(max_length=200, blank=True, null=True)
    division_name = models.CharField(max_length=200, blank=True, null=True)
    parents_id= models.CharField(max_length=200, blank=True, null=True)
    student_card_number=models.CharField(max_length=200, null=True,blank=True)
    password=models.CharField(max_length=200, blank=True, null=True)
    created_on = models.DateTimeField(default=datetime.now, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.image!="":
            imageTemproary = Image.open(self.image)
            outputIoStream = BytesIO()
            imageTemproaryResized = imageTemproary.resize( (920,673) ) 
            if imageTemproaryResized.mode in ["RGBA", "P"]:
                imageTemproaryResized = imageTemproaryResized.convert("RGB")
                #imageTemproaryResized.save(outputIoStream, format='JPEG', quality=95)
            imageTemproaryResized.save(outputIoStream , format='JPEG', quality=85)
            outputIoStream.seek(0)
            self.image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        super(StudentMaster, self).save(*args, **kwargs)
    def __str__(self):
        return self.Full_name+" "


class ParentsMaster(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    fathername = models.CharField(max_length=200, blank=True, null=True)
    mothername = models.CharField(max_length=200, blank=True, null=True)
    father_occupation=models.CharField(max_length=200, blank=True, null=True)
    mother_occupation=models.CharField(max_length=200, blank=True, null=True)
    Parents_email = models.CharField(  max_length=200, blank=True, null=True)
    Parents_mobile= models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    Parents_blood_group = models.CharField(max_length=200, blank=True, null=True)
    Parents_image = models.ImageField(upload_to='images/', blank=True, null=True)
    Parents_Address = models.CharField(max_length=200, blank=True, null=True)
    Parents_city = models.CharField(max_length=200, blank=True, null=True)
    Parents_pincode = models.CharField(max_length=20,blank=True, null=True)
    Parents_Religion = models.CharField(max_length=200, blank=True, null=True)
    Parents_occupation = models.CharField(max_length=200, blank=True, null=True)
    Parents_school_code=models.CharField(max_length=200, null=True,blank=True)
    password=models.CharField(max_length=200, blank=True, null=True)
    created_on = models.DateTimeField(default=datetime.now, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self. fathername+" "+str(self.Parents_mobile)+":"+str(self.pk)


class StaffMaster(models.Model):
    staff_user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    staff_user_name = models.CharField(max_length=200, blank=True, null=True)
    staff_First_name = models.CharField(max_length=200, blank=True, null=True)
    staff_Last_name = models.CharField(max_length=200, blank=True, null=True)
    staff_gender = models.CharField(max_length=10, blank=True, null=True)
    staff_date_of_birth=models.CharField(max_length=10, blank=True, null=True)
    staff_email = models.CharField(  max_length=200, blank=True, null=True)
    staff_mobile= models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    staff_qualification = models.CharField(  max_length=200, blank=True, null=True)
    staff_blood_group = models.CharField(max_length=200, blank=True, null=True)
    staff_image = models.ImageField(upload_to='images/', blank=True, null=True)
    staff_Address = models.CharField(max_length=200, blank=True, null=True)
    staff_city = models.CharField(max_length=200, blank=True, null=True)
    staff_pincode = models.CharField(max_length=20,blank=True, null=True)
    staff_Religion = models.CharField(max_length=200, blank=True, null=True)
    staff_subject = models.CharField(max_length=200, blank=True, null=True)
    staff_medium_name = models.CharField(max_length=200, blank=True, null=True)
    staff_class_name = models.CharField(max_length=200, blank=True, null=True)
    staff_division_name = models.CharField(max_length=200, blank=True, null=True)
    staff_card_number=models.CharField(max_length=200, null=True,blank=True)
    staff_school_code=models.CharField(max_length=200, null=True,blank=True)
    password=models.CharField(max_length=200, blank=True, null=True)
    created_on = models.DateTimeField(default=datetime.now, blank=True)
    created_by = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.staff_First_name




class attendance_api(models.Model):
    school_code=models.CharField( max_length=200)
    attendance_timestamp=models.CharField(max_length=100)
    rf_id=models.CharField(max_length=64)
    gwId = models.CharField(max_length=64,db_column='gwId',null=True)


class Attendance(models.Model):
    attendance_id=models.AutoField(primary_key=True)
    rf_id=models.CharField(max_length=64)
    name=models.CharField(max_length=64,null=True, blank=True)
    date= models.DateField(null=True)
    gwId= models.CharField(max_length=64,db_column='gwId',null=True)
    intime=models.CharField(max_length=64,null=True, blank=True)
    outtime=models.CharField(max_length=64,null=True, blank=True)
    school_code = models.CharField(max_length=200, blank=True, null=True)
    medium_name = models.CharField(max_length=200, blank=True, null=True)
    class_name = models.CharField(max_length=200, blank=True, null=True)
    division_name = models.CharField(max_length=200, blank=True, null=True)
    group_id=models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.school_code+" "+self.name+" "+str(self.date)


class notice_board_school(models.Model):
    notice_id = models.AutoField(primary_key=True)
    school_code = models.CharField(max_length=200, blank=True, null=True)
    Title=models.CharField(max_length=64,null=True, blank=True)
    Details=models.CharField(max_length=64,null=True, blank=True)
    Posted_by=models.CharField(max_length=64,null=True, blank=True)
    Date=models.DateField(null=True)
    created_on = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.school_code+" "+self.Title

class School_Transport(models.Model):
    transport_id = models.AutoField(primary_key=True)
    school_code = models.CharField(max_length=200, blank=True, null=True)
    Vehicle_Number= models.CharField(max_length=200, blank=True, null=True)
    Driver_Name = models.CharField(max_length=200, blank=True, null=True)
    Phone_Number = models.CharField(max_length=200, blank=True, null=True)
    License_Number = models.CharField(max_length=200, blank=True, null=True)
    Route_Name = models.CharField(max_length=200, blank=True, null=True)
    reader_machine_no = models.CharField(max_length=200, blank=True, null=True)
    gps_sim_no = models.CharField(max_length=200, blank=True, null=True)
    ssid= models.CharField(max_length=20, blank=True, null=True)
    password=models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        return self.school_code + " " + self.Route_Name

class school_library(models.Model):
    school_library_id = models.AutoField(primary_key=True)
    school_code = models.CharField(max_length=200, blank=True, null=True)
    Book_Name= models.CharField(max_length=200, blank=True, null=True)
    Subject = models.CharField(max_length=200, blank=True, null=True)
    Writter_Name = models.CharField(max_length=200, blank=True, null=True)
    Class = models.CharField(max_length=200, blank=True, null=True)
    created_on = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.school_code + " " + self.Book_Name+ " " + self.Writter_Name


class school_holiday(models.Model):
    school_holiday_id = models.AutoField(primary_key=True)
    school_code = models.CharField(max_length=200, blank=True, null=True)
    holiday_name= models.CharField(max_length=200, blank=True, null=True)
    details=models.CharField(max_length=200, blank=True, null=True)
    date= models.DateField(null=True)
    created_on = models.DateTimeField(default=datetime.now)


    def __str__(self):
        return self.school_code + " " + self.holiday_name

class quary_form(models.Model):
    quary_id = models.AutoField(primary_key=True)
    concern_person =models.CharField(max_length=200, blank=True, null=True)
    school_admin_name= models.CharField(max_length=200, blank=True, null=True)
    school_admin_contact= models.CharField(max_length=200, blank=True, null=True)
    school_name = models.CharField(max_length=200, blank=True, null=True)
    school_adress= models.CharField(max_length=200, blank=True, null=True)
    state=models.CharField(max_length=200, blank=True, null=True)
    pincode = models.CharField(max_length=20,blank=True, null=True)
    total_students=models.CharField(max_length=200, blank=True, null=True)
    total_teachers=models.CharField(max_length=200, blank=True, null=True)
    number_of_medium =models.CharField(max_length=200, blank=True, null=True)
    class_up_to=models.CharField(max_length=200, blank=True, null=True)
    meeting_conclussion =models.CharField(max_length=200, blank=True, null=True)#select field 1 agree for product (school_mannagement system) 2 next meeting
    if_next_meeting_date=models.DateField(null=True)
    massage=models.CharField(max_length=200, blank=True, null=True)
    date= models.DateField(null=True,default=datetime.today)
    created_on = models.DateTimeField(default=datetime.now)


class message_pack(models.Model):
    massage_id = models.AutoField(primary_key=True)
    school_code = models.CharField(max_length=200, blank=True, null=True)
    total_msg= models.CharField(max_length=200, blank=True, null=True)
    sent_msg_to=models.CharField(max_length=200, blank=True, null=True)
    message=models.CharField(max_length=200, blank=True, null=True)
    date= models.DateField(null=True)

    def str(self):
        return self.school_code + " total_msg = " + self.total_msg
        
class user_command(models.Model):
    command_id = models.AutoField(primary_key=True)
    user_contact = models.CharField(max_length=200,unique=True, blank=True, null=True)
    command= models.CharField(max_length=200, blank=True, null=True)
    pin_no=models.CharField(max_length=200, blank=True, null=True)
    date= models.DateField(null=True)               
        
class gpsrestapi(models.Model):
    imei_no=models.CharField( max_length=200, blank=True, null=True)
    sim_no=models.CharField(max_length=100, blank=True, null=True)
    log=models.CharField(max_length=64, blank=True, null=True)
    lat=models.CharField(max_length=64, blank=True, null=True)
    datetime=models.CharField(max_length=64, blank=True, null=True)
   
   
#*****************************************************************bile lock projects************VVVVVVVVVVVVVVVVVVVVV**********************************************         

class Bikeapi(models.Model):   # machine details by api through machine send by machine
    id = models.AutoField(primary_key=True)
    machine_id = models.CharField( max_length=200, blank=True, null=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    mobile_no = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    vechile_no = models.CharField(max_length=20,blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    ssid= models.CharField(max_length=20,blank=True, null=True)
    password=models.CharField(max_length=20,blank=True, null=True)
    rf_id1=models.CharField(max_length=64 , blank=True, null=True)
    rf_id2=models.CharField(max_length=64 , blank=True, null=True)
    created_on = models.DateTimeField(default=datetime.now, blank=True)
    dealer=models.CharField(max_length=200,blank=True, null=True)

class bike_user(models.Model):   # machine data update perpous any update of user by html page to here atomatically updated by machine
    id = models.AutoField(primary_key=True)
    machine_id = models.CharField(unique=True, max_length=200, blank=True, null=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    mobile_no = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    vechile_no = models.CharField(max_length=20,blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    ssid= models.CharField(max_length=20,blank=True, null=True)
    password=models.CharField(max_length=20,blank=True, null=True)
    rf_id1=models.CharField(max_length=64 , blank=True, null=True)
    rf_id2=models.CharField(max_length=64, blank=True, null=True)
    created_on = models.DateTimeField(default=datetime.now, blank=True)
    dealer=models.CharField(max_length=200,blank=True, null=True)  
    
    
class bike_user_details(models.Model):   # bike user details conformed by machine on api through  Bikeapi models
    id = models.AutoField(primary_key=True)
    machine_id = models.CharField(unique=True, max_length=200, blank=True, null=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    mobile_no = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    vechile_no = models.CharField(max_length=20,blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    ssid= models.CharField(max_length=20,blank=True, null=True)
    password=models.CharField(max_length=20,blank=True, null=True)
    rf_id1=models.CharField(max_length=64 , blank=True, null=True)
    rf_id2=models.CharField(max_length=64, blank=True, null=True)
    created_on = models.DateTimeField(default=datetime.now, blank=True)
    dealer=models.CharField(max_length=200,blank=True, null=True)     
    
    
    

 
 
#*****************************************************************bile lock projects************^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^**********************************************    


class Busapi(models.Model):   # machine details by api through machine send by machine
    id = models.AutoField(primary_key=True)
    machine_no = models.CharField( max_length=200, blank=True, null=True)
    school_code = models.CharField(max_length=100,blank=True, null=True)
    rf_id=models.CharField(max_length=64 , blank=True, null=True)
    date = models.CharField(max_length=64 , blank=True, null=True)
    time = models.CharField(max_length=64 , blank=True, null=True)
    created_on = models.DateTimeField(default=datetime.now, blank=True)





class Pumpapi(models.Model):
    id = models.AutoField(primary_key=True)
    volt1 = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    volt2 = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    volt3 = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    relay1 = models.CharField(max_length=100, blank=True, null=True)
    relay2 = models.CharField(max_length=100, blank=True, null=True)
    relay3 = models.CharField(max_length=100, blank=True, null=True)
    temp= models.CharField(max_length=20,blank=True, null=True)
    tank1_waterlevel=models.CharField(max_length=20,blank=True, null=True)
    tank2_waterlevel=models.CharField(max_length=20,blank=True, null=True) 
    

class school_machine_update(models.Model):
    id = models.AutoField(primary_key=True)
    machine_no = models.CharField(unique=True,max_length=100,blank=True, null=True)
    school_code = models.CharField(max_length=200, blank=True, null=True)
    gwid= models.CharField(max_length=200, blank=True, null=True)
    ssid= models.CharField(max_length=20, blank=True, null=True)
    password=models.CharField(max_length=20, blank=True, null=True)
    machine_status=models.CharField(max_length=200, blank=True, null=True)
    created_on = models.DateTimeField(default=datetime.now, blank=True)


class school_machine_details(models.Model):
    id = models.AutoField(primary_key=True)
    machine_no = models.CharField(max_length=100,blank=True, null=True)
    school_code = models.CharField(max_length=200, blank=True, null=True)
    gwid= models.CharField(max_length=200, blank=True, null=True)
    ssid= models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    created_on = models.DateTimeField(default=datetime.now, blank=True)

class school_machine_api(models.Model):
    id = models.AutoField(primary_key=True)
    machine_no = models.CharField(max_length=100,blank=True, null=True)
    school_code = models.CharField(max_length=200, blank=True, null=True)
    gwid= models.CharField(max_length=200, blank=True, null=True)
    ssid= models.CharField(max_length=20, blank=True, null=True)
    password=models.CharField(max_length=20, blank=True, null=True)
    created_on = models.DateTimeField(default=datetime.now, blank=True)
    
    
class busmap(models.Model):
    id = models.AutoField(primary_key=True)
    bus_no = models.CharField(max_length=100,blank=True, null=True)
    machine_no = models.CharField(max_length=100,blank=True, null=True)
    school_code = models.CharField(max_length=200, blank=True, null=True)
    rf_id=models.CharField(max_length=64 , blank=True, null=True)
    lat=models.CharField(max_length=64, blank=True, null=True)
    log=models.CharField(max_length=64, blank=True, null=True)
    date=models.CharField(max_length=64, blank=True, null=True)
    time=models.CharField(max_length=64, blank=True, null=True)
    created_on = models.DateTimeField(default=datetime.now, blank=True)


class ModelWithImage(models.Model):
    image = models.ImageField(
        upload_to='images',
    )
    file= models.FileField(upload_to='videos/', null=True, verbose_name="", blank=True)