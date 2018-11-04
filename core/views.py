from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import ProjectDetails
import uuid
from django.db.models.functions import ExtractMonth
from django.db.models.functions import ExtractDay
from .forms import PhotoForm
from .models import Photo
from django.http import JsonResponse
from django.views import View
import os
from django.conf import settings


def auth_login(request):
        msg = []
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    msg.append("login successful")
                    return redirect('show_studio_dashboard')
                else:
                    msg.append("disabled account")
            else:
                msg.append("invalid login")
        return render(request, 'home.html', {'errors': msg})


@login_required
def show_studio_dashboard(request):

    project_details_list = []
    user = request.user
    fetch_all_project_details(project_details_list, user)
    return render(request, 'studiodashboard.html', {'project_details_list': project_details_list})


@login_required
def add_project(request):
    project_details_list = []
    project_title = request.POST.get('title')
    client_name = request.POST.get('name')
    email = request.POST.get('mail')
    mobile_number = request.POST.get('mobile')
    user = request.user
    unique_id = uuid.uuid4()
    if project_title is not None and client_name is not None:
            ProjectDetails.objects.create(unique_id=unique_id, user=user, project_name=project_title,
                            client_name=client_name, email=email, mobile=mobile_number)
    media_root = settings.MEDIA_ROOT
    make_folder(os.path.join(media_root, str(unique_id)))
    fetch_all_project_details(project_details_list, user)
    return render(request, 'studiodashboard.html', {'project_details_list': project_details_list})


def fetch_all_project_details(project_details_list, user):
    all_projects = ProjectDetails.objects.all().filter(user=user).\
        annotate(month=ExtractMonth('date'), day=ExtractDay('date'))
    for element in all_projects:
        project_title = element.project_name
        client_name = element.client_name
        email = element.email
        mobile_number = element.mobile
        unique_id = element.unique_id
        month = fetch_month_string(element.month)
        day = element.day
        current_element = {'project_title': project_title, 'client_name': client_name, 'email': email, 'mobile_number':
            mobile_number, 'unique_id': unique_id, 'day': day, 'month': month}
        project_details_list.append(current_element)


@login_required
def view_project_details(request, value):
    request.session[0] = value
    photos_list = Photo.objects.all().filter(client_id=value)
    return render(request, 'projectdetails.html', {'photos': photos_list})


@login_required
def auth_logout(request):
    return render(request, 'home.html')


def fetch_month_string(month_number):
    month_string = ''
    if month_number == 1:
        month_string = 'JAN'
    if month_number == 2:
        month_string = 'FEB'
    if month_number == 3:
        month_string = 'MAR'
    if month_number == 4:
        month_string = 'APR'
    if month_number == 5:
        month_string = 'MAY'
    if month_number == 6:
        month_string = 'JUN'
    if month_number == 7:
        month_string = 'JUL'
    if month_number == 8:
        month_string = 'AUG'
    if month_number == 9:
        month_string = 'SEPT'
    if month_number == 10:
        month_string = 'OCT'
    if month_number == 11:
        month_string = 'NOV'
    if month_number == 12:
        month_string = 'DEC'
    return month_string


class ProgressBarUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'photos/progress_bar_upload/index.html', {'photos': photos_list})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        client_id=''
        if form.is_valid():
            image = form.cleaned_data['file']
            filename = image.name
            client_id = request.session['0']
            photo = Photo.objects.create(title=filename, file=image, client_id=client_id)
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        photos_list = Photo.objects.all().filter(client_id=client_id)
        return render(request, 'projectdetails.html', {'photos': photos_list})


def clear_database(request):
    client_id = request.session['0']
    for photo in Photo.objects.all().filter(client_id=client_id):
        photo.file.delete()
        photo.delete()
    return redirect(request.POST.get('next'))


def make_folder(path):
    try:
        os.makedirs(path)
    except OSError:
        pass


def delete_project(request, value):
    for photo in Photo.objects.all().filter(client_id=value):
        photo.file.delete()
        photo.delete()
    ProjectDetails.objects.filter(unique_id=value).delete()
    media_root = settings.MEDIA_ROOT
    os.rmdir(os.path.join(media_root, value))
    project_details_list = []
    user = request.user
    fetch_all_project_details(project_details_list, user)
    return render(request, 'studiodashboard.html', {'project_details_list': project_details_list})


