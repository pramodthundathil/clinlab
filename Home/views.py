from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserAddForm
from django.contrib.auth.models import User, Group
from .decorators import admin_only, unautenticated_user
from django.contrib.auth.decorators import login_required
from .models import Units, LabDetails, Patient
from Clinic.models import Order, TestResult, TestType
from datetime import timedelta,  datetime

today = datetime.now() + timedelta(1)
daybeforeyesterday = today - timedelta(2)

@login_required(login_url='SignIn')
def Index(request):
    pending_samples_count = Order.objects.filter(order_status = False, user = request.user).count()
    completed_samples = Order.objects.filter(approval_date__gte = daybeforeyesterday, approval_date__lte = today, user = request.user)
    
    context = {
        "pendinf_samples_count":pending_samples_count,
        "recent_complete_count":len(completed_samples),
        "completed_samples":completed_samples
    }
    return render(request,"index.html",context)


@login_required(login_url='SignIn')
def calender(request):
    return render(request,'calender.html')



@unautenticated_user
def SignIn(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pswd']
        user1 = authenticate(request, username = username , password = password)
        
        if user1 is not None:
            
            request.session['username'] = username
            request.session['password'] = password
            login(request, user1)
            return redirect('Index')
        
        else:
            messages.error(request,'Username or Password Incorrect')
            return redirect('SignIn')
    return render(request,"login.html")


def SignOut(request):
    logout(request)
    return redirect('SignIn')



@login_required(login_url="SignIn")
def AddUser(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname= request.POST['lname']
        email = request.POST["email"]
        uname = request.POST["uname"]
        pswd = request.POST["pswd"]
        pswd1 = request.POST["pswd1"]
        utype = request.POST['utype']

        if pswd != pswd1:
            messages.error(request,"Password Do not Matches..")
            return redirect("AddUser")
        if User.objects.filter(username = uname).exists():
            messages.error(request,"Username alredy exists user another username")
            return redirect("AddUser")
        if User.objects.filter(email = email).exists():
            messages.error(request,"Email alredy exists user another email")
            return redirect("AddUser")
        else:
            user = User.objects.create_user(first_name = fname,last_name = lname,email = email, username = uname, password =pswd)
            user.save()

            group = Group.objects.get(name=utype)
            user.groups.add(group)
            messages.success(request,"Staff added To Staff list....")
            return redirect("ListUser")
    return render(request,"user-add.html")


'''
Settings for units of tests and its functionalities this functions hadeled in settings tab on Dashboard
'''

@login_required(login_url='SignIn')
def Unit(request):
    myunits = Units.objects.all().order_by("unit")
    if request.method == "POST":
        unit = request.POST.get("unit")
        description = request.POST.get("description")

        try:
            units = Units.objects.create(unit = unit,description = description)
            units.save()
            messages.info(request,"Unit Addedd....")
            return redirect("Units")
        except:
            messages.info(request, "Something wrong.... ")
            return redirect("Units")
    context = {
        "myunits":myunits
    }

    return render(request,'settings/units.html',context)



@login_required(login_url='SignIn')
def profile(request):

    if LabDetails.objects.filter(user = request.user).exists():
        lab_profile =  LabDetails.objects.get(user = request.user)
    else:
        lab_profile = LabDetails.objects.create(user = request.user)
        lab_profile.save()

    if request.method == "POST":
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        country = request.POST.get('country')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal')
        phone = request.POST.get('phone')
        address = request.POST.get("address")

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        lab_profile.country = country
        lab_profile.state = state
        lab_profile.postel_code = postal_code
        lab_profile.contact_number = phone
        lab_profile.address = address

        user.save()
        lab_profile.save()
        messages.info(request,'Your Profile Updated...')
        return redirect("profile")

    context = {
        "lab_profile":lab_profile
    }
    return render(request,"settings/profiles.html",context)



@login_required(login_url='SignIn')
def ChangeProfilePic(request,pk):
    if request.method == "POST":
        lab = LabDetails.objects.get(id  = pk)
        lab.logo_of_lab.delete()
        lab.logo_of_lab = request.FILES['pro_pic']
        lab.save()
        messages.info(request,"Logo Changed..")
        return redirect("profile")
    else:
        return redirect("profile")
    

@login_required(login_url='SignIn')
def customers(request):
    patients = Patient.objects.filter(user = request.user).order_by('id')

    context = {
        "patients":patients
    }
    return render(request,'laboratory/cutomers.html',context)

@login_required(login_url='SignIn')
def customer_single(request,pk):
    patient = Patient.objects.get(id = pk)
    order = Order.objects.filter(patient = patient)

    context = {
        "patient":patient,
        "order":order
    }

    return render(request,"laboratory/patientsingle.html",context)

@login_required(login_url='SignIn')
def UploadLeatterHead(request):
    if request.method =="POST":
        letter_top = request.FILES.get("letter_top")
        letter_down = request.FILES.get("letter_down")
        lab = LabDetails.objects.get(user = request.user)
        lab.letter_head = letter_top
        lab.save()
        lab.letter_head_down = letter_down
        lab.save()
        messages.info(request,"letter head created")
        return redirect("profile")

    return redirect("profile")







