from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^submit/?$', views.select_appointments, name='submit'),
    url(r'^verify/(\d+)/?$', views.verify, name='verify'),
    url(r'^checkin/(\d+)/?$', views.check_in, name='checkin')
]
