from rest_framework import serializers
from main.models import MacroFeeLog, UserPage


class UserPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPage
        fields = ('macro', 'end_date', 'end_yn')
