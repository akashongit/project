from django import forms
from django.contrib.auth.models import User
from .models import Employee,leave_history

class loginform(forms.Form):
    username=forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder':'password'}))


# for registration purpose
# reference http://www.tangowithdjango.com/book17/chapters/login.html

class UserForm(forms.ModelForm):
    password = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    username=forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Username'}))
    first_name=forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name=forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    email=forms.EmailField(label="",widget=forms.TextInput(attrs={'placeholder':'Email'}))
    class Meta:
        model = User
        fields = ('first_name','last_name','email','username', 'password')

class UserprofileForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('department','Tflag')

# for leave application
class leave_app_form(forms.ModelForm):
    startdate = forms.DateField(label="",widget=forms.DateInput(attrs={'placeholder':'Start Date'})) 
    enddate = forms.DateField(label="",widget=forms.DateInput(attrs={'placeholder':'End Date'})) 
    des = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Leave reason','height':'100','width':'100'}))
    # half_day = forms.IntegerField(label="",widget=forms.NumberInput(attrs={'placeholder':'No of Halfdays'}))
    # leavetype = forms.ChoiceField(label="leave Type",widget=forms.Select(attrs={}),('casual leave','half paid'))
    class Meta:
        model = leave_history
        fields = '__all__'
        exclude =('user','status','recom','half_day')

class leave_approve(forms.ModelForm):
    status = forms.BooleanField(label="",widget=forms.CheckboxInput(attrs={'name':'approve'}),required=False)
    class Meta:
        model = leave_history
        fields = ('status',)