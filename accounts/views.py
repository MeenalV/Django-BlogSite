from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login

from .forms import RegisterForm
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
            user = authenticate(email=email, password=raw_password)
            login(request, user)
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
