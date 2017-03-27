from django.conf.urls import url
from . import views,registration,leave_application

urlpatterns = [
    url(r'^$',views.home,name='home'),
    url(r'^login/',views.user_login.as_view(),name='login'),
    url(r'^register/',registration.register,name='register'),
    url(r'^hello/',views.userpage,name='userpage'),
    url(r'^logout/',views.user_logout,name='userlogout'),
    url(r'^apply_leave/',leave_application.leave_apply.as_view(),name='leave_apply'),
    url(r'^cancel_leave/',views.leave_cancel.as_view(),name='leave_cancel'),
    url(r'^leave_history/',views.leavehistory.as_view(),name='leave_history'),
    url(r'^check_status/',views.check_status.as_view(),name='check_status'),
    url(r'^statistics/',views.statistics.as_view(),name='statistics'),
    url(r'^profile/',views.profile.as_view(),name='profile'),
    url(r'^pending_leave/',views.pendingleave.as_view(),name='pending_leave'),
    url(r'^emp_profile/',views.empprofile.as_view(),name='emp_profile')
]
