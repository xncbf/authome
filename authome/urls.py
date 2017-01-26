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
from main import views
from django.conf.urls.static import static
from django.conf import settings

handler404 = 'main.views.page_not_found_view'
handler500 = 'main.views.error_view'
handler403 = 'main.views.permission_denied_view'
handler400 = 'main.views.bad_request_view'


urlpatterns = [
    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    url(r'^xncbf/', include(admin.site.urls)),
    url(r'^accounts/login/', views.user_login, name='login'),
    url(r'^accounts/logout/', views.user_logout, name='logout'),
    url(r'^accounts/join/', views.user_join, name='join'),
    url(r'^docs/tutorial/', views.tutorial, name='tutorial'),
    url(r'^docs/introduction/', views.introduction, name='introduction'),
    url(r'^mypage/', include('main.urls', namespace='mypage'), ),
    url(r'^yeonsu/', views.yeonsu, name='yeonsu'),
    url(r'^$', views.intro, name='intro'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
