from django.db import models
from datetime import datetime
from django.contrib.postgres import fields


class HBVStdCurve(models.Model):
    name = models.CharField(max_length = 100, default = datetime.now().strftime('%Y-%m-%d'))
    e3 = fields.JSONField()
    e5 = fields.JSONField()
    e7 = fields.JSONField()
    std_curve = fields.JSONField()
    r_2 = models.FloatField()
    eff = models.FloatField()
    slope = models.FloatField()

    def __str__(self):
        return self.name


