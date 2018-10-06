from django.db import models
from datetime import datetime
from django.contrib.postgres import fields


class HBVStandardCurve(models.Model):
    name = models.CharField(max_length = 100, default = datetime.now().strftime('%Y-%m-%d'))
    
    std_curve = fields.JSONField()
    r_2 = models.FloatField()
    eff = models.FloatField()
    slope = models.FloatField()
    stds = fields.JSONField()


    def __str__(self):
        return self.name

class HBVSample(models.Model):
    lab_id = models.CharField(max_length = 50, unique_for_year = 'added')
    added = models.DateTimeField(auto_now_add= True)
    modified = models.DateTimeField(auto_now=True)
    sid = models.CharField(max_length = 50, unique_for_year = 'added')
    name = models.CharField(max_length = 100)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length = 10)
    address = models.CharField(max_length = 200)
    doctor = models.CharField(max_length = 100)
    dx = models.CharField(max_length = 400)
    result = models.CharField(max_length = 50)
    ct = models.FloatField()
    copies = models.FloatField()
    finished = models.BooleanField(default= False)
    curves = fields.JSONField()
    std_curve = models.ForeignKey(HBVStandardCurve, on_delete = models.PROTECT, default = HBVStandardCurve.objects.last())


