"""authome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from mypage import views
from django.conf.urls.static import static
from django.conf import settings

handler404 = 'mypage.views.page_not_found_view'
handler500 = 'mypage.views.error_view'
handler403 = 'mypage.views.permission_denied_view'
handler400 = 'mypage.views.bad_request_view'


urlpatterns = [
    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    url(r'^accounts/login/', views.user_login, name='login'),
    url(r'^accounts/logout/', views.user_logout, name='logout'),
    url(r'^accounts/join/', views.user_join, name='join'),
    url(r'^tutorial/', views.tutorial, name='tutorial'),
    url(r'^introduction/', views.introduction, name='introduction'),
    url(r'^mypage/', include('mypage.urls', namespace='mypage'), ),
    url(r'^$', views.intro, name='intro'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
