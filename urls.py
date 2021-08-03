"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from myapp.views import *
from memberApp.views import *
from productApp.views import *
from orderApp.views import *

urlpatterns = [
    # url(r'^admin/$', admin.site.urls),
    # url(r'^myapp/$', myApphome),
    # url(r'^add/(\d+)/(\d+)/(\d+)/.*', myAppAdd),
    url(r'^product/$', productAppHome),
    url(r'^orderAppHome/$', orderAppHome),
    # url(r'^orderHandle/$', orderHandle),
    # url(r'^orderMessage/(\w+)/(\w+)/(\w+)/$', orderMessage),
    # url(r'^show/$', show),

    url(r'^orderSystem/$', orderSystem),
    url(r'^orderRestaurant/$', orderRestaurant),
    url(r'^orderMenu/$', orderMenu),
    url(r'^orderSelect/$', orderSelect),
    url(r'^orderSelectCart/(\w+)/$', orderSelectCart),
    url(r'^orderCartList/$', orderCartList),
    url(r'^orderDelete/(\w+)/$', orderDelete),
    # url(r'^editRestaurant/$', editRestaurant),

    url(r'^memberLogin/$', memberLogin),  
    url(r'^memberLogout/$', memberLogout),
    url(r'^member/$', memberAppHome),   
    url(r'^memberCreate/(\w+)/(\w+)/(\w+)/(\w+)$', memberCreate),  
    url(r'^memberCreate/$', memberCreate),  
    url(r'^memberCreateDbCheck/$', memberCreateDbCheck),
    url(r'^memberCreateConfirm/$', memberCreateConfirm),
    url(r'^memberUpdate/(\w+)/$', memberUpdate),
    url(r'^memberUpdate/$', memberKeyQuery),    
    url(r'^memberDelete/(\w+)/$', memberDelete),
    url(r'^memberDelete/$', memberKeyQuery),
    url(r'^memberKeyQuery/$', memberKeyQuery),
    url(r'^memberListOne/(\w+)/$', memberListOne),
    url(r'^memberListOne/$', memberListOne),
    url(r'^memberListAll/$', memberListAll),
    url(r'^memberValid/$', memberValid),
    # path('admin/', admin.site.urls),
    # path(r'aaa/$', admin.site.urls),
]
