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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import  routers
from school import views
from rest_framework import  routers
router=routers.DefaultRouter()
router.register('',views.attendanceCRUDCBV)

router1=routers.DefaultRouter()
router1.register('',views.gpsrestapiCRUDCBV)

router2=routers.DefaultRouter()
router2.register('',views.BikeapiCRUDCBV)

router3=routers.DefaultRouter()
router3.register('',views.pumpapiCRUDCBV)

router4=routers.DefaultRouter()
router4.register('',views.school_machine_apiCRUDCBV)

router5=routers.DefaultRouter()
router5.register('',views.BusapiCRUDCBV)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sbsydatapi/', include(router.urls)),
    path('gpsrestapi/', include(router1.urls)),
    path('Bikeapi/', include(router2.urls)),
    path('pumpapi/', include(router3.urls)),
    path('school_machine_api/', include(router4.urls)),
    path('', include('school.urls')),
    path('Busapi/', include(router5.urls)),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)






