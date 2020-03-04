from django.shortcuts import render
from Site.forms import *
# Create your views here.


def display_Blog(request) :
	form =  Blog(request.POST)
	if form.is_valid() :
		print()
		print(form.cleaned_data['title'])
		print(form.cleaned_data['Blog'])
		print(form.cleaned_data['Comment'])
		print()
	form = Blog()	
	return render(request , 'Site/forms.html' , {'form' : form})	


def login_Page(request) :
	login =  Login(request.POST)
	if login.is_valid() :
		print("Login details")
		print(login.cleaned_data['username'])
		print(login.cleaned_data['userID'])
		print(login.cleaned_data['password'])
		print()
	login = Login()	
	return render(request , 'Site/login.html' , {'login' : login})		