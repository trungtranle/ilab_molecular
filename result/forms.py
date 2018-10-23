from django import forms
from result.models import *
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.utils import timezone

current_month = datetime.now().strftime('%m') 

#HBV FORMS
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
    added = forms.DateField(initial = timezone.now(), widget = forms.SelectDateWidget, label = 'Ngày gửi mẫu')
    class Meta:
        model = HBVSample
        fields = ('sid', 'lab_id', 'name', 'age','address','sex','doctor','dx', 'added','clinic')
        
class HBVSampleForm(forms.ModelForm):
    result = forms.ChoiceField(choices=(("",""),('DƯƠNG TÍNH','DƯƠNG TÍNH'),('DƯỚI NGƯỠNG PHÁT HIỆN', 'DƯỚI NGƯỠNG PHÁT HIỆN')))
    sex = forms.ChoiceField(choices=[(" ",' '),('Nam','Nam'),('Nữ', 'Nữ'), ('Khác', 'Khác')], label = 'Giới tính')
    ct = forms.FloatField(label = 'Chu kỳ ngưỡng (Ct)', required = False)
    copies = forms.FloatField(label = 'Nồng độ (Copies/phản ứng) (Lấy số máy hiển thị)', required = False)
    class Meta:
        model = HBVSample
        fields = '__all__'

class HBVFileUpload(forms.Form):
    green_file = forms.FileField(label = 'File màu FAM (Green)')
    yellow_file = forms.FileField(label = 'File màu HEX (Yellow)')

#HCV FORMS
class HCVInfoForm(forms.ModelForm):
    hcv_id = 'HCV-'+ current_month + '-'
    lab_id = forms.CharField(max_length = 20, label = 'Lab ID', initial = hcv_id)
    sid = forms.CharField(max_length = 20, label = 'SID', required = False)
    name = forms.CharField(max_length = 100, label = 'Họ và tên', required = False)
    age = forms.CharField(max_length = 4, label = 'Tuổi', required = False)
    address = forms.CharField(max_length = 200, label = 'Địa chỉ', required = False)
    sex = forms.ChoiceField(choices=[(" ",' '),('Nam','Nam'),('Nữ', 'Nữ'), ('Khác', 'Khác')], label = 'Giới tính')
    doctor =forms.CharField(max_length = 100, required = False, label = 'Bác Sĩ')
    dx = forms.CharField(max_length = 100, required = False, label = 'Chẩn đoán')
    sample_type = forms.CharField(max_length = 100, initial = 'Máu', label = 'Loại mẫu')
    test_required = forms.CharField(max_length = 100, initial = 'HCV-RNA đo tải lượng bằng real-time RT PCR', label = 'Yêu cầu')
    added = forms.DateField(initial = timezone.now(), widget = forms.SelectDateWidget, label = 'Ngày gửi mẫu')
    class Meta:
        model = HCVSample
        fields = ('sid', 'lab_id', 'name', 'age','address','sex','doctor','dx', 'added','clinic')
        
class HCVSampleForm(forms.ModelForm):
    result = forms.ChoiceField(choices=(("",""),('DƯƠNG TÍNH','DƯƠNG TÍNH'),('DƯỚI NGƯỠNG PHÁT HIỆN', 'DƯỚI NGƯỠNG PHÁT HIỆN')))
    sex = forms.ChoiceField(choices=[(" ",' '),('Nam','Nam'),('Nữ', 'Nữ'), ('Khác', 'Khác')], label = 'Giới tính')
    ct = forms.FloatField(label = 'Chu kỳ ngưỡng (Ct)', required = False)
    copies = forms.FloatField(label = 'Nồng độ (Copies/phản ứng) (Lấy số máy hiển thị)', required = False)
    class Meta:
        model = HCVSample
        fields = '__all__'

class HCVFileUpload(forms.Form):
    green_file = forms.FileField(label = 'File màu FAM (Green)')
    yellow_file = forms.FileField(label = 'File màu HEX (Yellow)')

#CTNG FORMS
class CTNGInfoForm(forms.ModelForm):
    ctng_id = 'CTNG-'+ current_month + '-'
    lab_id = forms.CharField(max_length = 20, label = 'Lab ID', initial = ctng_id)
    sid = forms.CharField(max_length = 20, label = 'SID', required = False)
    name = forms.CharField(max_length = 100, label = 'Họ và tên', required = False)
    age = forms.CharField(max_length = 4, label = 'Tuổi', required = False)
    address = forms.CharField(max_length = 200, label = 'Địa chỉ', required = False)
    sex = forms.ChoiceField(choices=[('Nữ', 'Nữ'),('Nam','Nam'), ('Khác', 'Khác')], label = 'Giới tính')
    doctor =forms.CharField(max_length = 100, required = False, label = 'Bác Sĩ')
    dx = forms.CharField(max_length = 100, required = False, label = 'Chẩn đoán')
    sample_type = forms.ChoiceField(choices = [('Phết cổ tử cung','Phết cổ tử cung' ), ('Nước tiểu','Nước tiểu'), ('Phết niệu đạo', 'Phết niệu đạo'), ('Phết âm đạo','Phết âm đạo'), ('Phết vòm họng', 'Phết vòm họng'), ('Khác', 'Khác')], label = 'Loại mẫu')
    test_required = forms.CharField(max_length = 100, initial = 'CTNG', label = 'Yêu cầu')
    added = forms.DateField(initial = timezone.now(), widget = forms.SelectDateWidget, label = 'Ngày gửi mẫu')
    class Meta:
        model = CTNGSample
        fields = ('sid', 'lab_id', 'name', 'age','address','sex','doctor','dx', 'added','clinic')
        
class CTNGSampleForm(forms.ModelForm):
    result_ct = forms.ChoiceField(choices=(("",""),('DƯƠNG TÍNH','DƯƠNG TÍNH'),('ÂM TÍNH', 'ÂM TÍNH')))
    result_ng = forms.ChoiceField(choices=(("",""),('DƯƠNG TÍNH','DƯƠNG TÍNH'),('ÂM TÍNH', 'ÂM TÍNH')))
    sex = forms.ChoiceField(choices=[('Nữ', 'Nữ'), ('Nam','Nam'), ('Khác', 'Khác')], label = 'Giới tính')
    class Meta:
        model = CTNGSample
        fields = '__all__'

class CTNGFileUpload(forms.Form):
    green_file = forms.FileField(label = 'File màu FAM (Green)')
    yellow_file = forms.FileField(label = 'File màu HEX (Yellow)')
    orange_file = forms.FileField(label = 'File màu Texas Red (Orange)')

#HPV FORMS
class HPVInfoForm(forms.ModelForm):
    HPV_id = 'HPV-'+ current_month + '-'
    lab_id = forms.CharField(max_length = 20, label = 'Lab ID', initial = HPV_id)
    sid = forms.CharField(max_length = 20, label = 'SID', required = False)
    name = forms.CharField(max_length = 100, label = 'Họ và tên', required = False)
    age = forms.CharField(max_length = 4, label = 'Tuổi', required = False)
    address = forms.CharField(max_length = 200, label = 'Địa chỉ', required = False)
    sex = forms.ChoiceField(choices=[('Nữ', 'Nữ'),('Nam','Nam'), ('Khác', 'Khác')], label = 'Giới tính')
    doctor =forms.CharField(max_length = 100, required = False, label = 'Bác Sĩ')
    dx = forms.CharField(max_length = 100, required = False, label = 'Chẩn đoán')
    sample_type = forms.ChoiceField(choices = [('Phết cổ tử cung','Phết cổ tử cung' ), ('Phết vòm họng', 'Phết vòm họng'), ('Phết niệu đạo', 'Phết niệu đạo'), ('Phết âm đạo','Phết âm đạo'), ('Mẫu phết', 'Mẫu phết') , ('Khác', 'Khác')], label = 'Loại mẫu')
    test_kit = forms.ChoiceField(choices = [('KT','KHOA THƯƠNG'),('VA', 'VIỆT Á')], label = 'Loại kit')
    test_required = forms.CharField(max_length = 100, initial = 'HPV GENOTYPE', label = 'Yêu cầu')
    added = forms.DateField(initial = timezone.now(), widget = forms.SelectDateWidget, label = 'Ngày gửi mẫu')
    class Meta:
        model = HPVSample
        fields = ('sid', 'lab_id', 'name', 'age','address','sex','doctor','dx', 'added','clinic','test_kit')
        
class HPVSampleForm(forms.ModelForm):
    result_16_kt = forms.ChoiceField(choices=(("",""),('DƯƠNG TÍNH','DƯƠNG TÍNH'),('ÂM TÍNH', 'ÂM TÍNH')), label = 'HPV 16 KHOA THƯƠNG', required = False)
    result_18_kt = forms.ChoiceField(choices=(("",""),('DƯƠNG TÍNH','DƯƠNG TÍNH'),('ÂM TÍNH', 'ÂM TÍNH')), label = 'HPV 18 KHOA THƯƠNG', required = False)
    result_hr_kt = forms.ChoiceField(choices=(("",""),('DƯƠNG TÍNH','DƯƠNG TÍNH'),('ÂM TÍNH', 'ÂM TÍNH')), label = 'HPV HR KHOA THƯƠNG', required = False)
    result_qual_va = forms.ChoiceField(choices=(("",""),('DƯƠNG TÍNH','DƯƠNG TÍNH'),('ÂM TÍNH', 'ÂM TÍNH')), label = 'ĐỊNH TÍNH HPV VIỆT Á', required = False)
    result_type_va = forms.CharField(max_length = 100, label = 'ĐỊNH TYPE VIỆT Á', required = False)
   
    sex = forms.ChoiceField(choices=[('Nữ', 'Nữ'), ('Nam','Nam'), ('Khác', 'Khác')], label = 'Giới tính')
    img_va = forms.ImageField(required = None)
    class Meta:
        model = HPVSample
        fields = '__all__'

class HPVFileUpload(forms.Form):
    green_file = forms.FileField(label = 'File màu FAM (Green)')
    yellow_file = forms.FileField(label = 'File màu HEX (Yellow)')
    orange_file = forms.FileField(label = 'File màu ROX (Orange)', required = False)
    red_file = forms.FileField(label = 'File màu Cy5 (Red)', required = False)