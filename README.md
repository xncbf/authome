이 프로젝트가 마음에 드신다면, star 버튼을 눌러주세요 :heart_eyes:  
If you like this project, please press the 'star' button :heart_eyes:
  
[![Build Status](https://travis-ci.org/xncbf/authome.svg?branch=master)](https://travis-ci.org/xncbf/authome)
# [AUTHOME](https://autho.me) 매크로 사용자 관리 사이트
프로젝트에 대한 전체 문서는 다음 링크에서 확인할 수 있습니다. https://docs.autho.me

## Requirements
* python==3.6.x
* django==1.11.8

## 시스템 의존성
패키지 의존성을 설치하기 전에 앞서 설치가 필요합니다.
* libpq-dev
* python3-dev

## 패키지 의존성
* django==1.11.8
* djangorestframework
* subdomains
* django-allauth==0.31.0
* django-admin-honeypot
* django-ipware
* django-ses
* boto
* Unipath
* psycopg2
* drfdocs
* celery
* django-celery-beat==1.0
* django-hitcount
* django-markdown-deux
* django-contrib-comments
* markdown2
* django-material



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
>>> site = Site.objects.all()[0]
>>> site.domain = 'example.com:8000'
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
AWS_SES_REGION_NAME = AWS 리전 네임
AWS_SES_REGION_ENDPOINT = AWS SES 리전 엔드포인트
AWS_ACCESS_KEY_ID = AWS 엑세스 키
AWS_SECRET_ACCESS_KEY = AWS 시크릿 엑세스 키
```

### 이메일 환경
회원가입 email confirm 및 비밀번호 찾기를 위해 django-ses 를 사용하였습니다.

### celery
ses 통계와 유저 인증의 end_yn 검증을 위해 django-celery-beat 를 사용합니다.  
broker는 product 환경에서 rabbitmq 를 사용합니다.

### 개발환경
#### URL
개발환경은 example.com:8000 에서 개발하기 적합하도록 설정되어있습니다.  
host 파일 수정후에 사용하시면 됩니다.

#### settings
개발용 settings 는 settings_local.py 에서 settings.py 를 오버라이딩 하도록 설정되어있습니다.
```
$ python3 manage.py runserver example.com:8000 --settings=authome.settings_local
```
또는 환경변수에
```
DJANGO_SETTINGS_MODULE = authome.settings_local
```
를 추가한 뒤에 사용해주시면 됩니다.
