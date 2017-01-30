![Image of Yaktocat](/main/static/images/authome.png)
# [AUTHOME](http://autho.me)
매크로 사용자 관리 사이트  
Full documentation for the project is available at http://docs.autho.me
#Requirements
* python>=3.4
* django==1.9.9

#Setting for development
In console
```
$ pip install -r requirements.txt
$ python manage.py migrate
```
In manage.py shell
```
>>> from django.contrib.sites.models import Site
>>> site = Site.objects.all()[SITE_ID]
>>> site.domain = 'localhost:8000'
>>> site.save()
```
