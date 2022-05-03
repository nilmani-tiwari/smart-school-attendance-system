from django import forms
from school.models import *

# class LoginForm(forms.Form): # doubtfull
#    occasion=['christmas','New Year']
#    user = forms.CharField(max_length = 100)
#    select = forms.ChoiceField(widget=forms.Select(choices=occasion))


class StudentForm(forms.ModelForm):
   class Meta:
      model=StudentMaster
      #fields= "__all__"
      fields = ['student_name', 'father_name', 'mother_name', 'admission_date','date_of_birth','caste_category','gender','student_email','student_mobile','student_image','address',
                'city','pincode','standard','division','medium'
                ]

class ParentsForm(forms.ModelForm):
   class Meta:
      model=ParentsMaster
      #fields= "__all__"
      fields = ['father_name', 'mother_name','parents_email','parents_mobile','parents_image','address',
                'city','pincode','father_occupation','mother_occupation'
                ]


class notice_board_school(forms.ModelForm):
   class Meta:
      model=notice_board_school
      fields = ['Title','Details','Posted_by','Date','school_code']