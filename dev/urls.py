
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/(?P<macro_id>\d+)/$', views.UserPageDetail.as_view()),
    url(r'^auth/', views.UserPageList.as_view()),
    url(r'^today/', views.today),
    url(r'^$', views.dev_index, name='index'),
]
