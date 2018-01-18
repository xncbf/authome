from django.conf.urls import url, include
from . import views


handler404 = 'main.views.page_not_found_view'
handler500 = 'main.views.error_view'
handler403 = 'main.views.permission_denied_view'
handler400 = 'main.views.bad_request_view'

urlpatterns = [
    # 17년 5월부터 사용금지인데 기존에 쓰고있는 사람때문에 지울수가없다 ㅠ
    url(r'^auth/(?P<username>.*)/(?P<password>.*)/(?P<macro_id>[0-9a-z-]+)/$', views.GetAuth.as_view()),
    url(r'^auth/(?P<token>.*)/(?P<macro_id>[0-9a-z-]+)/$', views.GetAuth2.as_view(), name='auth'),
]
