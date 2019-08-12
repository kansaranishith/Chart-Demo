from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SignUpForm
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import User, UserFiles
import csv
from django.http import JsonResponse
import os

def index(request):
	return render(request, 'chart/index.html')

def login_page(request):
	if request.method == 'POST':
		username = request.POST['username']
		pwd = request.POST['pwd']
		user = authenticate(request, username=username, password=pwd)
		if user is not None:
			request.session['user'] = user.id
			return HttpResponseRedirect(reverse('chart:home'))
		else:
			return render(request, 'chart/login.html',{"msg":"Authentication failed, please login again !"})
	else:
		return render(request, 'chart/login.html')	

def logout(request):
	request.session['user'] = None
	del request.session['user']
	return HttpResponseRedirect(reverse('chart:index'))

def home(request):
	if "user" in request.session:
		if request.session['user']:
			file_list = get_files(request.session['user'])
			return render(request, 'chart/home.html',{"file_list":file_list,"type":str(settings.DEFAULT_CHART_TYPE)})
		else:
			return HttpResponseRedirect(reverse('chart:login'))
	else:
		return HttpResponseRedirect(reverse('chart:login'))

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            return HttpResponseRedirect(reverse('chart:success'))
    else:
        form = SignUpForm()
    return render(request, 'chart/signup.html', {'form': form})

def success(request):
	return render(request, 'chart/index.html',{"msg":"You have sign up successfully, please log in now."})

def upload(request):
    if request.method == 'POST' and request.FILES['file_upload'] and request.session['user']:
        file_upload = request.FILES['file_upload']

        if not file_upload.name.endswith('.csv'):
        	file_list = get_files(request.session['user'])
        	return render(request, 'chart/home.html', {"msg":"Please upload a valid csv file", "file_list":file_list})

        fs = FileSystemStorage()

        import uuid
        f_name = uuid.uuid1()
        f_name = str(f_name) +str(".csv")

        filename = fs.save(f_name, file_upload)
        uploaded_file_url = fs.url(filename)

        file = UserFiles()
        file.user_id = User(pk=request.session['user'])
        file.file_path = uploaded_file_url
        file.file_name = f_name
        file.save()

    return HttpResponseRedirect(reverse('chart:home'))

def chart(request, file_id, type):
	if "user" in request.session:
		if request.session['user']:
			
			file = get_files(request.session['user'])
			file = file.filter(pk=file_id)

			if file:
				return render(request, 'chart/chart.html', {"file_id":file_id,"type":type})
			else:
				return HttpResponseRedirect(reverse('chart:home'))
	else:
		return HttpResponseRedirect(reverse('chart:home'))

def get_files(user_id):
	user = User(pk=user_id)
	file_list = user.userfiles_set.all()
	return file_list

def delete_file(request, file_id):
	if "user" in request.session:
		if request.session['user']:
			file = get_files(request.session['user'])
			file = file.filter(pk=file_id)
			if file:
				#remove file from media folder
				os.remove(str(settings.BASE_DIR)+ str(file[0].file_path))
				#remove file from database
				file.delete()
				return HttpResponseRedirect(reverse('chart:home'))
			else:
				return HttpResponseRedirect(reverse('chart:home'))
	else:
		return HttpResponseRedirect(reverse('chart:home'))

def chart_data(request, file_id):
	if "user" in request.session:
		if request.session['user']:
			file = get_files(request.session['user'])
			file = file.filter(pk=file_id)
			if file:
				file_path = str(settings.BASE_DIR)+ str(file[0].file_path)
				data={"X":[],"Y":[]}
				with open(file_path,'rb')as f:
					count = 0
					for l in f.readlines():
						if count:
							row = l.decode('utf8', 'ignore').strip()
							row_data= row.split(',')
							data["X"].append(row_data[0])
							data["Y"].append(row_data[1])
						count+=1
				return JsonResponse(data)
	else:
		data = {'msg': 'Not permitted'}
		return JsonResponse(data)