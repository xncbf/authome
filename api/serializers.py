from rest_framework import serializers
from dev.models import UserPage


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPage
        fields = ('macro', 'end_date', 'end_yn', 'active_yn')
