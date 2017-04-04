from django.shortcuts import render,redirect
from .forms import loginform
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from user_login.forms import leave_approve
from .models import *
from django.core.mail import send_mail
from user_login.mail import *

# from .models import Employee
# Create your views here.
admins=['akashgeevarghese.mec@gmail.com','dvanisree3@gmail.com','albin.plathottathil@gmail.com','krishnatm84@gmail.com']

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
                history = leave_history.objects.filter(user=profile.user,status=False)
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
                        try:        
                                if leave.leavetype=='cl':
                                        leave_stat.casual=leave_stat.casual+leave_history.half_day
                                else :
                                        leave_stat.half_paid=leave_stat.half_paid+(leave.half_day)
                        except TypeError:
                                pass
                                        
                                
                        leave_stat.save()        
                        leave.delete()
                        # send_mail('asasas','dsdsd','lilium366@gmail.com',['akashgeevarghese.mec@gmail.com'],fail_silently=False,)
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
                history = leave_history.objects.filter(user=profile.user,status=False)
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
                msg=""
                template = 'user_login/pending_leave.html'
                profile = Employee.objects.get(user=request.user)
                history = leave_history.objects.filter(status=False)
                # return render(request, template, {'profile': profile,'history':history})
                return render(request, template, {'profile': profile,'history':history,'approved':approved,'msg':msg})

        # def post(self,request):
                # template='user_login/pending_leave.html'
                # profile = Employee.objects.get(user=request.user)
                # print('approve')
                # if request.POST.get('approve')=='on' :
                #         print('success')
                #         approved=False
                #         leaveid = request.POST.get('leavetype')
                #         print(leaveid)
                #         leaveid=int(leaveid)
                #         leave = leave_history.objects.get(id=leaveid)
                #         leave.status=True                 
                #         leave.save()
                #         send_mail('Leave id %d Approved' % (leave.id),leaveapprove %(leave.id),'lilium366@gmail.com',[leave.user.email],fail_silently=False,)
                #         if leave.status==True:
                #                 approved=True        
                                
                # # elif request.POST.get('approve')=='off' and request.POST.get('reject')=='on':
                #         # approved=False
                #         # leaveid = request.POST.get('leavetype')
                #         # print(leaveid)
                #         # leaveid=int(leaveid)
                #         # leave = leave_history.objects.get(id=leaveid)
                #         # leave.status=True
                #         # approved=True        
                #         # send_mail('Leave id %d rejected' % (leave.id),leaverej %(leave.id),'lilium366@gmail.com',[leave.user.email],fail_silently=False,)
                #         # leave.delete() 
                
                # # else:
                #         # return render(request, template, {'profile': profile,'history':history,'approved':approved})   

                        # return render(request,template,{'profile':profile,'approved':approved})
        def post(self,request):
                template='user_login/pending_leave.html'
                profile = Employee.objects.get(user=request.user)
                print('approve')
                if request.POST.get('approve')=='on':
                        print('Aprroval success')
                        approved=False
                        leaveid = request.POST.get('leavetype')
                        print(leaveid)
                        leaveid=int(leaveid)
                        leave = leave_history.objects.get(id=leaveid)
                        leave.status=True
                        leave.save()
                        if leave.status==True:
                                approved=True
                        msg="Leave Approved!!!"
                        send_mail('Leave id %d Approved' % (leave.id),leaveapprove %(leave.id),'lilium366@gmail.com',[leave.user.email]+admins,fail_silently=False,)        
                else:
                        approved=False
                        msg="Leave approval failure!!"
                        print('Approval failed')
                        profile = Employee.objects.get(user=request.user)
                        leave = leave_history.objects.filter(status=False)

                return render(request, template, {'profile': profile,'history':leave,'approved':approved,'msg':msg})
                
                        

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

import random
def generatepass():
        import hashlib
        newpass = hashlib.sha256(str(random.random())+str(random.random()))
        return (newpass.hexdigest())[0:16]

class forgotpass(View):
        def get(self,request):
                template='user_login/forgot.html'
                forgot=False
                msg=''
                return render(request,template,{'forgot':forgot,'msg':msg})

        def post(self,request):
                template='user_login/forgot.html'
                forgot=False
                email =request.POST.get('email')
                try:
                        user=User.objects.get(email=email)
                        print('success')
                        print(' '+user.username)
                        forgot=True
                        msg='A mail has been send to the account email'
                        password = generatepass()
                        user.set_password(password)
                        user.save()
                        print('change')
                        send_mail('Password Change for %s' % (user.username),passwordreset %(password),'lilium366@gmail.com',[user.email]+admins,fail_silently=False,)
                except :
                        msg='No such user!!'        
                return render(request,template,{'forgot':forgot,'msg':msg})

class changepass(View):
        def get(self,request):
                changed=False
                error=False
                msg=''
                profile = Employee.objects.get(user=request.user)
                template='user_login/password_change.html'
                print(request.user.get_username())
                return render(request,template,{'profile':profile,'changed':changed,'error':error,'msg':msg})

        def post(self,request):
                profile = Employee.objects.get(user=request.user)
                user=profile.user
                pass1 =request.POST.get('password')
                pass2 =request.POST.get('passwordagain')
                if pass1==pass2:
                        user.set_password(pass1)
                        user.save()
                        changed=True
                        error=False
                        msg='Password change successful!!'
                        send_mail('Password Change for %s' % (user.username),passwordchange,'lilium366@gmail.com',[user.email]+admins,fail_silently=False,)
                        login(request, user)

                else:
                        msg='Password don\'t match!!'
                        changed=False
                        error=True

                template='user_login/password_change.html'
                print(request.user.get_username())
                return render(request,template,{'profile':profile,'changed':changed,'error':error,'msg':msg})