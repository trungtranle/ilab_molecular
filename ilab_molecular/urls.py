"""ilab_molecular URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
import result.views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', result.views.index, name = 'index'),
    re_path(r'logout', result.views.logout, name = 'logout'),    
    path('login', result.views.user_login, name = 'login'),
    #B URLS
    re_path(r'^b_new', result.views.hbv_sample_input, name = 'b_new'),
    re_path(r'^b_sample_list', result.views.hbv_sample_list, name = 'b_sample_list'),
    re_path(r'^b_run_file', result.views.hbv_take_info_from_run, name = 'b_run_file'),    
    re_path(r'b_detail/(\d+)', result.views.hbv_sample_detail, name = 'b_detail'),
    re_path(r'b_image/(\d+)', result.views.hbv_create_img, name = 'b_image'),
    #C URL
    re_path(r'^c_new', result.views.hcv_sample_input, name = 'c_new'),
    re_path(r'^c_sample_list', result.views.hcv_sample_list, name = 'c_sample_list'),
    re_path(r'^c_run_file', result.views.hcv_take_info_from_run, name = 'c_run_file'),    
    re_path(r'c_detail/(\d+)', result.views.hcv_sample_detail, name = 'c_detail'),
    re_path(r'c_image/(\d+)', result.views.hcv_create_img, name = 'c_image'),
    #CTNG_URL
    re_path(r'^ctng_new', result.views.ctng_sample_input, name = 'ctng_new'),
    re_path(r'^ctng_sample_list', result.views.ctng_sample_list, name = 'ctng_sample_list'),
    re_path(r'^ctng_run_file', result.views.ctng_take_info_from_run, name = 'ctng_run_file'),    
    re_path(r'ctng_detail/(\d+)', result.views.ctng_sample_detail, name = 'ctng_detail'),
    re_path(r'ctng_image/(\d+)', result.views.ctng_create_img, name = 'ctng_image'),
    #HPV_URL
    re_path(r'^hpv_new', result.views.hpv_sample_input, name = 'hpv_new'),
    re_path(r'^hpv_sample_list', result.views.hpv_sample_list, name = 'hpv_sample_list'),
    re_path(r'^hpv_run_file', result.views.hpv_take_info_from_run, name = 'hpv_run_file'),    
    re_path(r'hpv_detail/(\d+)', result.views.hpv_sample_detail, name = 'hpv_detail'),
    re_path(r'hpv_image/(\d+)', result.views.hpv_create_img, name = 'hpv_image'),
    re_path(r'hpv_populate/(\d+)', result.views.hpv_populate, name= 'hpv_populate')


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
