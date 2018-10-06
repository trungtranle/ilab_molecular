'''from django.shortcuts import render, redirect, get_object_or_404
from result.forms import HBVInfoForm, HBVSampleForm, HBVFileUpload
from result.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from result.functions import process_HBV_runfile
# Create your views here.

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


def hbv_sample_input(request):
    saved = False
    if request.method == "POST":
        form = HBVInfoForm(data = request.POST)        
        if form.is_valid():            
            form.save()            
            saved = True
    
    else:
        form = HBVInfoForm()
    
    return render(request, 'hbv_sample_input.html', {'form':form, 'saved':saved})

def hbv_sample_list(request):
    samples = HBVSampleInfo.objects.all()
    
    return render(request, 'hbv_sample_list.html', {'samples':samples})

def hbv_sample_detail(request, id_ = None):
    saved = False
    instance = get_object_or_404(HBVSampleInfo, id = id_)
    form = HBVSampleForm(request.POST or None, instance= instance, initial= {'finished_by' : request.user.last_name + ' ' + request.user.first_name, 'standard_curve':HBVStandardCurve.objects.last().pk})
    print(request.user.last_name + ' ' + request.user.first_name)
    
    if form.is_valid():

        form.save()
        saved = True
    else:
        print('NO')
    return render(request, 'hbv_detail.html', {'form':form, 'saved':saved})

def hbv_take_info_from_run(request):
    if request.method == "POST":
        print('HERE')
        form = HBVFileUpload(request.POST, request.FILES)
        if form.is_valid():
            print('OK')
            #completed, incompledted = ""
            completed, incompleted = process_HBV_runfile(request.FILES['green_file'], request.FILES['yellow_file'])
            return render(request, 'processing_info.html', {'completed':completed, 'incompleted':incompleted})
    else:
        form = HBVFileUpload()
        
        return render(request, 'HBV_file_processing.html', {'form':form})'''