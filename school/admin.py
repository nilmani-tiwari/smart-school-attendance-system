from django.contrib import admin
from school.models import *
# Register your models here.
admin.site.register(SchoolMaster)

admin.site.register(MediumMaster)

admin.site.register(ClassMaster)

admin.site.register(DivisionMaster)
admin.site.register(OwnerMaster)
admin.site.register(StudentMaster)
admin.site.register(ParentsMaster)
admin.site.register(StaffMaster)
admin.site.register(Attendance)
admin.site.register(notice_board_school)
admin.site.register(School_Transport)
admin.site.register(school_library)
admin.site.register(school_holiday)
admin.site.register(message_pack)
admin.site.register(user_command)
admin.site.register(bike_user)
admin.site.register(school_machine_update)
admin.site.register(Posts)
#admin.site.register(school_machine_api)
admin.site.register(school_machine_details)
admin.site.register(busmap)
admin.site.register(ModelWithImage)


class attendanceAdmin(admin.ModelAdmin):
   list_display = ['school_code', 'attendance_timestamp', 'rf_id', 'gwId']

admin.site.register(attendance_api,attendanceAdmin)

class gpsrestapiAdmin(admin.ModelAdmin):
   list_display = ['imei_no', 'sim_no', 'log', 'lat', 'datetime']

admin.site.register(gpsrestapi,gpsrestapiAdmin)



class BikeapiAdmin(admin.ModelAdmin):
   list_display = ['name','machine_id', 'mobile_no', 'vechile_no', 'address', 'ssid','password','rf_id1','rf_id2','created_on','dealer']

admin.site.register(Bikeapi,BikeapiAdmin)



# class BusapiAdmin(admin.ModelAdmin):
#   list_display = ['machine_no','school_code', 'rf_id', 'date','time','created_on']

admin.site.register(Busapi)


class school_machine_apiAdmin(admin.ModelAdmin):
   list_display = ['machine_no', 'school_code', 'ssid','password','gwid']

admin.site.register(school_machine_api,school_machine_apiAdmin)

class PumpapiAdmin(admin.ModelAdmin):
   list_display = ['volt1']
admin.site.register(Pumpapi,PumpapiAdmin)