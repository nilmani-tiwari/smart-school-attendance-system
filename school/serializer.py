
from school.models import attendance_api,gpsrestapi,Bikeapi,Pumpapi,school_machine_api,Busapi
from rest_framework.serializers import ModelSerializer

class attendanceSerializer(ModelSerializer):
    
    class Meta:
        
        model=attendance_api
        fields='__all__'


class gpsrestapiSerializer(ModelSerializer):
    
    class Meta:
        
        model=gpsrestapi
        fields='__all__'



class BikeapiSerializer(ModelSerializer):
    
    class Meta:
        
        model=Bikeapi
        fields='__all__'
        
        

class BusapiSerializer(ModelSerializer):
    
    class Meta:
        
        model=Busapi
        fields='__all__'
        

class pumpapiSerializer(ModelSerializer):
    
    class Meta:
        
        model=Pumpapi
        fields='__all__'
        
        

class school_machine_apiSerializer(ModelSerializer):
    
    class Meta:
        
        model=school_machine_api
        fields='__all__'