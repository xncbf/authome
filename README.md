[![Build Status](https://travis-ci.org/xncbf/authome.svg?branch=master)](https://travis-ci.org/xncbf/authome)
# [AUTHOME](https://autho.me) 매크로 사용자 관리 사이트
프로젝트에 대한 전체 문서는 다음 링크에서 확인할 수 있습니다. https://docs.autho.me

## Requirements
* python>=3.4.x
* django==1.9.x

## 시스템 의존성
패키지 의존성을 설치하기 전에 앞서 설치가 필요합니다.
* libpq-dev
* python3-dev

## 패키지 의존성
* djangorestframework
* django-subdomains
* Unipath
* django-allauth
* django-admin-honeypot
* pytz
* invoke
* django-ipware
* psycopg2
* drfdocs
* django_mobile


## 개발 환경 세팅
### 의존성 패키지 설치 및 모델 migration
```
$ pip install -r requirements.txt
$ python manage.py migrate
```

### 사이트 변수 설정
api.autho.me 와 같은 subdomain 을 사용하려면 다음과 같은 설정이 필요합니다.
```
$ python manage.py shell
>>> from django.contrib.sites.models import Site
>>> site = Site.objects.all()[SITE_ID]
>>> site.domain = 'localhost:8000'
>>> site.save()
```

### 환경변수 세팅
#### 예시
```
AUTHOME_SECRET_KEY = 비밀키
AUTHOME_DATABASE_NAME = 디비명
AUTHOME_DATABASE_USER = 디비 아이디
AUTHOME_DATABASE_PASSWORD = 디비 패스워드
AUTHOME_DATABASE_HOST = 디비 호스트
AUTHOME_DATABASE_PORT = 디비 포트
AUTHOME_ADMIN_URL = 관리자페이지 url
```
