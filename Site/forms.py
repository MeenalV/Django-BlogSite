from django import forms


# table for blogs : 1. blog id , writer id, writer username , title of blog, content of blog , topic related to , date of writing 					, date of uploading , date of deleting , date of content updating , active/inactive				   							 
#  2. interaction id , blog id , interaction type , writer/reader id, date of interaction

class Blog(forms.Form) :
	title =  forms.CharField(max_length = 320 , widget =  forms.TextInput(
			attrs = (
				{
				'class' : 'form-control' ,
				'placeholder' : 'Enter the Title for your Blog'
				})
			))

	Blog = 	forms.CharField(max_length = 4000 , widget =  forms.TextInput(
			attrs = (
				{
				'class' : 'form-control' ,
				'placeholder' : 'Let''s start writing!!!'
				})
			))

	Comment = forms.CharField(max_length = 4000 , required = False , widget =  forms.TextInput(
			attrs = (
				{
				'class' : 'form-control' ,
				'placeholder' : 'Enter your Comment Here!'
				})
			))


class Login(forms.Form) :
	username = forms.CharField(max_length = 128 , widget =  forms.TextInput(
			attrs = (
				{
				'class' : 'form-control' ,
				'placeholder' : 'UserName Please'
				})
			))

	userID = forms.EmailField(max_length = 128 , widget =  forms.TextInput(
			attrs = (
				{
				'class' : 'form-control' ,
				'placeholder' : 'Email ID'
				})
			))

	password = forms.CharField(max_length=32, widget=forms.PasswordInput(
			attrs = (
				{
				'class' : 'form-control' ,
				'placeholder' : 'Password'
				})
			))