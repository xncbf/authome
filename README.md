[![Build Status](https://travis-ci.org/xncbf/authome.svg?branch=django1.11)](https://travis-ci.org/xncbf/authome)

[![alt text](https://authome.s3.amazonaws.com/images/logo/facebook_cover.png)](https://autho.me) 
# 매크로 사용자 관리 사이트
프로젝트에 대한 전체 문서는 다음 링크에서 확인할 수 있습니다. https://docs.autho.me

## Requirements
* python==3.6.x
* django==1.11.8
* zappa>=0.45.1

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
AWS_ACCESS_KEY_ID = AWS 엑세스 키
AWS_SECRET_ACCESS_KEY = AWS 시크릿 엑세스 키
```

### 이메일 환경
회원가입 email confirm 및 비밀번호 찾기를 위해 mailchimp, mandrill 을 사용하였습니다.

### 스케줄
유저 인증의 end_yn 검증을 위해 스케줄링을 사용합니다.
스케줄링은 zappa schedule 을 통해 동작합니다.

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
