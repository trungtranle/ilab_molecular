from django.contrib import admin
from result.models import *
# Register your models here.

class HBVAdmin(admin.ModelAdmin):
    list_display = ['lab_id', 'sid', 'name', 'age', 'result', 'ct', 'copies', 'added', 'modified']
    list_filter = ['added', 'result']
    
class HCVAdmin(admin.ModelAdmin):
    list_display = ['lab_id', 'sid', 'name', 'age', 'result', 'ct', 'copies', 'added', 'modified']
    list_filter = ['added', 'result']
#HBV REGISTER
admin.site.register(HBVSample, HBVAdmin)
admin.site.register(HBVStandardCurve)

#HCV REGISTER
admin.site.register(HCVSample, HCVAdmin)
admin.site.register(HCVStandardCurve)

admin.site.register(HPVSample)

