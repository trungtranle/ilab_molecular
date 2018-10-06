import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xml.dom.minidom
import re
from result.models import HBVSampleInfo
from django.core.exceptions import ObjectDoesNotExist

def process_HBV_runfile(green_file, yellow_file):
    completed = []
    not_complete = []
    try:
        file_1 = xml.dom.minidom.parse(green_file)
        root_1 = file_1.documentElement
        data_1 = {}
        series = root_1.getElementsByTagName('series')
        for serie in series:    
            name = re.search(r'([Hh][Bb][vV]-\S*)',serie.getAttribute('title')).group(0)
            array = []
            for point in serie.getElementsByTagName('points')[0].getElementsByTagName('point'):
                array.append(float(point.getAttribute('Y')))
            data_1[name] = array
        
        file_2 = xml.dom.minidom.parse(yellow_file)
        root_2 = file_2.documentElement
        data_2 = {}
        series = root_2.getElementsByTagName('series')
        for serie in series:    
            name = re.search(r'([Hh][Bb][vV]-\S*)',serie.getAttribute('title')).group(0)
            array = []
            for point in serie.getElementsByTagName('points')[0].getElementsByTagName('point'):
                array.append(float(point.getAttribute('Y')))
            data_2[name] = array
    except AttributeError:
        not_complete.append('File chạy không chứa mẫu tên HBV')
    
    else:
        for k, name in list(enumerate(data_1)):
            try:
                pt = HBVSampleInfo.objects.get(lab_id = name)
                pt.green_curve = data_1[name]
                pt.yellow_curve = data_2[name]
                pt.save()

                completed.append(name)
            except(HBVSampleInfo.DoesNotExist, ObjectDoesNotExist):

                not_complete.append(name)
            except KeyError:
                not_complete.append('Hai files chạy không khớp nhau')
    return completed, not_complete
   

