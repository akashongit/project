from user_login.forms import leave_app_form
from django.views import View
from django.shortcuts import render,HttpResponse
from user_login.forms import UserForm,UserprofileForm
from .models import Employee,leave_statistics
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
import datetime
from django.core.mail import send_mail
from user_login.mail import *

today = datetime.date.today()

class leave_apply(View):
    # set to false initially as request is not submitted
    applied = False
    template=""
    def get(self,request):
        applied = False
        try:
            profile = Employee.objects.get(user=request.user)
        except TypeError:
            return HttpResponse('No user logged in:-(:-(<br>Please <a href="/user/login/">login</a>')
        if profile.user.is_authenticated:
            template="user_login/applyleave.html"
            leave_stat = leave_statistics.objects.get(user=profile.user)
            return render(request,template,{'profile':profile,'leave_app_form': leave_app_form, 'applied': applied,'leave':leave_stat} )

    def post(self,request):
        template="user_login/applyleave.html"
        # If it's a HTTP POST, we're interested in processing form data.
        # Attempt to grab information from the raw form information.
        leave_form = leave_app_form(data=request.POST)
        # retrieve user
        profile = Employee.objects.get(user=request.user)
        leave_stat=leave_statistics.objects.get(user=profile.user)
        # If the two forms are valid...
        try: 
            if leave_form.is_valid():
            # leave_form not saved
                leave_app = leave_form.save(commit=False)
            # setting user of leaveform
                leave_app.user=profile.user
                #returning the leave_history of that user to leave_stat
                # print(leave_app.user.get_username())
                # print(leave_stat.user.get_username())
                # print(leave_app.half_day)
                # print(leave_app.leavetype)
                d0 = leave_app.startdate
                d1 = leave_app.enddate
                if (d0-today).days<=0 and (d1-today).days<=0:
                    print('start or end date error')
                    applied=False
                    msg="Invalid start or end date!!"
                    return render(request,template,{'profile':profile,'leave_app_form': leave_app_form, 'applied': applied,'leave':leave_stat,'msg':msg} )
                delta = d1-d0
                days=delta.days
                if days<0:
                    applied=False
                    msg="Invalid start or end date!!"
                    return render(request,template,{'profile':profile,'leave_app_form': leave_app_form, 'applied': applied,'leave':leave_stat,'msg':msg})
                leave_app.half_day=days*2
                check_leave(leave_app=leave_app,leave_stat=leave_stat)
                # print(leave_stat.casual)
                leave_app.save()
                send_mail('Leave id %d submitted' % (leave_app.id),leaveapp %(leave_app.id,profile.user.username),'lilium366@gmail.com',['akashgeevarghese.mec@gmail.com','dvanisree3@gmail.com','albin.plathottathil@gmail.com','krishnatm84@gmail.com'],fail_silently=False,)
                

            return HttpResponse('Leave Application Successful!!')
            # return HttpResponse('Leave Application Successful!!')
        except ValueError:
            applied = False
            msg="Form error"
            return render(request,template,{'profile':profile,'leave_app_form': leave_app_form, 'applied': applied,'leave':leave_stat,'msg':msg} )

def check_leave(leave_app,leave_stat):
    flag=False
    leave={
        'cl','hp'
        }
    if leave_app.leavetype == 'cl':
        if leave_app.half_day < leave_stat.casual:
            leave_stat.casual-= leave_app.half_day
            flag=True

    elif leave_app.leavetype == 'hp':
        if leave_app.half_day < leave_stat.casual:
            leave_stat.half_paid-= leave_app.half_day
            flag=True
    leave_stat.save()
    if flag==False:
        return HttpResponse('Incorrect leave Application<br><a href="/user/apply_leave/">Redo</a>')     