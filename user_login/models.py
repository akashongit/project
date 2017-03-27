from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Employee(models.Model):
    user = models.OneToOneField(User)
    dept=( 
        
        ('cs','Computer Science'),
        ('EC','Electronics and Communication'),
        ('EEE','Electrical and Electronic'),
        ('Mech','Mechanical'),
        ('BE','Biomedial'),
        ('AS','Applied Science'),
        ('NT','Non-Teching')
        )
    department = models.CharField(max_length=4,choices=dept,default='NT')
    Tflag = models.BooleanField(default=False)

    def _str_(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username   

class department(models.Model):
    depart=models.CharField(max_length=4,primary_key=True)
    hod = models.OneToOneField(User)

    def _str_(self):
        return self.depart

    def __unicode__(self):
        return self.depart

class leave_history(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    startdate = models.DateField()
    enddate = models.DateField()
    choices=(
        ('cl','casual leave'),
        ('hp','half paid')
        )
    leavetype = models.CharField(max_length=20,choices=choices)
    status = models.BooleanField(default=False)
    recom = models.BooleanField(default=False)
    des = models.CharField(max_length=300)
    half_day = models.IntegerField()

    def _str_(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username       

class leave_statistics(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    casual = models.IntegerField(default=0)
    vacation = models.IntegerField(default=0)
    conpens = models.IntegerField(default=0)
    earned = models.IntegerField(default=0)
    half_paid = models.IntegerField(default=0)

    def _str_(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username 



