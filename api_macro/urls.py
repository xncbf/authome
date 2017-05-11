from django.conf.urls import url, include
from . import views


handler404 = 'main.views.page_not_found_view'
handler500 = 'main.views.error_view'
handler403 = 'main.views.permission_denied_view'
handler400 = 'main.views.bad_request_view'

urlpatterns = [
    # TODO: 5월20일부터는 토큰으로만 로그인하도록 변경
    url(r'^auth/(?P<username>.*)/(?P<token>.*)/(?P<macro_id>[0-9a-z-]+)/$', views.GetAuth.as_view()),
]
