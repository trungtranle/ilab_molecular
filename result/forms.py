"""from django import forms
from result.models import *
from datetime import datetime
from django.core.files.storage import FileSystemStorage
current_month = datetime.now().strftime('%m') 

class HBVInfoForm(forms.ModelForm):
    hbv_id = 'HBV-'+ current_month + '-'
    lab_id = forms.CharField(max_length = 20, label = 'Lab ID', initial = hbv_id)
    sid = forms.CharField(max_length = 20, label = 'SID', required = False)
    name = forms.CharField(max_length = 100, label = 'Họ và tên', required = False)
    age = forms.CharField(max_length = 4, label = 'Tuổi', required = False)
    address = forms.CharField(max_length = 200, label = 'Địa chỉ', required = False)
    sex = forms.ChoiceField(choices=[(" ",' '),('Nam','Nam'),('Nữ', 'Nữ'), ('Khác', 'Khác')], label = 'Giới tính')
    doctor =forms.CharField(max_length = 100, required = False, label = 'Bác Sĩ')
    dx = forms.CharField(max_length = 100, required = False, label = 'Chẩn đoán')
    sample_type = forms.CharField(max_length = 100, initial = 'Máu', label = 'Loại mẫu')
    test_required = forms.CharField(max_length = 100, initial = 'HBV-DNA đo tải lượng bằng real-time PCR', label = 'Yêu cầu')
    
    class Meta:
        model = HBVSampleInfo
        fields = ('sid', 'lab_id', 'name', 'age','address','sex','doctor','dx','sample_type','test_required')
        
class HBVSampleForm(forms.ModelForm):
    result = forms.ChoiceField(choices=(('DƯƠNG TÍNH','DƯƠNG TÍNH'),('HBV-DNA DƯỚI NGƯỠNG PHÁT HIỆN', 'DƯỚI NGƯỠNG PHÁT HIỆN'),('ÂM TÍNH','ÂM TÍNH')))
    sex = forms.ChoiceField(choices=[(" ",' '),('Nam','Nam'),('Nữ', 'Nữ'), ('Khác', 'Khác')], label = 'Giới tính')
    c_t = forms.FloatField(label = 'Chu kỳ ngưỡng (Ct)', required = False)
    concentration = forms.FloatField(label = 'Nồng độ (Copies/phản ứng) (Lấy số máy hiển thị)', required = False)
    class Meta:
        model = HBVSampleInfo
        fields = '__all__'

storage_HBV = FileSystemStorage(location='/runfile/HBV')
class HBVFileUpload(forms.Form):
    green_file = forms.FileField(label = 'File màu FAM (Green)')
    yellow_file = forms.FileField(label = 'File màu HEX (Yellow)')"""