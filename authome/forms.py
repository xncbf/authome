from django import forms
from django.utils import timezone
from authome.settings import ACCOUNT_USERNAME_BLACKLIST


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
        nickname_modified = self.user.extendsuser.nickname_modified
        # 닉네임 변경한지 1일이 지나지 않았을때 에러 발생
        if (timezone.now() - nickname_modified).seconds < 3600 * 24 * 1 and self.user.extendsuser.nickname is not None:
            self.add_error(
                'nickname', "닉네임을 최근 24시간 이내에 변경했습니다."
            )
        if nickname in ACCOUNT_USERNAME_BLACKLIST:
            self.add_error(
                'nickname', "해당 닉네임은 사용이 불가능합니다."
            )
        return cleaned_data

    def save(self):
        nickname = self.cleaned_data.get('nickname')
        user = self.user.extendsuser
        user.nickname = nickname
        user.save()
