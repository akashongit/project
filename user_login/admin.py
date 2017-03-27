from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Employee,department,leave_history,leave_statistics 
# Register your models here.
admin.site.unregister(Group)

class Empadmin(admin.ModelAdmin):
    list_display = ['__unicode__','department'
    ]
    class Meta:
        model = Employee

admin.site.register(Employee,Empadmin)

class depadmin(admin.ModelAdmin):
    list_display = ['__unicode__','depart','hod'
    ]
    class Meta:
        model = department
admin.site.register(department,depadmin)

class lev_his_admin(admin.ModelAdmin):
    list_display = ['__unicode__','startdate','enddate','leavetype','status'
    ]
    class Meta:
        model = leave_history
admin.site.register(leave_history,lev_his_admin)

class lev_stat_admin(admin.ModelAdmin):
    list_display = ['__unicode__']
    class Meta:
        model = leave_statistics
admin.site.register(leave_statistics,lev_stat_admin)