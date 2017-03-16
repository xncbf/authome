from django.conf.urls import url, include
from . import views


handler404 = 'main.views.page_not_found_view'
handler500 = 'main.views.error_view'
handler403 = 'main.views.permission_denied_view'
handler400 = 'main.views.bad_request_view'

urlpatterns = [
    url(r'^auth/(?P<username>.*)/(?P<password>.*)/(?P<macro_id>[0-9a-z-]+)/$', views.GetAuth.as_view()),
]
