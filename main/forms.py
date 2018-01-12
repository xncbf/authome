from django.contrib.auth import authenticate
from django import forms
from django.utils import timezone
from authome.settings import ACCOUNT_USERNAME_BLACKLIST
from .models import ExtendsUser


class LoginForm(forms.Form):
    email = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'ID', 'required': 'True',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Password', 'required': 'True',
        })
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("email 또는 Password 가 일치하지 않습니다")
        return self.cleaned_data

    def login(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        return user


class ChangeNicknameForm(forms.Form):
    nickname_length = 10
    nickname = forms.CharField(
        max_length=nickname_length,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': '변경할 닉네임', 'required': 'True',
        })
    )

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ChangeNicknameForm, self).clean()
        nickname = cleaned_data.get('nickname')
        nickname_modified = ExtendsUser.objects.filter(user=self.user)[0].nickname_modified
        # 닉네임 변경한지 30일이 지나지 않았을때 에러 발생
        if (timezone.now() - nickname_modified).seconds < 3600 * 24 * 30:
            self.add_error(
                'nickname', "닉네임을 최근에 변경했습니다."
            )
        if nickname in ACCOUNT_USERNAME_BLACKLIST:
            self.add_error(
                'nickname', "해당 닉네임은 사용이 불가능합니다."
            )
        return cleaned_data

    def save(self):
        nickname = self.cleaned_data.get('nickname')
        ExtendsUser.objects.filter(user=self.user).update(nickname=nickname)

