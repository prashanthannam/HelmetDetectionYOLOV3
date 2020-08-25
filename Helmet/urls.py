from django.contrib import admin
from django.urls import path
from django.conf import settings 
from django.conf.urls import *
from django.views.generic import TemplateView
from django.conf.urls.static import static 


urlpatterns = [
    # path('admin/',admin.site.urls),
    path('admin/', admin.site.urls),
    url('detect/',include('detect.urls')),
    url('accounts/',include('accounts.urls')),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
