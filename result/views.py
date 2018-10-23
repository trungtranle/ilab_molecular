from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.decorators.cache import never_cache
from result.forms import *
from result.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from result.functions import *
from django.conf import settings
import os
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
# AUTHENTICATION VIEWS
def index(request):
    return render(request, 'index.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request, user)
                print('OK')
                return redirect('index')
        else:
            return render(request, 'login.html',{'result':'Invalid username and password'})
    else: 
        return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

#COMMON VIEWS
def delete_record(model, pk = None):
    #try:
    obj = model.objects.get(pk = pk)
    if obj:
        message = 'Đã xóa ' + obj.lab_id
        obj.delete()
        
    else:
        message = 'Chưa xóa ' + obj.lab_id
    
    return message
# HBV VIEWS    
def hbv_sample_input(request):
    saved = False
    if request.method == "POST":
        form = HBVInfoForm(data = request.POST)
        
              
        if form.is_valid():
            raw_dt = form.save(commit=False)  
            if form.cleaned_data['sid'] != "":
                sid = form.cleaned_data['added'].strftime('%d%m%y-') + form.cleaned_data['sid']                
                raw_dt.sid = sid
            raw_dt.name = form.cleaned_data['name'].upper()
            raw_dt.save()            
            saved = True
           
    else:
        form = HBVInfoForm()
    
    return render(request, 'hbv_sample_input.html', {'form':form, 'saved':saved})

    
def hbv_sample_list(request):
    samples = HBVSample.objects.all()
    mess = ""
    if request.method == "POST":               
        if request.POST.get('actionbutton') == 'Xóa':        
          #  if len(request.POST.getlist('chkbx')):
            for item in request.POST.getlist('chkbx'):
                a = HBVSample.objects.get(pk = item).lab_id
                m = delete_record(HBVSample, item)
                mess += 'Đã xóa ' + a + r"\n"
            

        if request.POST.get('actionbutton') == "Finish Toggle":
            for item in request.POST.getlist('chkbx'):
                obj = HBVSample.objects.get(pk = item)
                state = obj.finished 
                obj.finished = not state
                obj.save()
                #mess += 'Updated ' + obj.lab_id + r"\n"
        
        if request.POST.get('actionbutton') == "Tạo kết quả":
            #mess = ""
            for item in request.POST.getlist('chkbx'):
                c, i = create_HBV_report(pk = item)
                if c != "": 
                    mess +=  "Đã xuất: " +  c + r"\n"
                if i != "":
                    mess +=  "LỖI: " + i + r"\n"
            
            #return render(request, 'processing_info.html', {"completed": completed, "incompleted": incompleted})

    return render(request, 'hbv_sample_list.html', {'samples':samples, 'mess':mess})

def hbv_sample_detail(request, id_ = None):
    saved = False
    instance = get_object_or_404(HBVSample, id = id_)
    form = HBVSampleForm(request.POST or None, instance= instance)
    image_file = "/run_img/" + instance.lab_id + "_amp.png"
    
    if form.is_valid():

        form.save()
        saved = True
    
    return render(request, 'hbv_detail.html', {'form':form, 'saved':saved,'sample':instance, 'image_file':image_file})

def hbv_take_info_from_run(request):
    if request.method == "POST":
        
        form = HBVFileUpload(request.POST, request.FILES)
        if form.is_valid():
            
            #completed, incompledted = ""
            completed, incompleted = process_HBV_runfile(request.FILES['green_file'], request.FILES['yellow_file'])
            return render(request, 'processing_info.html', {'completed':completed, 'incompleted':incompleted})
    else:
        form = HBVFileUpload()
        
        return render(request, 'HBV_file_processing.html', {'form':form})


def hbv_create_img(request, pk = None):
    completed, incompleted = create_HBV_image(pk = pk)
    return redirect(hbv_sample_detail, int(pk))

#HCV VIEWS
def hcv_sample_input(request):
    saved = False
    if request.method == "POST":
        form = HCVInfoForm(data = request.POST)
        
              
        if form.is_valid():
            raw_dt = form.save(commit=False)  
            if form.cleaned_data['sid'] != "":
                sid = form.cleaned_data['added'].strftime('%d%m%y-') + form.cleaned_data['sid']                
                raw_dt.sid = sid
            raw_dt.name = form.cleaned_data['name'].upper()
            raw_dt.save()            
            saved = True
           
    else:
        form = HCVInfoForm()
    
    return render(request, 'hcv_sample_input.html', {'form':form, 'saved':saved})

    
def hcv_sample_list(request):
    samples = HCVSample.objects.all()
    mess = ""
    if request.method == "POST":               
        if request.POST.get('actionbutton') == 'Xóa':        
          #  if len(request.POST.getlist('chkbx')):
            for item in request.POST.getlist('chkbx'):
                a = HCVSample.objects.get(pk = item).lab_id
                m = delete_record(HCVSample, item)
                mess += 'Đã xóa ' + a + r"\n"
            

        if request.POST.get('actionbutton') == "Finish Toggle":
            for item in request.POST.getlist('chkbx'):
                obj = HCVSample.objects.get(pk = item)
                state = obj.finished 
                obj.finished = not state
                obj.save()
                #mess += 'Updated ' + obj.lab_id + r"\n"
        
        if request.POST.get('actionbutton') == "Tạo kết quả":
            #mess = ""
            for item in request.POST.getlist('chkbx'):
                c, i = create_HCV_report(pk = item)
                if c != "": 
                    mess +=  "Đã xuất: " +  c + r"\n"
                if i != "":
                    mess +=  "LỖI: " + i + r"\n"
            
            #return render(request, 'processing_info.html', {"completed": completed, "incompleted": incompleted})

    return render(request, 'hcv_sample_list.html', {'samples':samples, 'mess':mess})

def hcv_sample_detail(request, id_ = None):
    saved = False
    instance = get_object_or_404(HCVSample, id = id_)
    form = HCVSampleForm(request.POST or None, instance= instance)
    image_file = "/run_img/" + instance.lab_id + "_amp.png"
    
    if form.is_valid():

        form.save()
        saved = True
    
    return render(request, 'hcv_detail.html', {'form':form, 'saved':saved,'sample':instance, 'image_file':image_file})

def hcv_take_info_from_run(request):
    if request.method == "POST":
        
        form = HCVFileUpload(request.POST, request.FILES)
        if form.is_valid():
            
            #completed, incompledted = ""
            completed, incompleted = process_HCV_runfile(request.FILES['green_file'], request.FILES['yellow_file'])
            return render(request, 'processing_info.html', {'completed':completed, 'incompleted':incompleted})
    else:
        form = HCVFileUpload()
        
        return render(request, 'HCV_file_processing.html', {'form':form})

def hcv_create_img(request, pk = None):
    
    completed, incompleted = create_HCV_image(pk = pk)
    #return render(request, 'index')
    return redirect(hcv_sample_detail, int(pk), )


#CTNG
def ctng_sample_input(request):
    saved = False
    if request.method == "POST":
        form = CTNGInfoForm(data = request.POST)
        
              
        if form.is_valid():
            raw_dt = form.save(commit=False)  
            if form.cleaned_data['sid'] != "":
                sid = form.cleaned_data['added'].strftime('%d%m%y-') + form.cleaned_data['sid']                
                raw_dt.sid = sid
            raw_dt.name = form.cleaned_data['name'].upper()
            raw_dt.save()            
            saved = True
           
    else:
        form = CTNGInfoForm()
    
    return render(request, 'ctng_sample_input.html', {'form':form, 'saved':saved})

    
def ctng_sample_list(request):
    samples = CTNGSample.objects.order_by("-lab_id")
    mess = ""
    if request.method == "POST":               
        if request.POST.get('actionbutton') == 'Xóa':        
          #  if len(request.POST.getlist('chkbx')):
            for item in request.POST.getlist('chkbx'):
                a = CTNGSample.objects.get(pk = item).lab_id
                m = delete_record(CTNGSample, item)
                mess += 'Đã xóa ' + a + r"\n"
            

        if request.POST.get('actionbutton') == "Finish Toggle":
            for item in request.POST.getlist('chkbx'):
                obj = CTNGSample.objects.get(pk = item)
                state = obj.finished 
                obj.finished = not state
                obj.save()
                #mess += 'Updated ' + obj.lab_id + r"\n"
        
        if request.POST.get('actionbutton') == "Tạo kết quả":
            #mess = ""
            for item in request.POST.getlist('chkbx'):
                c, i = create_CTNG_report(pk = item)
                if c != "": 
                    mess +=  "Đã xuất: " +  c + r"\n"
                if i != "":
                    mess +=  "LỖI: " + i + r"\n"
            
            #return render(request, 'processing_info.html', {"completed": completed, "incompleted": incompleted})

    return render(request, 'ctng_sample_list.html', {'samples':samples, 'mess':mess})

def ctng_sample_detail(request, id_ = None):
    saved = False
    instance = get_object_or_404(CTNGSample, id = id_)
    form = CTNGSampleForm(request.POST or None, instance= instance, initial= {'result_ct': 'ÂM TÍNH', 'result_ng':'ÂM TÍNH'})
    image_file = "/run_img/" + instance.lab_id + "-VA.png"
    
    if form.is_valid():

        form.save()
        saved = True
    
    return render(request, 'ctng_detail.html', {'form':form, 'saved':saved,'sample':instance, 'image_file':image_file})

def ctng_take_info_from_run(request):
    if request.method == "POST":
        
        form = CTNGFileUpload(request.POST, request.FILES)
        if form.is_valid():
            
            #completed, incompledted = ""
            completed, incompleted = process_CTNG_runfile(request.FILES['green_file'], request.FILES['orange_file'], request.FILES['yellow_file'])
            return render(request, 'processing_info.html', {'completed':completed, 'incompleted':incompleted})
    else:
        form = CTNGFileUpload()
        
        return render(request, 'CTNG_file_processing.html', {'form':form})

def ctng_create_img(request, pk = None):
    
    completed, incompleted = create_CTNG_image(pk = pk)
    #return render(request, 'index')
    return redirect(ctng_sample_detail, int(pk))

#HPV
def hpv_sample_input(request):
    saved = False
    if request.method == "POST":
        form = HPVInfoForm(data = request.POST)
        
              
        if form.is_valid():
            raw_dt = form.save(commit=False)  
            if form.cleaned_data['sid'] != "":
                sid = form.cleaned_data['added'].strftime('%d%m%y-') + form.cleaned_data['sid']                
                raw_dt.sid = sid
            raw_dt.name = form.cleaned_data['name'].upper()
            raw_dt.save()            
            saved = True
           
    else:
        form = HPVInfoForm()
    
    return render(request, 'hpv_sample_input.html', {'form':form, 'saved':saved})

    
def hpv_sample_list(request):
    samples = HPVSample.objects.order_by("-lab_id")
    mess = ""
    if request.method == "POST":               
        if request.POST.get('actionbutton') == 'Xóa':        
          #  if len(request.POST.getlist('chkbx')):
            for item in request.POST.getlist('chkbx'):
                a = HPVSample.objects.get(pk = item).lab_id
                m = delete_record(HPVSample, item)
                mess += 'Đã xóa ' + a + r"\n"
            

        if request.POST.get('actionbutton') == "Finish Toggle":
            for item in request.POST.getlist('chkbx'):
                obj = HPVSample.objects.get(pk = item)
                state = obj.finished 
                obj.finished = not state
                obj.save()
                #mess += 'Updated ' + obj.lab_id + r"\n"
        
        if request.POST.get('actionbutton') == "Tạo kết quả":
            #mess = ""
            for item in request.POST.getlist('chkbx'):
                c, i = create_HPV_report(pk = item)
                if c != "": 
                    mess +=  "Đã xuất: " +  c + r"\n"
                if i != "":
                    mess +=  "LỖI: " + i + r"\n"
            
            #return render(request, 'processing_info.html', {"completed": completed, "incompleted": incompleted})

    return render(request, 'hpv_sample_list.html', {'samples':samples, 'mess':mess})

def hpv_sample_detail(request, id_ = None):
    saved = False
    instance = get_object_or_404(HPVSample, id = id_)
    form = HPVSampleForm(request.POST or None, request.FILES or None, instance= instance)
    if instance.test_kit == "VA":
        image_file = "/run_img/" + instance.lab_id + "-VA.png"
    elif instance.test_kit == "KT": 
        image_file = "/run_img/" + instance.lab_id + "-KT.png"

    if form.is_valid():

        form.save()
        saved = True
    
    return render(request, 'hpv_detail.html', {'form':form, 'saved':saved,'sample':instance, 'image_file':image_file})

def hpv_take_info_from_run(request):
    if request.method == "POST":
        
        form = HPVFileUpload(request.POST, request.FILES)
        if form.is_valid():
            
            #completed, incompledted = ""
            try:
                completed, incompleted = process_HPV_runfile(request.FILES['green_file'], request.FILES['yellow_file'], request.FILES['orange_file'], request.FILES['red_file'])
            except MultiValueDictKeyError:
                completed, incompleted = process_HPV_runfile(request.FILES['green_file'], request.FILES['yellow_file'],None, None)
            return render(request, 'processing_info.html', {'completed':completed, 'incompleted':incompleted})
    else:
        form = HPVFileUpload()
        
        return render(request, 'HPV_file_processing.html', {'form':form})

def hpv_create_img(request, pk = None):
    
    completed, incompleted = create_HPV_image(pk = pk)
    #return render(request, 'index')
    return redirect(hpv_sample_detail, int(pk))


