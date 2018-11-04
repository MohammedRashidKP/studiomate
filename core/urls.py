from django.conf.urls import url
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from . import views as core_views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^auth_login/$', core_views.auth_login, name='auth_login'),
    url(r'^auth_logout/$', core_views.auth_logout, name='auth_logout'),
    url(r'^show_studio_dashboard/$', core_views.show_studio_dashboard, name='show_studio_dashboard'),
    url(r'^add_project/$', core_views.add_project, name='add_project'),
    url(r'^project_view/(?P<value>\S+)/', core_views.view_project_details, name='project_view'),
    url(r'^progress-bar-upload/$', core_views.ProgressBarUploadView.as_view(), name='progress_bar_upload'),
    url(r'^clear/$', core_views.clear_database, name='clear_database'),
    url(r'^delete_project/(?P<value>\S+)/', core_views.delete_project, name='delete_project'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)