from django.contrib import admin
from result.models import *
# Register your models here.

'''class HBVAdmin(admin.ModelAdmin):
    list_display = ['lab_id', 'sid', 'name', 'age', 'result', 'c_t', 'concentration']
    list_filter = ['finished', 'result', 'date_receive']
    

admin.site.register(HBVSampleInfo, HBVAdmin)'''
#admin.site.register(HBVStandardCurve)