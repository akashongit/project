from user_login.forms import UserForm,UserprofileForm
from django.shortcuts import render
from .models import Employee,leave_statistics
from django.contrib.auth.models import User

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form= UserprofileForm(data=request.POST)
        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            add_leave(emp=user)

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors,profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserprofileForm()

    # Render the template depending on the context.
    return render(request,
            'user_login/register.html',
            {'user_form': user_form,'profile_form':profile_form, 'registered': registered} )

def add_leave(emp):
    
    if emp.is_staff!=True:
        leave = leave_statistics.objects.get_or_create(user=emp)[0]
        leave.casual = 100
        leave.vacation = 100
        leave.copens = 0
        leave.earned = 0
        leave.half_paid = 0
        leave.save()
        return leave
    else:
        return None        