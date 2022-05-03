"""newsbsy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    #path('admin/', admin.site.urls),
   path('',views.home, name='home'),
   path('student/', views.student, name='student'),
    path('sachin/', views.sachin, name='sachin'),
    path('parents/', views.parents, name='parents'),
    path('staff/', views.staff, name='staff'),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('change_password/', views.change_password, name="change_password"),
    path('forget_password/', auth_views.PasswordResetView.as_view()),
    path('allstudent/', views.Allstudent, name='Allstudent'),
    path('student_delete/<int:id>', views.student_delete, name='student_delete'),
    path('allstaff/', views.Allstaff, name='Allstaff'),
    path('staff_delete/<int:id>', views.staff_delete, name='staff_delete'),
    path('student_details/', views.student_details, name='student_details'),
    path('staff_details/', views.staff_details, name='staff_details'),
    path('admit_form/',views.admit_form, name='admit_form'),
    path('add_staff/', views.add_staff, name='add_staff'),
     path('add_other_staff/', views.add_other_staff, name='add_other_staff'),           #add other staff
    path('alot_rfid/', views.alot_rfid, name='alot_rfid'),
    path('attendence/', views.attendence, name='attendence'),
    path('manual_attendence/', views.manual_attendence, name='manual_attendence'),
    path('staff_attendence/', views.staff_attendence, name='staff_attendence'),
    path('allclass_form/', views.allclass_form, name='allclass_form'),
    path('addclass_form/', views.addclass_form, name='addclass_form'),
    path('class_delete/<int:id>', views.class_delete, name='class_delete'),
    # path('add_parents/<str:id>', views.parents_form, name='parents_form'),
    path('admission_detail/<str:id>', views.admission_detail, name='admission_details'),
    path('add_staff_detail/<str:id>', views.add_staff_detail, name='add_staff_detail'),
    path('notice_board/', views.notice_board, name='notice_board'),
    path('notice_board_delete/<int:id>', views.notice_board_delete, name='notice_board_delete'),
    path('manual_attendence/', views.manual_attendence, name='manual_attendence'),
    path('transport/', views.transport, name='transport'),
    path('transport_delete/<int:id>', views.transport_delete, name='transport_delete'),
    path('library/', views.library, name='library'),
    path('all_book/', views.all_book, name='all_book'),
    path('book_delete/<int:id>', views.book_delete, name='book_delete'),
    path('add_holiday/', views.add_holiday, name='add_holiday'),
    path('view_holidays/', views.view_holidays, name='view_holidays'),
    path('holiday_delete/<int:id>', views.holiday_delete, name='holiday_delete'),
    path('kids_attendence/', views.kids_attendence, name='kids_attendence'),
    path('my_attendence/', views.my_attendence, name='my_attendence'),
   path('msg/', views.msg, name='msg'),
   path('load_class/',views.load_class, name='ajax_load_class'),                                           # ajex
   path('load_division/', views.load_division, name='ajax_load_division'),
   path('load_student/', views.load_student, name='ajax_load_student'),
    path('load_parents/', views.load_parents, name='ajax_load_parents'),                                    #ajex
   path('absent_Student/', views.absent_Student, name='absent_Student'),
   path('Edit_student/<int:id>', views.Edit_student, name='Edit_student'),
   path('Edit_staff/<int:id>', views.Edit_staff, name='Edit_staff'),
   path('alot_verify/<str:user>/<str:rfid>/<str:password>', views.alot_verify, name='alot_verify'),
   path('bike_data_update/<str:machine_id>', views.bike_data_update, name='bike_data_update'),            # esp32 update hotspot 
  path('school_data_update/<str:machine_no>', views.school_data_update, name='school_data_update'),            # esp32 
   path('bike_save_update/', views.bike_save_update, name='bike_save_update'),
   path('school_save_update/', views.school_save_update, name='school_save_update'),
    path('homepage/',views.homepage, name='homepage'),
    path('add_school/', views.add_school, name='add_school'),
    path('commands/<str:user_contact>', views.commands, name='commands'),
    path('submit_commands/', views.submit_commands, name='submit_commands'),
    path('server_run/', views.server_run, name='server_run'),
    path('student_id_view/',views.student_id_view,name='student_id_view'),                                #  id view
    path('student_idcard/<int:id>',views.student_idcard,name='student_idcard'),
    path('staff_id_view/',views.staff_id_view,name='staff_id_view'),
    path('staff_id_view3/',views.staff_id_view3,name='staff_id_view3'),                                   # id view    delete_gps_data
    path('owner_details_update/',views.owner_details_update,name='owner_details_update'), 
    path('alot_machine_no_school_code/',views.alot_machine_no_school_code,name='alot_machine_no_school_code'),  
    
     path('delete_gps_data/', views.delete_gps_data, name='delete_gps_data'),
      path('show_map/', views.show_map, name='show_map'),

     path('visit_demo_school/', views.visit_demo_school, name='visit_demo_school'),
    path('login_demo/', views.login_demo, name='login_demo'),
    path('chat/', views.chat, name='chat'),

    path('cam/',views.cam,name='cam'),
    path('camchat/', views.camchat, name='camchat'),
      path('screen/', views.screen, name='screen'),
            path('screen1/', views.screen1, name='screen1'),


]
