from django.contrib import admin
from result.models import *
# Register your models here.

#class HBVAdmin(admin.ModelAdmin):
    list_display = ['lab_id', 'sid', 'name', 'age', 'result', 'ct', 'copies']
    list_filter = ['added', 'result']
    

#admin.site.register(HBVSample, HBVAdmin)
#admin.site.register(HBVStandardCurve)