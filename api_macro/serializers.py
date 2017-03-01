from rest_framework import serializers
from main.models import MacroFeeLog, UserPage


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPage
        fields = ('macro', 'end_date', 'end_yn')
