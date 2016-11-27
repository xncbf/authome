from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/', views.macro_register, name='macro_register'),
    url(r'^manager/(?P<macro_id>[0-9a-z-]+)/$', views.MacroManage.as_view(), name='macro_manager'),
    url(r'^auth-register/(?P<macro_id>[0-9a-z-]+)/$', views.auth_register, name='auth_register'),
    url(r'^$', views.Index.as_view(), name='index'),
]
