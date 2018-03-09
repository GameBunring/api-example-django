from django.conf.urls import include, url
from django.views.generic import TemplateView
import kiosk.views
import drchrono.views

urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='check_in.html'), name='home'),
    url(r'^$', drchrono.views.index, name='home'),
    url(r'^accounts/profile', drchrono.views.success, name='success'),
    url(r'^load_appointments/?', drchrono.views.load_appointments, name='load_appointments'),
    url(r'^dashboard/?$', drchrono.views.dash_board, name='dashboard'),
    url(r'^meet/(\d+)$', drchrono.views.meet, name='meet'),
    url(r'^complete/(\d+)$', drchrono.views.complete, name='complete'),
    url(r'^kiosk/', include('kiosk.urls', namespace='kiosk')),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]
