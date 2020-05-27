"""BlogSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
<<<<<<< Updated upstream
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny
from django.conf.urls import url
from accounts import api as account_api
from rest_framework_simplejwt import views as jwt_views


admin.site.site_header = "BlogSite"
admin.site.site_title = "BlogSite"
admin.site.index_title = "Welcome to BlogSite Admin Portal"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/', include_docs_urls(title=admin.site.site_header, permission_classes=(AllowAny,), )),
    path('', include('accounts.urls')),
    path('', include('blog.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path(r'api/v1/auth/login/token/', account_api.ObtainAccessTokenView.as_view(), name='token_obtain'),
    path(r'api/v1/auth/login/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('accounts/login/', BlogLoginView.as_view(), name='login'),
    # path('auth/', include('api.urls')),
    # path("api/auth/", include("api.urls")),
# =======
# from blog import views
# from accounts.views import BlogLoginView

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('accounts.urls')),
#     path('accounts/login/', BlogLoginView.as_view(), name='login'),
#     path('', include('blog.urls')),
#     path('accounts/', include('django.contrib.auth.urls')),
#     path('auth/', include('api.urls')),
#     path("api/auth/", include("api.urls")),
# >>>>>>> Stashed changes
]
