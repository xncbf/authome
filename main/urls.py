from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/', views.MacroRegister.as_view(), name='macro_register'),
    url(r'^modify/(?P<macro_id>[0-9a-z-]+)/$', views.MacroModify.as_view(), name='macro_modify'),
    url(r'^user-manage/(?P<macro_id>[0-9a-z-]+)/$', views.UserManage.as_view(), name='user_manage'),
    url(r'^auth-register/(?P<macro_id>[0-9a-z-]+)/$', views.AuthRegister.as_view(), name='auth_register'),
    url(r'^auth-modify/(?P<macro_id>[0-9a-z-]+)/(?P<email>.*)/$', views.AuthModify.as_view(), name='auth_modify'),
    url(r'^macro-manage/$', views.MacroManage.as_view(), name='macro_manage'),
    url(r'^mypage/$', views.MyPage.as_view(), name='mypage'),
]
