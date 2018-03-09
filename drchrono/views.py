# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from drchrono.backends import *
from django.contrib import messages
from django.core.urlresolvers import reverse
from drchrono.models import *
import bcrypt


def index(request):
    return render(request, 'drchrono/index.html', {'title': "Welcome", 'hide_nav': True})


@login_required
def success(request):
    return render(request, 'drchrono/success.html', {'title': "Fetching Data"})


@login_required
def load_appointments(request):
    appointments = get_appointments_of_today(request)
    res = []
    user_info = get_doctor_info(request)

    # Do a cascade delete on the whole DB
    Configure.objects.filter(id=user_info['id']).delete()
    configure = Configure(user=request.user, dr_name=user_info['first_name'], id=user_info['id'])
    configure.save()
    request.session['user'] = configure
    for appointment in appointments:
        patient_id = appointment.get('patient')
        # No matter patient exists in database or not, we update it every time a doctor logs in
        patient = None

        if patient_id:
            patient_info = get_patient(request, _id=patient_id)
            ssn = patient_info["social_security_number"]
            patient = Patient(id=patient_id, first_name=patient_info['first_name'], last_name=patient_info['last_name'],
                              salt_ssn=bcrypt.hashpw(ssn[-4:].encode('utf-8'), bcrypt.gensalt(14)) if ssn else '',
                              photo=patient_info["patient_photo"] or
                              'https://semantic-ui.com/images/avatar2/large/molly.png', user=configure)
            patient.save()

        entry = {"patient_name": patient.first_name + ' ' + patient.last_name if patient else '',
                 "scheduled_time": appointment['scheduled_time'], "photo": patient.photo if patient else '',
                 "reason": appointment['reason']}

        # If the doctor log out and log in again when a patient is waiting, we need to retrieve the patient's info
        if appointment.get('status') in ('Checked In', 'In Session'):
            print('there')
            # entry['status'] = appointment.get('status')
            CheckIns.objects.create(pk=appointment['id'], appointment_id=appointment['id'], user=configure,
                                    check_in_time=appointment.get('check_in_time'), status=appointment['status'])

        # If this is an unseen appointment, we will save it to appointment model
        else:
            print('here')
            Appointment(id=appointment['id'], reason=appointment['reason'], patient=patient, user=configure,
                        scheduled_time=appointment['scheduled_time']+"-06:00").save()
        res.append(entry)

    # return HttpResponse(res, content_type='application/json')
    return HttpResponse(200)


@login_required
def dash_board(request):
    user = Configure.objects.get(user=request.user)
    checked_in_ids = set()
    in_session_res = []
    # TODO: Change to namedtuple
    for i in CheckIns.get_in_sessions(user):
        checked_in_ids.add(i.appointment_id)
        r = {'appointment': Appointment.objects.get(pk=i.appointment_id)}
        r['patient'] = r['appointment'].patient
        in_session_res.append(r)

    waiting_res = []
    for i in CheckIns.get_waitings(user):
        checked_in_ids.add(i.appointment_id)
        r = {'appointment': Appointment.objects.get(pk=i.appointment_id)}
        r['patient'] = r['appointment'].patient
        waiting_res.append(r)

    unseens = []
    print(Appointment.objects.count())
    for i in Appointment.objects.all():
        if not CheckIns.objects.filter(pk=i.id).count():
            unseens.append({'appointment': i, 'patient': i.patient})
    print('in', in_session_res)
    print('wait', waiting_res)
    print('unseen', unseens)
    return render(request, 'drchrono/dashboard.html', context={'title': "Dash Board", 'in_sessions': in_session_res,
                                                               'waitings': waiting_res, 'unseens': unseens})

@login_required
def meet(request, appointment_id):
    check_in = CheckIns.objects.get(appointment_id=appointment_id)
    check_in.meet_time = timezone.now()
    check_in.status = 'arrived'
    check_in.save()
    messages.info(request, 'Success')
    update_appointment(request, appointment_id, {'status': 'arrived', 'meet_time': check_in.meet_time})
    return redirect(reverse("dashboard"))


@login_required
def complete(request, appointment_id):
    check_in = CheckIns.objects.get(appointment_id=appointment_id)
    check_in.status = 'completed'
    check_in.save()
    messages.info(request, 'Success')
    update_appointment(request, appointment_id, {'status': 'completed'})
    Appointment.objects.get(pk=appointment_id).delete()
    return redirect(reverse("dashboard"))

