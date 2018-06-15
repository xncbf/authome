from django.conf.urls import url
from . import views


handler404 = 'dev.views.page_not_found_view'
handler500 = 'dev.views.error_view'
handler403 = 'dev.views.permission_denied_view'
handler400 = 'dev.views.bad_request_view'

urlpatterns = [
    url(r'^(?i)quickstart/', views.quick_start, name='quick_start'),
    url(r'^(?i)use/autohotkey/', views.use_auth, name='use_ahk'),
    url(r'^$', views.introduction, name='introduction'),
]
