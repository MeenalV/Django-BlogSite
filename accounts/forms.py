from django import forms
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from .models import User


class RegisterForm(forms.Form):
    """
    create user
    """
    email = forms.EmailField(max_length=254, required=True, widget=forms.TextInput(attrs={'class': 'cus-box'}))
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(), required=True)
    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput(), required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        existing_user = User.objects.filter(email=email)
        if existing_user.count() > 0:
            raise forms.ValidationError(_("User already exists with this email. Please try with different email."))
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if not password2:
            raise forms.ValidationError(_("You must confirm your password."))
        if password != password2:
            raise forms.ValidationError(_("Your passwords do not match."))
        return password2

    def save(self):
        data = self.cleaned_data
        user = User(
            email=data['email'],
            first_name= data['first_name'],
            last_name = data['last_name'],
            is_active=False,
            password=make_password(data['password'])
        )
        user.save()
        return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password2')


class PasswordRestForm(forms.Form):
    """
    reset password form
    """
    email = forms.EmailField(max_length=254, required=True)


class RegisterBloggerForm(forms.Form):
    """
    create user
    """
    email = forms.EmailField(max_length=254, required=True, widget=forms.TextInput(attrs={'class': 'cus-box'}))
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(), required=True)
    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput(), required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        existing_user = User.objects.filter(email=email)
        if existing_user.count() > 0:
            raise forms.ValidationError(_("User already exists with this email. Please try with different email."))
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if not password2:
            raise forms.ValidationError(_("You must confirm your password."))
        if password != password2:
            raise forms.ValidationError(_("Your passwords do not match."))
        return password2

    def save(self):
        data = self.cleaned_data
        user = User(
            email=data['email'],
            first_name= data['first_name'],
            last_name = data['last_name'],
            is_active=False,
            password=make_password(data['password']),
            is_writer=True
        )
        user.save()
        return user

