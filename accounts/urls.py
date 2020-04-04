from django.urls import path

from accounts import views as account_views

urlpatterns = [
    path('register/',  account_views.register, name='register'),
    path('accounts/profile/',  account_views.test, name='test'),
    path('accounts/logout/', account_views.logout_user, name='user_logout'),

]