from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dev_index, name='index'),
]
