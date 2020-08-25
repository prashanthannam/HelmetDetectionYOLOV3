from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from .views import *
app_name='detect'
urlpatterns=[
path('admin/', admin.site.urls),
    # path('sayHello/',myView),
    # path('',success),
    path('',base),
    
    url(r'^helmetview/$',helmetview,name='helmet'),
    url(r'^helmetview1/$',helmetview1,name='helmetview1'),    
    path('success',success),
]