# -*- coding: utf-8 -*-
"""
    drchrono.utils
    ~~~~~~~~~~~~

    Interface to handle DrChrono API.
"""

import requests
from social.apps.django_app.default.models import UserSocialAuth
from django.utils import timezone


def __get_auth_header(user):
    if not user:
        raise ValueError
    return {"Authorization": "Bearer {}".format(user.access_token)}


def __api_handler(request, url, method="GET", **kwargs):
    print(request)
    user = UserSocialAuth.objects.get(user=kwargs.get("user") or request.user)
    headers = kwargs.get('headers') or __get_auth_header(user)
    u_a = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
    headers["USER-AGENT"] = u_a
    kwargs['headers'] = headers

    response = requests.request(method, url, **kwargs)
    return response.json()


def api_get(request, url, **kwargs):
    return __api_handler(request, url, method="GET", **kwargs)


def api_post(request, url, data, **kwargs):
    return __api_handler(request, url, method="POST", data=data, **kwargs)


def api_patch(request, url, data, **kwargs):
    return __api_handler(request, url, method="PATCH", data=data, **kwargs)


BASE_URL = "https://drchrono.com/api"


def get_appointments_of_today(request):
    appointment_url = "{}/appointments".format(BASE_URL)
    params = {'date': timezone.now().date().isoformat()}
    appointment_list = []
    while appointment_url:
        data = api_get(request, appointment_url, params=params)
        if data['results'][0]['status'] not in ("Cancelled", "Not Confirmed"):
            appointment_list.extend(data['results'])
        appointment_url = data['next']
    print(len(appointment_list))
    return appointment_list


def get_doctor_info(request, **kwargs):
    doctor_url = "{}/doctors".format(BASE_URL)
    data = api_get(request, doctor_url, **kwargs)
    return data['results'][0]


# def search_appointments(request, last_name, first_name=None, ssn=None, **kwargs):
#     # search appointments of today for the patient checked_in
#
#     params = {'last_name': last_name}
#     if first_name:
#         params['first_name'] = first_name
#     patient_list = get_patients(request, params=params, **kwargs)
#     appointments = []
#     for p in patient_list:
#         if not p['social_security_number'] or not ssn or p['social_security_number'][-4:] == str(ssn):
#             return get_appointments_of_today(request, patient_id=p['id'])
#     return []


def search_patients(request, last_name, first_name=None, **kwargs):
    pass


def get_patient(request, _id, **kwargs):
    patient_url = "{}/patients/{}".format(BASE_URL, _id)
    return api_get(request, patient_url, **kwargs)


def update_appointment(request, appointment_id, data, **kwargs):
    url = "{}/appointments/{}".format(BASE_URL, appointment_id)
    return api_patch(request, url, data, **kwargs)


def update_patient(request, patient_id, data, **kwargs):
    url = "{}/patients/{}".format(BASE_URL, patient_id)
    return api_patch(request, url, data, **kwargs)