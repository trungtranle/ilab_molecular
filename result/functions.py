import numpy as np
import pandas as pd
import os
import xml.dom.minidom
import re
from result.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.conf import settings
import json
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
from mailmerge import MailMerge
import re
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Cm
from datetime import datetime
import math
from decimal import Decimal
from django.contrib import messages
import random


def no_accent_vietnamese(s):    
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s

#HBV FUNCTIONS
def create_HBV_image(pk = None):
    try:
        cycles = np.arange(1, 41)
        obj = get_object_or_404(HBVSample, pk = pk)
        completed = ""
        incompleted = ""
        #try:
        std = obj.std_curve
        standards = json.loads(std.stds)
        quant_curve = json.loads(std.std_curve)
        curves = json.loads(obj.curves) 

        #colors and makers for ax1
        color = ['#0084E8','#0C40FF','#2300E8']
        marker = ['o', '<','x']
        fig, (ax1,ax2) = plt.subplots(1,2)
        fig.set_size_inches(10, 4)
        #plot duong chay
        for no, name in list(enumerate(standards)):    
            ax1.plot(cycles, pd.DataFrame(standards[name]), label = 'Standard ' + str(name), c = color[no], marker = marker[no], markersize = 3, linestyle = '-', linewidth = 1)
        ax1.plot(cycles, pd.DataFrame(curves["green"]), label = obj.lab_id, c = 'red', linewidth = 2.3)
        ax1.plot(cycles, pd.DataFrame(curves['yellow']), label = 'Chứng nội', c = 'green', alpha = 0.7, marker = '+', markersize = 3)
        ax1.legend()
        ax1.set_xlabel('Cycles')
        ax1.set_ylabel('Normalized Fluorescence')    
        ax1.set_title('Amplification Plot')
        ax1.grid(linestyle = ':', alpha = 0.5)
        ax1.hlines(0.02, xmin = 0, xmax = 40, colors='grey', linestyles='dotted', linewidth = 0.7)
        ax1.text(0, 0.13, 'Threshold', fontsize = 9, color='grey')
        #plot duong chuan
        line_x = pd.DataFrame([1, 8])
        line_y = pd.DataFrame([std.slope + std.B, std.slope * 8 + std.B])
        ax2.plot(line_x, line_y, c = 'black')
        for k,v in quant_curve.items():
            ax2.scatter(float(k),v, c = 'black',s = 10, marker = 's')
        ax2.set_title("Standard Curve")
        ax2.set_xlabel("Log concentration per reaction")
        ax2.set_ylabel('C$_t$')
        
        if obj.ct != None:
            ax2.scatter((obj.ct - std.B)/std.slope, obj.ct, label = obj.lab_id)
        
        ax2.legend()
        ax2.grid(linestyle = ':', alpha = 0.5)
        textstr = '\n'.join((
        r'Efficiency = %.2f %%' % (std.eff, ),
        r'$R^2$ = %.2f' % (std.r_2, ),
        r'Slope = %.2f' % (std.slope, )))
        fig.tight_layout(h_pad = 3)    
        props = dict(boxstyle='round', alpha=0)
        ax2.text(0.05, 0.05, textstr, transform=ax2.transAxes,
            verticalalignment='bottom', bbox=props)
        name = "static/run_img/"+ obj.lab_id +'_amp.png'
        fig.savefig(name, type = 'png', bbox_inches = 'tight', dpi= 100)
        plt.close("all")
        completed = obj.lab_id
        
    
    except TypeError:
        incompleted = "Chưa nhập file chạy " + obj.lab_id
    
    return completed, incompleted

def process_HBV_runfile(green_file, yellow_file):
    completed = []
    not_complete = []
    
    try:
        file_1 = xml.dom.minidom.parse(green_file)
        root_1 = file_1.documentElement
        data_1 = {}
        series = root_1.getElementsByTagName('series')
        for serie in series:
            name = re.search(r'([Hh][Bb][vV]-\S*)',
                             serie.getAttribute('title')).group(0)
            array = []
            for point in serie.getElementsByTagName('points')[0].getElementsByTagName('point'):
                array.append(float(point.getAttribute('Y')))
            data_1[name] = array

        file_2 = xml.dom.minidom.parse(yellow_file)
        root_2 = file_2.documentElement
        data_2 = {}
        series = root_2.getElementsByTagName('series')
        for serie in series:
            name = re.search(r'([Hh][Bb][vV]-\S*)',
                             serie.getAttribute('title')).group(0)
            array = []
            for point in serie.getElementsByTagName('points')[0].getElementsByTagName('point'):
                array.append(float(point.getAttribute('Y')))
            data_2[name] = array
    except AttributeError:
        not_complete.append('File chạy không chứa mẫu tên HBV')

    else:
        for k, name in list(enumerate(data_1)):
            try:
                pt = HBVSample.objects.get(lab_id=name)
                js_data = {"green": data_1[name], "yellow": data_2[name]}
                js = json.dumps(js_data)
                pt.curves = js
                pt.save()

                completed.append(name)
            except(HBVSample.DoesNotExist, ObjectDoesNotExist):

                not_complete.append(name)
            except KeyError:
                not_complete.append('Hai files chạy không khớp nhau')
    for id_ in completed:
        obj = HBVSample.objects.get(lab_id = id_)
        print(obj.pk)
        c,i = create_HBV_image(obj.pk)
    
    return completed, not_complete

def create_HBV_report(pk = None):
    obj = HBVSample.objects.get(pk = pk)
    completed = ""
    incompleted = ""
    try:
        #desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        today_folder =  "D:/Result/" + datetime.now().strftime("%m%d")
        if not os.path.exists(today_folder):
            os.makedirs(today_folder, exist_ok = True)
        try:
            print(obj.sid)
            sid_short = re.search(r"\d+-(\d{4})", obj.sid).groups()[0]

        except (AttributeError, TypeError):
            sid_short = ""
        file_name = today_folder +"/" + sid_short + '-' + no_accent_vietnamese(obj.name.replace(" ",'')) + '-' +obj.lab_id+'.docx'
        pic_file = settings.STATIC_DIR + "/run_img/" + obj.lab_id + '_amp.png'
        if obj.sid == None:
            sid = ""
        else:
            sid = str(obj.sid)
        
        if obj.age != None:
            age = str(obj.age)
        else:
            age = ""
        #start merging
        f_1 = MailMerge(settings.STATIC_DIR + '/word_template/HBV FORM.docx')
        f_1.merge(
            sid = sid, 
            lab_id = str(obj.lab_id), 
            sex = obj.sex, 
            doctor = obj.doctor, 
            addres = obj.address, 
            age = age, 
            name = obj.name, 
            date_receive = obj.added.strftime('%d/%m/%Y'), 
            date_finished = obj.modified.strftime('%d/%m/%Y-%H:%M'), 
            d= datetime.now().strftime("%d"), 
            m= datetime.now().strftime('%m'), 
            y= datetime.now().strftime('%Y'))      
        if obj.result == "DƯỚI NGƯỠNG PHÁT HIỆN":
            f_1.merge(iu = "DƯỚI NGƯỠNG PHÁT HIỆN")
        elif obj.copies != None:        
            try:            
                f_1.merge(
                copies =  "{:.1E}".format(Decimal(obj.copies*obj.std_curve.factor)),
                iu = "{:.1E}".format(Decimal(obj.copies*obj.std_curve.factor/5)),
                log = "{:.1f}".format(math.log10(obj.copies*obj.std_curve.factor)))
            except:
                print('ERROR')

        f_1.write(file_name)

        doc = Document(file_name)
        for paragraph in doc.paragraphs:
            if r"None" in paragraph.text:
                print('YES NONE IS HERE')
                paragraph.text = paragraph.text.strip().replace("None", "")
            if "[image]" in paragraph.text:
                paragraph.text = paragraph.text.strip().replace("[image]", "")

                run = paragraph.add_run()
                run.add_picture(pic_file, width=Cm(15))
                paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        doc.save(file_name)
        completed = obj.lab_id + " vào " + today_folder
    except FileNotFoundError:
        incompleted = "Chưa có file hình " + obj.lab_id
    except:
        incompleted = obj.lab_id
    return completed, incompleted

#HCV FUNCTIONS
def create_HCV_image(pk = None):
    print('IM HERE')
    cycles = np.arange(1, 41)
    obj = get_object_or_404(HCVSample, pk = pk)
    completed = ""
    incompleted = ""
    #try:
    std = obj.std_curve
    standards = json.loads(std.stds)
    quant_curve = json.loads(std.std_curve)
    curves = json.loads(obj.curves) 
    print(type(standards))
    print(standards)
    #colors and makers for ax1
    color = ['#0084E8','#0C40FF','#2300E8']
    marker = ['o', '<','x']
    fig, (ax1,ax2) = plt.subplots(1,2)
    fig.set_size_inches(10, 4)
    #plot duong chay
    for no, name in list(enumerate(standards)):    
        ax1.plot(cycles, pd.DataFrame(standards[name]), label = 'Standard ' + str(name), c = color[no], marker = marker[no], markersize = 3, linestyle = '-', linewidth = 1)
    ax1.plot(cycles, pd.DataFrame(curves["green"]), label = obj.lab_id, c = 'red', linewidth = 2.3)
    ax1.plot(cycles, pd.DataFrame(curves['yellow']), label = 'Chứng nội', c = 'green', alpha = 0.7, marker = '+', markersize = 3)
    ax1.legend()
    ax1.set_xlabel('Cycles')
    ax1.set_ylabel('Normalized Fluorescence')    
    ax1.set_title('Amplification Plot')
    ax1.grid(linestyle = ':', alpha = 0.5)
    ax1.hlines(0.02, xmin = 0, xmax = 40, colors='grey', linestyles='dotted', linewidth = 0.7)
    ax1.text(0, 0.13, 'Threshold', fontsize = 9, color='grey')
    #plot duong chuan
    line_x = pd.DataFrame([1, 8])
    line_y = pd.DataFrame([std.slope + std.B, std.slope * 8 + std.B])
    ax2.plot(line_x, line_y, c = 'black')
    for k,v in quant_curve.items():
        ax2.scatter(float(k),v, c = 'black',s = 10, marker = 's')
    ax2.set_title("Standard Curve")
    ax2.set_xlabel("Log concentration per reaction")
    ax2.set_ylabel('C$_t$')
    
    if obj.ct != None:
        ax2.scatter((obj.ct - std.B)/std.slope, obj.ct, label = obj.lab_id)
    
    ax2.legend()
    ax2.grid(linestyle = ':', alpha = 0.5)
    textstr = '\n'.join((
    r'Efficiency = %.2f %%' % (std.eff, ),
    r'$R^2$ = %.2f' % (std.r_2, ),
    r'Slope = %.2f' % (std.slope, )))
    fig.tight_layout(h_pad = 3)    
    props = dict(boxstyle='round', alpha=0)
    ax2.text(0.05, 0.05, textstr, transform=ax2.transAxes,
        verticalalignment='bottom', bbox=props)
    name = "static/run_img/"+ obj.lab_id +'_amp.png'
    fig.savefig(name, type = 'png', bbox_inches = 'tight', dpi= 100)
    completed = obj.lab_id
    plt.close('all')
    print(completed)
    '''
    except TypeError:
        incompleted = "Chưa nhập file chạy " + obj.lab_id
    '''
    return completed, incompleted

def process_HCV_runfile(green_file, yellow_file):
    completed = []
    not_complete = []
    
    try:
        file_1 = xml.dom.minidom.parse(green_file)
        root_1 = file_1.documentElement
        data_1 = {}
        series = root_1.getElementsByTagName('series')
        for serie in series:
            name = re.search(r'([Hh][Cc][vV]-\S*)',
                             serie.getAttribute('title')).group(0)
            array = []
            for point in serie.getElementsByTagName('points')[0].getElementsByTagName('point'):
                array.append(float(point.getAttribute('Y')))
            data_1[name] = array

        file_2 = xml.dom.minidom.parse(yellow_file)
        root_2 = file_2.documentElement
        data_2 = {}
        series = root_2.getElementsByTagName('series')
        for serie in series:
            name = re.search(r'([Hh][Cc][vV]-\S*)',
                             serie.getAttribute('title')).group(0)
            array = []
            for point in serie.getElementsByTagName('points')[0].getElementsByTagName('point'):
                array.append(float(point.getAttribute('Y')))
            data_2[name] = array
    except AttributeError:
        not_complete.append('File chạy không chứa mẫu tên HCV')

    else:
        for k, name in list(enumerate(data_1)):
            try:
                pt = HCVSample.objects.get(lab_id=name)
                js_data = {"green": data_1[name], "yellow": data_2[name]}
                js = json.dumps(js_data)
                pt.curves = js
                pt.save()

                completed.append(name)
            except(HCVSample.DoesNotExist, ObjectDoesNotExist):

                not_complete.append(name)
            except KeyError:
                not_complete.append('Hai files chạy không khớp nhau')
    for id_ in completed:
        obj = HCVSample.objects.get(lab_id = id_)
        print(obj.pk)
        c,i = create_HCV_image(obj.pk)
    
    return completed, not_complete

def create_HCV_report(pk = None):
    obj = HCVSample.objects.get(pk = pk)
    completed = ""
    incompleted = ""
    try:
        desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        today_folder =  "D:/Result/" + datetime.now().strftime("%m%d")
        if not os.path.exists(today_folder):
            os.makedirs(today_folder, exist_ok = True)
        try:
            print(obj.sid)
            sid_short = re.search(r"\d+-(\d{4})", obj.sid).groups()[0]

        except (AttributeError, TypeError):
            sid_short = ""
        file_name = today_folder +"/" + sid_short + '-' + no_accent_vietnamese(obj.name.replace(" ",'')) + '-' +obj.lab_id+'.docx'
        pic_file = settings.STATIC_DIR + "/run_img/" + obj.lab_id + '_amp.png'
        if obj.sid == None:
            sid = ""
        else:
            sid = str(obj.sid)
        
        if obj.age != None:
            age = str(obj.age)
        else:
            age = ""
        #start merging
        f_1 = MailMerge(settings.STATIC_DIR + '/word_template/HCV FORM.docx')
        f_1.merge(
            sid = sid, 
            lab_id = str(obj.lab_id), 
            sex = obj.sex, 
            doctor = obj.doctor, 
            addres = obj.address, 
            age = age, 
            name = obj.name, 
            date_receive = obj.added.strftime('%d/%m/%Y'), 
            date_finished = obj.modified.strftime('%d/%m/%Y-%H:%M'), 
            d= datetime.now().strftime("%d"), 
            m= datetime.now().strftime('%m'), 
            y= datetime.now().strftime('%Y'))      
        if obj.result == "DƯỚI NGƯỠNG PHÁT HIỆN":
            f_1.merge(iu = "DƯỚI NGƯỠNG PHÁT HIỆN")
        elif obj.copies != None:        
            try:            
                f_1.merge(
                copies =  "{:.1E}".format(Decimal(obj.copies*obj.std_curve.factor)),
                iu = "{:.1E}".format(Decimal(obj.copies*obj.std_curve.factor/5)),
                log = "{:.1f}".format(math.log10(obj.copies*obj.std_curve.factor)))
            except:
                print('ERROR')

        f_1.write(file_name)

        doc = Document(file_name)
        for paragraph in doc.paragraphs:
            if r"None" in paragraph.text:
                print('YES NONE IS HERE')
                paragraph.text = paragraph.text.strip().replace("None", "")
            if "[image]" in paragraph.text:
                paragraph.text = paragraph.text.strip().replace("[image]", "")

                run = paragraph.add_run()
                run.add_picture(pic_file, width=Cm(15))
                paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        doc.save(file_name)
        completed = obj.lab_id + " vào " + today_folder
    except FileNotFoundError:
        incompleted = "Chưa có file hình " + obj.lab_id
    except:
        incompleted = obj.lab_id
    return completed, incompleted

#CTNG FUNCTIONS
def create_CTNG_image(pk = None):
    f = open('result/ctng_neg.json')
    ctng_neg = json.load(f)
    cycles = np.arange(1, 41)
    obj = get_object_or_404(CTNGSample, pk = pk)
    curves = json.loads(obj.curves)
    completed = ""
    incompleted = ""
    fig, (ax1,ax2) = plt.subplots(1,2)
    fig.set_size_inches(10, 4)
    
    ax1.plot(cycles, pd.DataFrame(ctng_neg['green']),label = 'N. gonorrhoeae', c = 'blue', marker = "s", markersize = 3)
    ax1.plot(cycles, pd.DataFrame(ctng_neg['yellow']),label = 'Chứng nội', c = 'green', marker = "o", markersize = 3)
    ax1.plot(cycles, pd.DataFrame(ctng_neg['orange']),label = 'C.trachomatis', c = 'red', marker = "<",  markersize = 3)
   
    #ax1.plot(cycles, pd.DataFrame(data_2[item[1]]), label = item[1], c = 'red', linewidth = 2.3)
    #ax1.plot(cycles, pd.DataFrame(data_3[item[1]]), label = 'Chứng nội ' + str(item[1]), c = 'green', alpha = 0.7, marker = '+', markersize = 3)
    ax1.legend()
    ax1.set_xlabel('Cycles')
    ax1.set_ylabel('Normalized Fluorescence')
    ax1.set_ylim(ymax = 0.8)

    ax1.set_title('Mẫu âm tính')
    ax1.grid(linestyle = ':', alpha = 0.5)

    
    ax2.plot(cycles, pd.DataFrame(curves['green']),label = 'N. gonorrhoeae', c = 'blue', marker = "s", markersize = 3)
    ax2.plot(cycles, pd.DataFrame(curves['yellow']),label = 'Chứng nội', c = 'green', marker = "o", markersize = 3)
    ax2.plot(cycles, pd.DataFrame(curves['orange']),label = 'C.trachomatis', c = 'red', marker = "<",  markersize = 3)
    
    ax2.legend()
    ax2.set_title(r"Mẫu " + obj.lab_id)
    ax2.set_xlabel('Cycles')
    ax2.set_ylabel('Normalized Fluorescence')
    ax2.grid(linestyle = ':', alpha = 0.5)
    if ax2.get_ylim()[1] < 0.5:
        ax2.set_ylim(ymax = 0.8)
    fig.tight_layout(h_pad = 3)
    props = dict(boxstyle='round', alpha=0)
    name = "static/run_img/" + obj.lab_id + '-VA.png'
    fig.savefig(name, type = 'png', bbox_inches = 'tight', dpi= 100)
    completed += obj.lab_id
    return completed, incompleted

def process_CTNG_runfile(green_file, orange_file, yellow_file):
    completed = []
    not_complete = []    
    try:
        file_1 = xml.dom.minidom.parse(green_file)
        root_1 = file_1.documentElement
        data_1 = {}
        series = root_1.getElementsByTagName('series')
        for serie in series:
            name = re.search(r'([Cc][Tt][Nn][Gg]-\S*)',
                             serie.getAttribute('title')).group(0)
            array = []
            for point in serie.getElementsByTagName('points')[0].getElementsByTagName('point'):
                array.append(float(point.getAttribute('Y')))
            data_1[name] = array

        file_2 = xml.dom.minidom.parse(yellow_file)
        root_2 = file_2.documentElement
        data_2 = {}
        series = root_2.getElementsByTagName('series')
        for serie in series:
            name = re.search(r'([Cc][Tt][Nn][Gg]-\S*)',
                             serie.getAttribute('title')).group(0)
            array = []
            for point in serie.getElementsByTagName('points')[0].getElementsByTagName('point'):
                array.append(float(point.getAttribute('Y')))
            data_2[name] = array
        
        file_3 = xml.dom.minidom.parse(orange_file)
        root_3 = file_3.documentElement
        data_3 = {}
        series = root_3.getElementsByTagName('series')
        for serie in series:
            name = re.search(r'([Cc][Tt][Nn][Gg]-\S*)',
                             serie.getAttribute('title')).group(0)
            array = []
            for point in serie.getElementsByTagName('points')[0].getElementsByTagName('point'):
                array.append(float(point.getAttribute('Y')))
            data_3[name] = array
    except AttributeError:
        not_complete.append('File chạy không chứa mẫu tên CTNG')

    else:
        for k, name in list(enumerate(data_1)):
            try:
                pt = CTNGSample.objects.get(lab_id=name)
                js_data = {"green": data_1[name], "yellow": data_2[name], "orange": data_3[name]}
                js = json.dumps(js_data)
                pt.curves = js
                pt.save()

                completed.append(name)
            except(CTNGSample.DoesNotExist, ObjectDoesNotExist):

                not_complete.append(name)
            except KeyError:
                not_complete.append('Hai files chạy không khớp nhau')
    for id_ in completed:
        obj = CTNGSample.objects.get(lab_id = id_)
        print(obj.pk)
        c,i = create_CTNG_image(obj.pk)
    
    return completed, not_complete

def create_CTNG_report(pk = None):
    obj = CTNGSample.objects.get(pk = pk)
    completed = ""
    incompleted = ""
    #try:
    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    today_folder =  "D:/Result/" + datetime.now().strftime("%m%d")
    if not os.path.exists(today_folder):
        os.makedirs(today_folder, exist_ok = True)
    try:
        print(obj.sid)
        sid_short = re.search(r"\d+-(\d{4})", obj.sid).groups()[0]

    except (AttributeError, TypeError):
        sid_short = ""
    file_name = today_folder +"/" + sid_short + '-' + no_accent_vietnamese(obj.name.replace(" ",'')) + '-' +obj.lab_id+'.docx'
    pic_file = settings.STATIC_DIR + "/run_img/" + obj.lab_id + '-VA.png'
    if obj.sid == None:
        sid = ""
    else:
        sid = str(obj.sid)
    
    if obj.age != None:
        age = str(obj.age)
    else:
        age = ""
    result_ct_neg = ''
    result_ct_pos = ''
    result_ng_neg = ''
    result_ng_pos = ''
    if obj.result_ct == 'ÂM TÍNH':
        result_ct_neg = 'ÂM TÍNH'
    else:
        result_ct_pos = 'DƯƠNG TÍNH'

    if obj.result_ng == 'ÂM TÍNH':
        result_ng_neg = 'ÂM TÍNH'
    else:
        result_ng_pos = 'DƯƠNG TÍNH'
    print(obj.modified.strftime('%d/%m/%Y-%H:%M'))
    #start merging
    f_1 = MailMerge(settings.STATIC_DIR + '/word_template/CTNG FORM.docx')
    f_1.merge(
        sid = sid, 
        lab_id = str(obj.lab_id), 
        sex = obj.sex, 
        doctor = obj.doctor, 
        addres = obj.address, 
        age = age, 
        name = obj.name, 
        date_receive = obj.added.strftime('%d/%m/%Y'), 
        date_finished = obj.modified.strftime('%d/%m/%Y-%H:%M'), 
        d= datetime.now().strftime("%d"), 
        m= datetime.now().strftime('%m'), 
        y= datetime.now().strftime('%Y'),
        result_ct_neg = result_ct_neg,
        result_ct_pos = result_ct_pos,
        result_ng_pos = result_ng_pos,
        result_ng_neg = result_ng_neg,
        sample_type = obj.sample_type
        )     


    f_1.write(file_name)

    doc = Document(file_name)
    for paragraph in doc.paragraphs:
        if r"None" in paragraph.text:
            print('YES NONE IS HERE')
            paragraph.text = paragraph.text.strip().replace("None", "")
        if "[image]" in paragraph.text:
            paragraph.text = paragraph.text.strip().replace("[image]", "")

            run = paragraph.add_run()
            run.add_picture(pic_file, width=Cm(15))
            paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    doc.save(file_name)
    completed = obj.lab_id + " vào " + today_folder
    '''
    except FileNotFoundError:
        incompleted = "Chưa có file hình " + obj.lab_id
    except:
        incompleted = obj.lab_id'''
    return completed, incompleted

#HPV FUNCTIONS
def create_HPV_image(pk = None):
    
    cycles = np.arange(1, 41)
    obj = get_object_or_404(HPVSample, pk = pk)
    curves = json.loads(obj.curves)
    completed = ""
    incompleted = ""
    if obj.test_kit == "KT":
        f = open('result/hpv_neg_kt.json')
        hpv_neg = json.load(f)
        fig, (ax1,ax2) = plt.subplots(1,2)
        fig.set_size_inches(10, 4)
        
        ax1.plot(cycles, pd.DataFrame(hpv_neg['green']),label = 'HPV-16', c = 'green', marker = "s", markersize = 3)
        ax1.plot(cycles, pd.DataFrame(hpv_neg['yellow']),label = 'HPV-18', c = '#2142FF', marker = "o", markersize = 3)
        ax1.plot(cycles, pd.DataFrame(hpv_neg['orange']),label = 'HPV High Risk', c = '#FF8600', marker = "<",  markersize = 3)
        ax1.plot(cycles, pd.DataFrame(hpv_neg['red']),label = 'Chứng nội', c = '#E80D0C', marker = 'x', markersize = 3)

        ax1.legend()
        ax1.set_xlabel('Cycles')
        ax1.set_ylabel('Normalized Fluorescence')
        ax1.set_ylim(ymax = 1.0)

        ax1.set_title('Mẫu âm tính')
        ax1.grid(linestyle = ':', alpha = 0.5)
        
        ax2.plot(cycles, pd.DataFrame(curves['green']),label = 'HPV-16', c = 'green', marker = "s", markersize = 3)
        ax2.plot(cycles, pd.DataFrame(curves['yellow']),label = 'HPV-18', c = '#2142FF', marker = "o", markersize = 3)
        ax2.plot(cycles, pd.DataFrame(curves['orange']),label = 'HPV High Risk', c = '#FF8600', marker = "<",  markersize = 3)
        ax2.plot(cycles, pd.DataFrame(curves['red']),label = 'Chứng nội', c = '#E80D0C', marker = 'x', markersize = 3)
        ax2.legend()
        ax2.set_title(r"Mẫu " + obj.lab_id)
        ax2.set_xlabel('Cycles')
        ax2.set_ylabel('Normalized Fluorescence')
        ax2.grid(linestyle = ':', alpha = 0.5)
        
        if ax2.get_ylim()[1] < 0.5:
            ax2.set_ylim(ymax = 0.5)
        
        fig.tight_layout(h_pad = 3)
        props = dict(boxstyle='round', alpha=0)
        name = "static/run_img/" + obj.lab_id+ '-KT.png'
        fig.savefig(name, type = 'png', bbox_inches = 'tight', dpi= 100)
        completed += obj.lab_id
        f.close()

    elif obj.test_kit == "VA":
        fig = plt.figure()    
        plt.plot(cycles, pd.DataFrame(curves['green']),label = 'HPV-DNA', c = 'red', marker = "s", markersize = 3)
        plt.plot(cycles, pd.DataFrame(curves['yellow']),label = 'Chứng nội', c = 'green', marker = "o", markersize = 3)
        
        plt.legend()
        plt.title(r"Mẫu " + obj.lab_id)
        plt.xlabel('Cycles')
        plt.ylabel('Normalized Fluorescence')
        plt.grid(linestyle = ':', alpha = 0.5)
        #ax2.set_ylim()
        fig.tight_layout(h_pad = 3)
        props = dict(boxstyle='round', alpha=0)
        name = "static/run_img/" + obj.lab_id + '-VA.png'
        fig.savefig(name, type = 'png', bbox_inches = 'tight', dpi= 100)
        completed += obj.lab_id
    elif obj.test_kit == "KT_611":
        f = open('result/hpv_neg_kt.json')
        hpv_neg = json.load(f)
        fig, (ax1,ax2) = plt.subplots(1,2)
        fig.set_size_inches(10, 4)
        
        ax1.plot(cycles, pd.DataFrame(hpv_neg['green']),label = 'HPV-16', c = 'green', marker = "s", markersize = 3)
        ax1.plot(cycles, pd.DataFrame(hpv_neg['yellow']),label = 'HPV-18', c = '#2142FF', marker = "o", markersize = 3)
        ax1.plot(cycles, pd.DataFrame(hpv_neg['orange']),label = 'HPV High Risk', c = '#FF8600', marker = "<",  markersize = 3)
        ax1.plot(cycles, pd.DataFrame(hpv_neg['red']),label = 'Chứng nội', c = '#E80D0C', marker = 'x', markersize = 3)
        ax1.plot(cycles, pd.DataFrame(hpv_neg['green_2']),label = 'HPV-6', c = '#460656', marker = "4",  markersize = 3)
        ax1.plot(cycles, pd.DataFrame(hpv_neg['yellow_2']),label = 'HPV-11', c = '#10073a', marker = "d",  markersize = 3)

        ax1.legend()
        ax1.set_xlabel('Cycles')
        ax1.set_ylabel('Normalized Fluorescence')
        ax1.set_ylim(ymax = 1.0)

        ax1.set_title('Mẫu âm tính')
        ax1.grid(linestyle = ':', alpha = 0.5)
        
        ax2.plot(cycles, pd.DataFrame(curves['green']),label = 'HPV-16', c = 'green', marker = "s", markersize = 3)
        ax2.plot(cycles, pd.DataFrame(curves['yellow']),label = 'HPV-18', c = '#2142FF', marker = "o", markersize = 3)
        ax2.plot(cycles, pd.DataFrame(curves['orange']),label = 'HPV High Risk', c = '#FF8600', marker = "<",  markersize = 3)
        ax2.plot(cycles, pd.DataFrame(curves['red']),label = 'Chứng nội', c = '#E80D0C', marker = 'x', markersize = 3)
        ax2.plot(cycles, pd.DataFrame(curves['green_2']),label = 'HPV-6', c = '#460656', marker = "4",  markersize = 3)
        ax2.plot(cycles, pd.DataFrame(curves['yellow_2']),label = 'HPV-11', c = '#10073a', marker = "d",  markersize = 3)
        ax2.legend()
        ax2.set_title(r"Mẫu " + obj.lab_id)
        ax2.set_xlabel('Cycles')
        ax2.set_ylabel('Normalized Fluorescence')
        ax2.grid(linestyle = ':', alpha = 0.5)
        
        if ax2.get_ylim()[1] < 0.5:
            ax2.set_ylim(ymax = 0.5)
        
        fig.tight_layout(h_pad = 3)
        props = dict(boxstyle='round', alpha=0)
        name = "static/run_img/" + obj.lab_id+ '-KTPLUS.png'
        fig.savefig(name, type = 'png', bbox_inches = 'tight', dpi= 100)
        completed += obj.lab_id
        f.close()

    return completed, incompleted

def process_HPV_runfile(green_file, yellow_file, orange_file = None, red_file = None, green_file_2 = None, yellow_file_2 = None):
    completed = []
    not_complete = []    
    try:
        file_1 = xml.dom.minidom.parse(green_file)
        root_1 = file_1.documentElement
        data_1 = {}
        series = root_1.getElementsByTagName('series')
        for serie in series:
            name = re.search(r'([Hh][Pp][Vv]-\S*)',
                             serie.getAttribute('title')).group(0)
            array = []
            for point in serie.getElementsByTagName('points')[0].getElementsByTagName('point'):
                array.append(float(point.getAttribute('Y')))
            data_1[name] = array

        file_2 = xml.dom.minidom.parse(yellow_file)
        root_2 = file_2.documentElement
        data_2 = {}
        series = root_2.getElementsByTagName('series')
        for serie in series:
            name = re.search(r'([Hh][Pp][Vv]-\S*)',
                             serie.getAttribute('title')).group(0)
            array = []
            for point in serie.getElementsByTagName('points')[0].getElementsByTagName('point'):
                array.append(float(point.getAttribute('Y')))
            data_2[name] = array
        if orange_file != None:
            file_3 = xml.dom.minidom.parse(orange_file)
            root_3 = file_3.documentElement
            data_3 = {}
            series = root_3.getElementsByTagName('series')
            for serie in series:
                name = re.search(r'([Hh][Pp][Vv]-\S*)',
                                serie.getAttribute('title')).group(0)
                array = []
                for point in serie.getElementsByTagName('points')[0].getElementsByTagName('point'):
                    array.append(float(point.getAttribute('Y')))
                data_3[name] = array
        if red_file != None:
            file_4 = xml.dom.minidom.parse(red_file)
            root_4 = file_4.documentElement
            data_4 = {}
            series = root_4.getElementsByTagName('series')
            for serie in series:
                name = re.search(r'([Hh][Pp][Vv]-\S*)',
                                serie.getAttribute('title')).group(0)
                array = []
                for point in serie.getElementsByTagName('points')[0].getElementsByTagName('point'):
                    array.append(float(point.getAttribute('Y')))
                data_4[name] = array
        if green_file_2 != None:
            file_5 = xml.dom.minidom.parse(green_file_2)
            root_5 = file_5.documentElement
            data_5 = {}
            series = root_5.getElementsByTagName('series')
            for serie in series:
                name = re.search(r'([Hh][Pp][Vv]-\S*)',
                                serie.getAttribute('title')).group(0)
                array = []
                for point in serie.getElementsByTagName('points')[0].getElementsByTagName('point'):
                    array.append(float(point.getAttribute('Y')))
                data_5[name] = array
        
        if yellow_file_2 != None:
            file_6 = xml.dom.minidom.parse(yellow_file_2)
            root_6 = file_6.documentElement
            data_6 = {}
            series = root_6.getElementsByTagName('series')
            for serie in series:
                name = re.search(r'([Hh][Pp][Vv]-\S*)',
                                serie.getAttribute('title')).group(0)
                array = []
                for point in serie.getElementsByTagName('points')[0].getElementsByTagName('point'):
                    array.append(float(point.getAttribute('Y')))
                data_6[name] = array
    except AttributeError:
        not_complete.append('File chạy không chứa mẫu tên HPV')

    else:
        for k, name in list(enumerate(data_1)):
            try:
                pt = HPVSample.objects.get(lab_id=name)
                js_data = {"green": data_1[name], "yellow": data_2[name]}
                if orange_file != None:
                    js_data['orange'] = data_3[name]
                if red_file != None:
                    js_data['red'] = data_4[name]
                if green_file_2 != None:
                    js_data['green_2'] = data_5[name]
                if yellow_file_2 != None:
                    js_data['yellow_2'] = data_6[name]
                js = json.dumps(js_data)

                pt.curves = js

                pt.save()

                completed.append(name)
            except(HPVSample.DoesNotExist, ObjectDoesNotExist):

                not_complete.append(name)
            except KeyError:
                not_complete.append('Hai files chạy không khớp nhau')
    for id_ in completed:
        obj = HPVSample.objects.get(lab_id = id_)
        print(obj.pk)
        c,i = create_HPV_image(obj.pk)
    
    return completed, not_complete

def create_HPV_report(pk = None):
    obj = HPVSample.objects.get(pk = pk)
    completed = ""
    incompleted = ""
    #try:
    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    today_folder =  "D:/Result/" + datetime.now().strftime("%m%d")
    if not os.path.exists(today_folder):
        os.makedirs(today_folder, exist_ok = True)
    try:
        print(obj.sid)
        sid_short = re.search(r"\d+-(\d{4})", obj.sid).groups()[0]

    except (AttributeError, TypeError):
        sid_short = ""
    file_name = today_folder +"/" + sid_short + '-' + no_accent_vietnamese(obj.name.replace(" ",'')) + '-' +obj.lab_id+'.docx'
    
    if obj.sid == None:
        sid = ""
    else:
        sid = str(obj.sid)
    if obj.age != None:
        age = str(obj.age)
    else:
        age = ""
    if obj.test_kit == "KT":
        pic_file = "static/run_img/" + obj.lab_id + "-KT.png"
        result_16_neg = ""
        result_16_pos = ""
        result_18_neg = ""
        result_18_pos = ""
        result_hr_neg = ""
        result_hr_pos = ""

        if obj.result_16_kt == "DƯƠNG TÍNH":
            result_16_pos = "DƯƠNG TÍNH"
        else: 
            result_16_neg = "ÂM TÍNH"

        if obj.result_18_kt == "DƯƠNG TÍNH":
            result_18_pos = "DƯƠNG TÍNH"
        else: 
            result_18_neg = "ÂM TÍNH"

        if obj.result_hr_kt == "DƯƠNG TÍNH":
            result_hr_pos = "DƯƠNG TÍNH"
        else: 
            result_hr_neg = "ÂM TÍNH"
        f_1 = MailMerge('static/word_template/HPV FORM.docx')
        f_1.merge(
            sid = obj.sid,
            lab_id = " " + obj.lab_id, 
            result_18_neg = result_18_neg,
            result_18_pos = result_18_pos,
            result_16_pos = result_16_pos,
            result_16_neg = result_16_neg,
            result_hr_pos = result_hr_pos,
            result_hr_neg = result_hr_neg,
            sex = obj.sex,
            doctor =obj.doctor, 
            address = obj.address, 
            age = age, 
            name = obj.name, 
            date_receive = obj.added.strftime('%d/%m/%Y'), 
            date_finished = obj.modified.strftime('%d/%m/%Y-%H:%M'), 
            d= datetime.now().strftime("%d"), 
            m= datetime.now().strftime('%m'), 
            y= datetime.now().strftime('%Y'))
    
        f_1.write(file_name)
        
        

        doc = Document(file_name)
        for paragraph in doc.paragraphs:
            if "[image]" in paragraph.text:
                paragraph.text = paragraph.text.strip().replace("[image]", "")

                run = paragraph.add_run()
                run.add_picture(pic_file, width=Cm(15))
                paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        doc.save(file_name)
        completed = obj.lab_id + " vào " + today_folder

    elif obj.test_kit == "VA":
        pic_file = "static/run_img/" + obj.lab_id + "-VA.png"
        result_hpv_neg = ""
        result_hpv_pos = ""
        result_geno_pos = ""
        result_geno_neg = ""

        if obj.result_qual_va == "DƯƠNG TÍNH":
            result_hpv_pos = "DƯƠNG TÍNH"
            result_geno_pos = obj.result_type_va
        else:
            result_hpv_neg = "ÂM TÍNH"        
            result_geno_neg = "ÂM TÍNH"
        f_1 = MailMerge('static/word_template/HPV FORM VA.docx')
        f_1.merge(
        sid = obj.sid,
        lab_id = " " + obj.lab_id, 
        result_hpv_neg = result_hpv_neg,
        result_hpv_pos = result_hpv_pos,
        result_geno_pos = result_geno_pos,
        result_geno_neg = result_geno_neg,
        sample_type = obj.sample_type,
        sex = obj.sex, 
        doctor = obj.doctor, 
        address = obj.address, 
        age = age, 
        name = obj.name, 
        date_receive = obj.added.strftime('%d/%m/%Y'), 
        date_finished = obj.modified.strftime('%d/%m/%Y-%H:%M'), 
        d= datetime.now().strftime("%d"), 
        m= datetime.now().strftime('%m'), 
        y= datetime.now().strftime('%Y'))
        f_1.write(file_name)      
        
        doc = Document(file_name)
        for paragraph in doc.paragraphs:
            if "[image]" in paragraph.text:
                paragraph.text = paragraph.text.strip().replace("[image]", "")
                run = paragraph.add_run()
                run.add_picture(pic_file, width=Cm(8.5))
                run.add_picture('static/run_img/valayout.gif', width=Cm(3.8))
                if obj.result_qual_va == "ÂM TÍNH":                    
                    run.add_picture('static/run_img/hpv neg.jpg', width = Cm(3.8))
                elif obj.result_qual_va == "DƯƠNG TÍNH":
                    run.add_picture(obj.img_va, width = Cm(3.8))
                paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        doc.save(file_name)
        completed = obj.lab_id + " vào " + today_folder

    if obj.test_kit == "KT_611":
        pic_file = "static/run_img/" + obj.lab_id + "-KTPLUS.png"
        result_16_neg = ""
        result_16_pos = ""
        result_18_neg = ""
        result_18_pos = ""
        result_hr_neg = ""
        result_hr_pos = ""
        result_6_neg = ""
        result_6_pos = ""
        result_11_neg = ""
        result_11_pos = ""

        if obj.result_16_kt == "DƯƠNG TÍNH":
            result_16_pos = "DƯƠNG TÍNH"
        else: 
            result_16_neg = "ÂM TÍNH"

        if obj.result_18_kt == "DƯƠNG TÍNH":
            result_18_pos = "DƯƠNG TÍNH"
        else: 
            result_18_neg = "ÂM TÍNH"

        if obj.result_hr_kt == "DƯƠNG TÍNH":
            result_hr_pos = "DƯƠNG TÍNH"
        else: 
            result_hr_neg = "ÂM TÍNH"

        if obj.result_6_kt == "DƯƠNG TÍNH":
            result_6_pos = "DƯƠNG TÍNH"
        else: 
            result_6_neg = "ÂM TÍNH"

        if obj.result_11_kt == "DƯƠNG TÍNH":
            result_11_pos = "DƯƠNG TÍNH"
        else: 
            result_11_neg = "ÂM TÍNH" 
        f_1 = MailMerge('static/word_template/HPV611 FORM.docx')
        f_1.merge(
            sid = obj.sid,
            lab_id = " " + obj.lab_id, 
            result_18_neg = result_18_neg,
            result_18_pos = result_18_pos,
            result_16_pos = result_16_pos,
            result_16_neg = result_16_neg,
            result_hr_pos = result_hr_pos,
            result_hr_neg = result_hr_neg,
            result_6_pos = result_6_pos,
            result_6_neg = result_6_neg,
            result_11_pos = result_11_pos,
            result_11_neg = result_11_neg,
            sex = obj.sex,
            doctor =obj.doctor, 
            address = obj.address, 
            age = age, 
            name = obj.name, 
            date_receive = obj.added.strftime('%d/%m/%Y'), 
            date_finished = obj.modified.strftime('%d/%m/%Y-%H:%M'), 
            d= datetime.now().strftime("%d"), 
            m= datetime.now().strftime('%m'), 
            y= datetime.now().strftime('%Y'))
    
        f_1.write(file_name)
        
        

        doc = Document(file_name)
        for paragraph in doc.paragraphs:
            if "[image]" in paragraph.text:
                paragraph.text = paragraph.text.strip().replace("[image]", "")

                run = paragraph.add_run()
                run.add_picture(pic_file, width=Cm(15))
                paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        doc.save(file_name)
        completed = obj.lab_id + " vào " + today_folder
        
    '''
    except FileNotFoundError:
        incompleted = "Chưa có file hình " + obj.lab_id
    except:
        incompleted = obj.lab_id'''
    return completed, incompleted

def create_red_run():
	arr = [-0.0307022044209794, -0.0280913091964497, -0.0254804139719199, -0.0228695187473902, -0.0204225687144872, -0.0180861506800482, -0.0157451881149236, -0.0132951264573411, -0.010757233874206, -0.00831366353130584, -0.00600839059388634, -0.00393327891278045, -0.00194970935807219, 0.000107940355260816, 0.00241048122940581, 0.00488721428384435, 0.00740852208138584, 0.00981269750245809, 0.0119529693744361, 0.0138114563660028, 0.0155742208295958, 0.0177146635781359, 0.0208902330238241, 0.0262995110617809, 0.0359125335872005, 0.0530687239571791, 0.0822455264825406, 0.128130786654408, 0.193579836149974, 0.278116153074254, 0.376969566008115, 0.481960430558091, 0.583440025861203, 0.673036977339407, 0.745318703643666, 0.798278306493034, 0.835157142336628, 0.860241914617969, 0.885326686899309, 0.910411459180649]
	arr_2 = [num + random.uniform(-0.005, 0.005) for num in arr]
	return arr_2

def populate_HPV_result():
    data = {
        'green': np.random.uniform(-0.005, 0.005, 40).tolist(),
        'yellow': np.random.uniform(0.01, 0.015, 40).tolist(),
        'orange': np.random.uniform(-0.005, 0.005, 40).tolist(),
        'red': create_red_run(),
        'green_2': np.random.uniform(0.005, 0.009, 40).tolist(),
        'yellow_2': np.random.uniform(-0.005, 0.005, 40).tolist(),
    }
    data = json.dumps(data)
    return data
