from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from .forms import RegisterForm, PasswordRestForm, RegisterBloggerForm
from accounts.models import User
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.translation import ugettext_lazy as _
from common.notification import Common
common = Common()
# Create your views here.


class BlogLoginView(LoginView):
    """
    checking user is login  and redirecting to user dash board
    """

    def dispatch(self, request, *args, **kwargs):
        """
        checking user is login  and redirecting to user dash board
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if self.request.user.id:
            return redirect('test')
        return super(BlogLoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Security check complete. Log the user in. remember me function """
        auth_login(self.request, form.get_user())
        if self.request.POST.get('remember_me', None) and self.request.user.id:
            self.request.session.set_expiry(86400)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        """"""
        context = super().get_context_data(**kwargs)

        return context


def register(request):
    """
    register user
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            RegisterForm.save(form)
            messages.success(request, _('Profile has been created successfully.'))
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            print(raw_password)
            user = authenticate(email=email, password=raw_password)
            login(request, user ,backend='django.contrib.auth.backends.ModelBackend')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def test(request):
    return HttpResponse('u are login')


def logout_user(request):
    """
    Frontend user logout.
    :param request:models
    :return:
    :author: Bharti(bharti@zapbuild.com)
    """
    logout(request)
    return redirect('login')


def reset_password(request):
    """
    reset user password
    :param request:
    :return:
    """
    page_title = 'Reset Password'
    host = 'https' if request.is_secure() else 'http'
    if request.method == 'POST':
        form = PasswordRestForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get('email')
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    if user.is_active:
                        mail_list = []
                        mail_args = {
                            "mail_template_args": {
                                'name': user.first_name +' '+ user.last_name,
                                'email': user.email,
                                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                'user': user,
                                'token': default_token_generator.make_token(user),
                                'protocol': 'https' if request.is_secure() else 'http',
                                'domain': request.META['HTTP_HOST']
                            },
                            "mail_to": user.email, "mail_template": "reset_password_email.html",
                            "mail_subject": 'BudgetScooter password reset'
                        }
                        mail_list.append(mail_args)
                        if mail_list:
                            common.send_mass_mail(mail_list)
                            print()
                        return redirect(_('password_reset_done'))
                    else:
                        return redirect('reset_password')
            else:
                return redirect('reset_password')
        else:
            return HttpResponse('Invalid  form request found.')
    else:
        form = PasswordRestForm()
        return render(request, 'registration/password_reset_form.html', {'form': form, 'page_title': page_title, 'host': host})


@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get("old_password")
            new_password = form.cleaned_data.get("new_password1")
            if old_password == new_password:
                messages.error(request, "Your new password and current password can't be same.")
                return redirect('change_password')
            else:
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('change_password')
        else:
            messages.error(request, 'Please enter correct current password.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})


def register_blogger(request):
    """
    register Writer
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = RegisterBloggerForm(request.POST)
        if form.is_valid():
            RegisterBloggerForm.save(form)
            messages.success(request, _('Profile has been created successfully.'))
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
        else:
            render(request, 'register_blogger.html', {'form': form})
    else:
        form = RegisterBloggerForm()
    return render(request, 'register_blogger.html', {'form': form})