from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^accounts/logout/', views.user_logout, name='account_logout'),
    url(r'^accounts/nickname/change/', views.nickname_change, name='account_change_nickname'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^auth-register/(?P<macro_id>[0-9a-z-]+)/$', views.AuthRegister.as_view(), name='auth_register'),
    url(r'^auth-modify/(?P<macro_id>[0-9a-z-]+)/(?P<email>.*)/$', views.AuthModify.as_view(), name='auth_modify'),
    url(r'^board/', include('board.urls', namespace='board'), ),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^log/', include('log.urls', namespace='log'), ),
    url(r'^modify/(?P<macro_id>[0-9a-z-]+)/$', views.MacroModify.as_view(), name='macro_modify'),
    url(r'^macro-manage/$', views.MacroManage.as_view(), name='macro_manage'),
    url(r'^mypage/$', views.MyPage.as_view(), name='mypage'),
    url(r'^register/', views.MacroRegister.as_view(), name='macro_register'),
    url(r'^user-manage/(?P<macro_id>[0-9a-z-]+)/$', views.UserManage.as_view(), name='user_manage'),
    url(r'^$', views.intro, name='intro'),
]
