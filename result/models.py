from django.db import models
from datetime import datetime
from django.contrib.postgres import fields
from django.utils import timezone

#HBV MODELS
class HBVStandardCurve(models.Model):
    name = models.CharField(max_length = 100, default = datetime.now().strftime('%Y-%m-%d'))
    
    std_curve = fields.JSONField()
    r_2 = models.FloatField()
    eff = models.FloatField()
    slope = models.FloatField()
    stds = fields.JSONField()
    B = models.FloatField()
    factor = models.FloatField()


    def __str__(self):
        return self.name

def get_latest(model):
    return model.objects.last().pk

class HBVSample(models.Model):
    added = models.DateField(default = timezone.now)
    lab_id = models.CharField(max_length = 50, unique_for_year = 'added')
    created = models.DateTimeField(auto_now_add= True)
    modified = models.DateTimeField(auto_now=True)
    sid = models.CharField(max_length = 50, null = True, blank = True)
    name = models.CharField(max_length = 100, blank = True)
    age = models.CharField(max_length = 4, blank = True, null = True)
    sex = models.CharField(max_length = 10, blank = True)
    address = models.CharField(max_length = 200, blank = True)
    doctor = models.CharField(max_length = 100, blank = True)
    clinic = models.CharField(max_length = 100, verbose_name = 'Đơn vị gửi mẫu', null = True, blank = True)
    dx = models.CharField(max_length = 400, blank = True)
    result = models.CharField(max_length = 50, blank = True)
    ct = models.FloatField(blank = True, null = True)
    copies = models.FloatField(blank = True, null = True)
    finished = models.BooleanField(default= False)
    curves = fields.JSONField(blank = True, null = True)
    std_curve = models.ForeignKey(HBVStandardCurve, on_delete = models.PROTECT, default = get_latest(HBVStandardCurve))

    class Meta:
        ordering = ('-added',)
    def __str__(self):
        return self.lab_id + self.name

#HCV MODELS
class HCVStandardCurve(models.Model):
    name = models.CharField(max_length = 100, default = datetime.now().strftime('%Y-%m-%d'))    
    std_curve = fields.JSONField()
    r_2 = models.FloatField()
    eff = models.FloatField()
    slope = models.FloatField()
    stds = fields.JSONField()
    B = models.FloatField()
    factor = models.FloatField()

    def __str__(self):
        return self.name

class HCVSample(models.Model):
    added = models.DateField(default = timezone.now)
    lab_id = models.CharField(max_length = 50, unique_for_year = 'added')
    created = models.DateTimeField(auto_now_add= True)
    modified = models.DateTimeField(auto_now=True)
    sid = models.CharField(max_length = 50, null = True, blank = True)
    name = models.CharField(max_length = 100, blank = True)
    age = models.CharField(max_length = 4, blank = True, null = True)
    sex = models.CharField(max_length = 10, blank = True)
    address = models.CharField(max_length = 200, blank = True)
    doctor = models.CharField(max_length = 100, blank = True)
    clinic = models.CharField(max_length = 100, verbose_name = 'Đơn vị gửi mẫu', null = True, blank = True)
    dx = models.CharField(max_length = 400, blank = True)
    result = models.CharField(max_length = 50, blank = True)
    ct = models.FloatField(blank = True, null = True)
    copies = models.FloatField(blank = True, null = True)
    finished = models.BooleanField(default= False)
    curves = fields.JSONField(blank = True, null = True)
    std_curve = models.ForeignKey(HCVStandardCurve, on_delete = models.PROTECT, default = get_latest(HCVStandardCurve))

    class Meta:
        ordering = ('-added',)
    def __str__(self):
        return self.lab_id + self.name

class CTNGSample(models.Model):
    added = models.DateField(default = timezone.now)
    lab_id = models.CharField(max_length = 50, unique_for_year = 'added')
    created = models.DateTimeField(auto_now_add= True)
    modified = models.DateTimeField(auto_now=True)
    sid = models.CharField(max_length = 50, null = True, blank = True)
    name = models.CharField(max_length = 100, blank = True)
    age = models.CharField(max_length = 4, blank = True, null = True)
    sex = models.CharField(max_length = 10, blank = True)
    address = models.CharField(max_length = 200, blank = True)
    doctor = models.CharField(max_length = 100, blank = True)
    clinic = models.CharField(max_length = 100, verbose_name = 'Đơn vị gửi mẫu', null = True, blank = True)
    dx = models.CharField(max_length = 400, blank = True)
    sample_type = models.CharField(max_length = 100, blank = True)
    result_ct = models.CharField(max_length = 50, blank = True)
    result_ng = models.CharField(max_length = 50, blank = True)
    finished = models.BooleanField(default= False)
    curves = fields.JSONField(blank = True, null = True)
    

    class Meta:
        ordering = ('-added',)
    def __str__(self):
        return self.lab_id + self.name

class HPVSample(models.Model):
    added = models.DateField(default = timezone.now)
    lab_id = models.CharField(max_length = 50, unique_for_year = 'added')
    created = models.DateTimeField(auto_now_add= True)
    modified = models.DateTimeField(auto_now=True)
    sid = models.CharField(max_length = 50, null = True, blank = True)
    name = models.CharField(max_length = 100, blank = True)
    age = models.CharField(max_length = 4, blank = True, null = True)
    sex = models.CharField(max_length = 10, blank = True)
    address = models.CharField(max_length = 200, blank = True)
    doctor = models.CharField(max_length = 100, blank = True)
    clinic = models.CharField(max_length = 100, verbose_name = 'Đơn vị gửi mẫu', null = True, blank = True)
    dx = models.CharField(max_length = 400, blank = True)
    sample_type = models.CharField(max_length = 100, blank = True)
    test_kit = models.CharField(max_length = 50, blank = True, null = True)
    result_16_kt = models.CharField(max_length = 50, blank = True, null = True)
    result_18_kt = models.CharField(max_length = 50, blank = True, null = True)
    result_hr_kt = models.CharField(max_length = 50, blank = True, null = True)
    result_qual_va = models.CharField(max_length = 50, blank = True, null = True)
    result_type_va = models.CharField(max_length = 50, blank = True, null = True)
    img_va = models.ImageField(upload_to = "img")
    finished = models.BooleanField(default= False)
    curves = fields.JSONField(blank = True, null = True)
    

    class Meta:
        ordering = ('-added',)
    def __str__(self):
        return self.lab_id + self.name