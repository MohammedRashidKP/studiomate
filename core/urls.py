from django.conf.urls import url
from django.views.generic import TemplateView
from . import views as core_views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^show_dashboard/$', core_views.show_dashboard, name='show_dashboard')
]
