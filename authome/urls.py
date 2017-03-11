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
from django.contrib.sitemaps.views import sitemap
from main import views
from django.conf.urls.static import static
from django.conf import settings
import os

handler404 = 'main.views.page_not_found_view'
handler500 = 'main.views.error_view'
handler403 = 'main.views.permission_denied_view'
handler400 = 'main.views.bad_request_view'


urlpatterns = [
    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    url(r'^' + os.environ['AUTHOME_ADMIN_URL'] + '/', include(admin.site.urls)),

    url(r'^accounts/logout/', views.user_logout, name='account_logout'),
    url(r'^accounts/', include('allauth.urls')),

    # url(r'^accounts/join/', views.user_join, name='join'),
    url(r'^macro/', include('main.urls', namespace='main'), ),
    url(r'^board/', include('board.urls', namespace='board'), ),
    url(r'^log/', include('log.urls', namespace='log'), ),
    url(r'^$', views.intro, name='intro'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
