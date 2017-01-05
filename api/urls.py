from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^(?P<macro_id>[0-9a-z-]+)/$', views.UserPageDetail.as_view()),
    url(r'^$', views.UserPageList.as_view()),
]
