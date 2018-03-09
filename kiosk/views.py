from django.shortcuts import render, redirect
from django.http import HttpResponse
from kiosk.forms import CheckInForm, PatientInfoForm
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from drchrono.backends import *
from drchrono.models import *


@login_required
def index(request):
    form = CheckInForm()
    dr_name = Configure.get_name_for_user(request.user)
    return render(request, 'kiosk/check_in.html', {'form': form, 'hide_nav': True, 'doctor_name': dr_name})


@login_required
def select_appointments(request):
    if request.method == 'POST':
        check_in_form = CheckInForm(request.POST)
        # Can't accept digits in name
        if check_in_form.is_valid() and \
                not any(i.isdigit() for i in check_in_form.cleaned_data['first_name']) and \
                not any(i.isdigit() for i in check_in_form.cleaned_data['last_name']):

            # Get a list of today's patients of this patient
            match_patients = Patient.match_patients(last_name=check_in_form.cleaned_data['last_name'],
                                                    first_name=check_in_form.cleaned_data['first_name'],
                                                    ssn_tail=check_in_form.cleaned_data['ssn_tail'],
                                                    user=Configure.objects.get(user=request.user))
            if not match_patients:
                messages.error(request, 'No appointment found')
                return redirect(reverse('kiosk:index'))
            else:
                print(match_patients[0].appointment_set.all())
                return render(request, 'kiosk/appointments.html', {"match_patients": match_patients})
        else:
            messages.error(request, 'Invalid form')
    return redirect(reverse("kiosk:index"))


@login_required
def verify(request, appointment_id):
    patient = Appointment.objects.get(pk=appointment_id).patient
    patient_info = get_patient(request, patient.id)
    print(patient_info)
    form = PatientInfoForm(patient_info)
    messages.info(request, 'success!')
    return render(request, 'kiosk/verify.html', {'form': form, 'appointment_id': appointment_id})


@login_required
def check_in(request, appointment_id):
    if CheckIns.objects.filter(appointment_id=appointment_id,
                               user=Configure.objects.get(user=request.user)).count() > 0:
        messages.error(request, 'Already checked in!')
    else:
        CheckIns.objects.create(appointment_id=appointment_id, status="checked_in",
                                user=Configure.objects.get(user=request.user))
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.checked = True
        appointment.save()

        messages.info(request, 'The doctor has known your arrival!')
    return redirect(reverse('kiosk:index'))






