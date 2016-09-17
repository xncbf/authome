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
from dev import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/', views.user_login, name='login'),
    url(r'^accounts/logout/', views.user_logout, name='logout'),
    url(r'^accounts/join/', views.user_join, name='join'),
    url(r'^dev/', include('dev.urls', namespace='dev'),),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/(?P<macro_id>[0-9a-z-]+)/$', views.UserPageDetail.as_view()),
    url(r'^auth/', views.UserPageList.as_view()),
    url(r'^$', views.intro, name='intro'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
