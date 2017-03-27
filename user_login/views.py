from django.shortcuts import render,redirect
from .forms import loginform
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from user_login.forms import leave_approve
from .models import *
# from .models import Employee
# Create your views here.

class user_login(View):
        def get(self,request):
                form=loginform
                context={"form":form}
                template='user_login/login.html'
                return render(request,template,context)




        def post(self,request):
                # If the request is a HTTP POST, try to pull out the relevant information.
                # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
                # if request.user.is_authenticated:
                        # return redirect('/user/hello/')

                username = request.POST.get('username')
                password = request.POST.get('password')
                # print(username)
                # print(password)
                # Use Django's machinery to attempt to see if the username/password
                # combination is valid - a User object is returned if it is.
                user = authenticate(username=username, password=password)
                # If we have a User object, the details are correct.
                # If None (Python's way of representing the absence of a value), no user
                # with matching credentials was found.
                if user:
                        # Is the account active? It could have been disabled.
                        if user.is_active:
                                # If the account is valid and active, we can log the user in.
                                # We'll send the user back to the homepage.
                                login(request, user)
                                print(request.POST['username'],request.POST['password'],user.username)
                                return redirect('/user/hello/')
                        else:
                                # An inactive account was used - no logging in!
                                return HttpResponse("Your account is disabled.")
                else:
                        # Bad login details were provided. So we can't log the user in.
                        print("Invalid login details: {0}, {1}".format(username, password))
                        return HttpResponse("Invalid login details supplied.")

@login_required
def user_logout(request):
        # Since we know the user is logged in, we can now just log them out.
        logout(request)
        # Take the user back to the homepage.
        return HttpResponseRedirect('/user/login/')

def home(request):
        context={}
        template='user_login/welcome.html'
        return render(request,template,context)

@login_required
def userpage(request):
        profile = Employee.objects.get(user=request.user)
        if profile.user.is_staff==False:
                template='user_login/hello.html'
        else:
                template='user_login/super.html'
        print(request.user.get_username())
        return render(request,template,{'profile':profile})    
          
class leave_cancel(View):
        def get(self,request):
                deleted=False
                template = 'user_login/leave_cancel.html'
                profile = Employee.objects.get(user=request.user)
                profile = Employee.objects.get(user=request.user)
                history = leave_history.objects.filter(status=False)
                return render(request, template, {'profile': profile,'history':history,'deleted':deleted})

        def post(self,request):
                template='user_login/leave_cancel.html'
                profile = Employee.objects.get(user=request.user)
                if request.POST.get('delete')=='on':
                        print('success')
                        leaveid = request.POST.get('leaveid')
                        print(leaveid)
                        leaveid=int(leaveid)
                        # des = request.POST.get('des')
                        leave = leave_history.objects.get(id=leaveid)
                        leave_stat = leave_statistics.objects.get(user=profile.user)
                        if leave.leavetype=='cl':
                                leave_stat.casual+=int(leave_history.half_day*0.5)
                        else :
                                leave_stat.half_paid+=int(leave.half_day*0.5)
                        leave_stat.save()        
                        leave.delete()
                        deleted=False
                # history = leave_history.objects.filter(user=profile.user)
                return render(request,template,{'profile':profile,'deleted':deleted})


class leavehistory(View):
        def get(self,request):
                template = 'user_login/leave_history.html'
                profile = Employee.objects.get(user=request.user)       
                try:
                        history = leave_history.objects.filter(user=profile.user)                      
                except AttributeError:
                        print("error")
                return render(request, template, {'profile': profile,'history':history})

        def post(self,request):
                template = 'user_login/leave_history.html'
                profile = Employee.objects.get(user=request.user)
                return render(request,template,{'profile':profile,'history':history})

class check_status(View):
        def get(self,request):
                template = 'user_login/check_status.html'
                profile = Employee.objects.get(user=request.user)
                history = leave_history.objects.filter(status=False)
                return render(request, template, {'profile': profile,'history':history})

        def post(self,request):
                template='user_login/check_status.html'
                profile = Employee.objects.get(user=request.user)
                return render(request,template,{'profile':profile})

class statistics(View):
        def get(self,request):
                template = 'user_login/statistics.html'
                profile = Employee.objects.get(user=request.user)
                leave_stat=leave_statistics.objects.get(user=profile.user)
                return render(request, template, {'profile': profile,'leave':leave_stat})

        def post(self,request):
                template='user_login/statistics.html'
                profile = Employee.objects.get(user=request.user)
                return render(request,template,{'profile':profile})

class profile(View):
        def get(self,request):
                template = 'user_login/profile.html'
                profile = Employee.objects.get(user=request.user)
                return render(request, template, {'profile': profile})

        def post(self,request):
                template='user_login/profile.html'
                profile = Employee.objects.get(user=request.user)
                return render(request,template,{'profile':profile})

class pendingleave(View):
        def get(self,request):
                approved = False
                template = 'user_login/pending_leave.html'
                profile = Employee.objects.get(user=request.user)
                history = leave_history.objects.filter(status=False)
                # return render(request, template, {'profile': profile,'history':history})
                return render(request, template, {'profile': profile,'history':history,'approved':approved})

        def post(self,request):
                template='user_login/pending_leave.html'
                profile = Employee.objects.get(user=request.user)
                print('approve')
                if request.POST.get('approve')=='on':
                        print('success')
                        approved=False
                        leaveid = request.POST.get('leavetype')
                        print(leaveid)
                        leaveid=int(leaveid)
                        leave = leave_history.objects.get(id=leaveid)
                        leave.status=True
                        leave.save()
                        if leave.status==True:
                                approved=True
                return render(request,template,{'profile':profile,'approved':approved})

class empprofile(View):
        def get(self,request):
                template = 'user_login/emp_profile.html'
                profile = Employee.objects.get(user=request.user)
                searched=False
                return render(request, template, {'profile': profile,'searched':searched})
        def post(self,request):
                template='user_login/emp_profile.html'
                searched=False
                profile = Employee.objects.get(user=request.user)
                employee=request.POST.get('employee')
                employee=User.objects.get(username=employee)
                emp_profile=Employee.objects.get(user=employee)
                searched=True
                return render(request,template,{'profile':profile, 'searched':searched,'emp_profile':emp_profile})


