from django.urls import path
from django.conf.urls import url
from accounts import views as account_views


urlpatterns = [
    path(r'register/',  account_views.register, name='register'),
    path(r'register/blogger/',  account_views.register_blogger, name='register_blogger'),
    path(r'accounts/profile/',  account_views.test, name='test'),
    path('accounts/logout/', account_views.logout_user, name='user_logout'),
    path('accounts/reset-password/', account_views.reset_password, name='reset_password'),
    url(r'^accounts/change_password/$', account_views.change_password, name='change_password'),
]