"""django_capstone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import include  # url뿐 아니라 include를 import해야 합니다.
from django.contrib import admin
from django.urls import path
from main.views import *  # 1st app : main homepage
from dashboard.views import *  # 2nd app : dashboard
from upload.views import *  # 3rd app : upload
from django.conf.urls.static import static


SOCIAL_AUTH_URL_NAMESPACE = 'social'

LOGIN_REDIRECT_URL = '/'

urlpatterns = [
    # base
    path('admin/', admin.site.urls),

    # homepage
    path('', goHome),
    path('home/', index, name='home'),

    # google login
    path('social/', social_login, name='login_social'),

    # authentication with google
    path('oauth/', include('social_django.urls', namespace='social')),

    # logout
    path('logout/', logout, name='logout'),

    # dashboard
    path('mypage/dashboard/', include('dashboard.urls'), name='dashboard'),

    # history
    path('mypage/history/', history, name='history'),

    # upload
    path('mypage/upload/', include('upload.urls'), name='upload'),

    # loading
    path('mypage/loading/', loading, name='loading'),


]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
