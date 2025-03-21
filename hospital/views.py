from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.urls import re_path as login
from django.urls import re_path as authenticate
from django.http import HttpResponseServerError
from django.contrib.auth import logout 
from .models import *

from django.utils import timezone
from .models import Appointment





# Create your views here.

def About(request):
    return render(request,'about.html')



def Contact(request):
    return render(request,'contact.html')



def login(request):
    if not request.user.is_staff:
        return redirect('login')
    return render(request,'index.html')

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.shortcuts import render


def Login(request):
    error = ""  # To store error messages
    if request.method == 'POST':
        user = request.POST['username']
        pwd = request.POST['password']
        
        # Authenticate the user with provided credentials
        user = authenticate(request, username=user, password=pwd)
        
        # Check if the user exists and is authenticated
        if user is not None:
            if user.is_staff:  # Check if the user has staff privileges
                login(request, user)  # Log the user in
                error = "no"  # No error, login successful
            else:
                error = "yes"  # User is not staff
        else:
            error = "yes"  # Invalid credentials
    
    # Return the response with the error message
    d = {'error': error}
    return render(request, 'login.html', d)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def logout_Admin(request):
    # if not request.user.is_staff:
    #     return redirect('login')\
    request.session.clear()
    logout(request)
    return redirect('login')
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Appointment, Doctor, Patient

def Index(request):
    if not request.user.is_staff:
        return redirect('login')

    today = timezone.localdate()  # Get today's date in the correct timezone

    # Filter appointments for today (use date1 directly, since it's a date field)
    today_appointment_count = Appointment.objects.filter(date1=today).count()

    doctor_count = Doctor.objects.count()  # Efficient way to get doctor count
    patient_count = Patient.objects.count()
    appointment_count = Appointment.objects.count()

    # Pass the context data to the template
    context = {
        'doctor_count': doctor_count,
        'patient_count': patient_count,
        'appointment_count': appointment_count,
        'today_appointment_count': today_appointment_count
    }

    return render(request, 'index.html', context)



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def View_Doctor(request):
    if not request.user.is_staff:
        return redirect('login')
    doc = Doctor.objects.all()
    d = {'doc':doc}
    return render(request,'view_doctor.html',d)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def Add_Doctor(request):
    error = ""  # To store error messages
    if not request.user.is_staff:
        return redirect('login')
         
         
    if request.method == 'POST':
        n = request.POST['name']
        c = request.POST['contact']
        sp = request.POST['specialization']
        
        
        # Check if the user exists and is authenticated
        try:
            Doctor.objects.create(name=n, mobile=c, special=sp)
            error = "no"  # No error, login successful
        except:
            error = "yes"
    
    # Return the response with the error message
    d = {'error': error}
    return render(request, 'add_doctor.html', d)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def Delete_Doctor(request,pid):
    if not request.user.is_staff:
         return redirect('login')
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    return redirect('view_doctor')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Edit_Doctor(request, pid):
    pass
    if not request.user.is_staff:
        return redirect('login')
    
    try:
        doctor = Doctor.objects.get(id=pid)
    except Doctor.DoesNotExist:
        return redirect('view_doctor')  # Redirect if doctor not found

    error = ""  # To store error messages
    
    if request.method == 'POST':
        # Retrieve updated data from the form
        name = request.POST['name']
        contact = request.POST['contact']
        specialization = request.POST['specialization']

        try:
            # Update doctor details
            doctor.name = name
            doctor.mobile = contact
            doctor.special = specialization
            doctor.save()
            error = "no"  # No error, update successful
        except:
            error = "yes"  # Something went wrong, error occurred

    # Return the response with the error message and current doctor details
    d = {'doctor': doctor, 'error': error}
    return render(request, 'edit_doctor.html', d)


            



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def View_Patient(request):
    if not request.user.is_staff:
        return redirect('login')
    pat = Patient.objects.all()
    d = {'pat':pat}
    return render(request,'view_patient.html',d)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def Add_Patient(request):
    error = ""  # To store error messages
    if not request.user.is_staff:
         return redirect('login')
    if request.method == 'POST':
        n = request.POST['name']
        m = request.POST['mobile']
        g = request.POST['gender']
        a = request.POST['address']
        
        
        # Check if the user exists and is authenticated
        try:
            Patient.objects.create(name=n, mobile=m, gender=g, address=a)
            error = "no"  # No error, login successful
        except:
            error = "yes"
    
    # Return the response with the error message
    d = {'error': error}
    return render(request, 'add_patient.html', d)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def Delete_Patient(request,pid):
    if not request.user.is_staff:
         return redirect('login')
    patient = Patient.objects.get(id=pid)
    patient.delete()
    return redirect('view_patient')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from django.shortcuts import get_object_or_404


def Edit_Patient(request, pid):
    
    error = ""  # To store error messages
    if not request.user.is_staff:
        return redirect('login')
    
    patient = get_object_or_404(Patient, id=pid)   # Get the patient by ID or return 404 if not found
    
    if request.method == 'POST':
        # Get the updated details from the POST request
        n = request.POST['name']
        m = request.POST['mobile']
        g = request.POST['gender']
        a = request.POST['address']
        
        try:
            # Update the patient details
            patient.name = n
            patient.mobile = m
            patient.gender = g
            patient.address = a
            patient.save()  # Save the updated patient
            error = "no"  # No error, update successful
        except:
            error = "yes"  # Error occurred
    
    # Return the response with the error message and patient data
    d = {'error': error, 'patient': patient}
    return render(request, 'edit_patient.html', d)




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
















def View_Appointment(request):
    if not request.user.is_staff:
        return redirect('login')
    appoint = Appointment.objects.all()
    d = {'appoint':appoint}
    return render(request,'view_appointment.html',d)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def Add_Appointment(request):
    error = ""  # To store error messages
    if not request.user.is_staff:
         return redirect('login')
    doctor1=Doctor.objects.all()
    patient1=Patient.objects.all()
    if request.method == 'POST':
        d = request.POST['doctor']
        p = request.POST['patient']
        d1 = request.POST['date']
        t = request.POST['time']
        doctor=Doctor.objects.filter(name=d).first()
        patient=Patient.objects.filter(name=p).first()
        
        
        
        # Check if the user exists and is authenticated
        try:
            Appointment.objects.create(doctor=doctor, patient=patient,date1=d1, time1=t)
            error = "no"  # No error, login successful
        except:
            error = "yes"
    
    # Return the response with the error message
    d = {'doctor': doctor1,'patient': patient1,'error': error}
    return render(request, 'add_appointment.html', d)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def Delete_Appointment(request,pid):
    if not request.user.is_staff:
         return redirect('login')
    appointment = Appointment.objects.get(id=pid)
    appointment.delete()
    return redirect('view_appointment')


def Edit_Appointment(request, pid):
    error = ""  # To store error messages
    if not request.user.is_staff:
        return redirect('login')
    
    appointment = get_object_or_404(Appointment, id=pid)  # Get the appointment by ID
    doctor1 = Doctor.objects.all()
    patient1 = Patient.objects.all()

    if request.method == 'POST':
        d = request.POST['doctor']
        p = request.POST['patient']
        d1 = request.POST['date']
        t = request.POST['time']
        
        doctor = Doctor.objects.filter(name=d).first()
        patient = Patient.objects.filter(name=p).first()

        try:
            # Update the appointment
            appointment.doctor = doctor
            appointment.patient = patient
            appointment.date1 = d1
            appointment.time1 = t
            appointment.save()  # Save the updated appointment
            error = "no"  # No error, update successful
        except:
            error = "yes"  # Error occurred
    
    context = {'appointment': appointment, 'doctor': doctor1, 'patient': patient1, 'error': error}
    return render(request, 'edit_appointment.html', context)
# _________________________________________

from django.shortcuts import render, redirect
from .models import Appointment

from django.shortcuts import render, redirect
from django.utils.timezone import localdate
from .models import Appointment

def Today_Appointments(request):
    if not request.user.is_staff:
        return redirect('login')

    today = localdate()  # Get the local current date
    appointments = Appointment.objects.filter(date1=today).order_by('time1')  # Fetch today's appointments

    return render(request, 'today_appointments.html', {'appoint': appointments, 'today': today})























