from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^macro$', views.macro_register, name='macro_register'),
    url(r'^$', views.dev_index, name='dev_index'),
]
