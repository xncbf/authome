from django.conf.urls import url, include
from . import views


handler404 = 'dev.views.page_not_found_view'
handler500 = 'dev.views.error_view'
handler403 = 'dev.views.permission_denied_view'
handler400 = 'dev.views.bad_request_view'

urlpatterns = [
    url(r'^', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.DRFDocsView.as_view(), name='drfdocs'),

    # 17년 5월부터 사용금지인데 기존에 쓰고있는 사람때문에 지울수가없다 ㅠ
    url(r'^macro/auth/(?P<username>.*)/(?P<password>.*)/(?P<macro_id>[0-9a-z-]+)/$', views.GetAuth.as_view()),
    url(r'^macro/auth/(?P<token>.*)/(?P<macro_id>[0-9a-z-]+)/$', views.GetAuth2.as_view(), name='auth'),
]
