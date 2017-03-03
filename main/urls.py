from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/', views.MacroRegister.as_view(), name='macro_register'),
    url(r'^modify/(?P<macro_id>[0-9a-z-]+)/$', views.MacroModify.as_view(), name='macro_modify'),
    url(r'^manager/(?P<macro_id>[0-9a-z-]+)/$', views.MacroManage.as_view(), name='macro_manager'),
    url(r'^auth-register/(?P<macro_id>[0-9a-z-]+)/$', views.AuthRegister.as_view(), name='auth_register'),
    url(r'^$', views.MyPage.as_view(), name='mypage'),
]
