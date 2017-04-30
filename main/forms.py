from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django import forms
from authome.settings import ACCOUNT_USERNAME_BLACKLIST


class LoginForm(forms.Form):
    username = forms.CharField(
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
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Username 또는 Password 가 일치하지 않습니다")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class ChangeNicknameForm(forms.Form):
    nickname_length = 10
    nickname = forms.CharField(
        max_length=nickname_length,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': '변경할 닉네임', 'required': 'True',
        })
    )

    def clean(self):
        cleaned_data = super(ChangeNicknameForm, self).clean()
        nickname = cleaned_data.get('nickname')

        if nickname in ACCOUNT_USERNAME_BLACKLIST:
            self.add_error(
                'nickname', "해당 닉네임은 사용이 불가능합니다."
            )
        return cleaned_data

    def save(self):
        pass
        # get_adapter().set_password(self.user, self.cleaned_data["password1"])
