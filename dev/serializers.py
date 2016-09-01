from django.forms import widgets
from rest_framework import serializers
from .models import MacroFeeLog, MacroLog, Macro, UserPage
from datetime import datetime, timedelta


class UserPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPage
        fields = ('user', 'macro', 'end_date')

    def create(self, validated_data):
        """
        검증한 데이터로 새 `Snippet` 인스턴스를 생성하여 리턴합니다.
        """
        return MacroFeeLog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        검증한 데이터로 기존 `Snippet` 인스턴스를 업데이트한 후 리턴합니다.
        """
        instance.owner = validated_data.get('user', instance.user)
        instance.macro = validated_data.get('macro', instance.macro)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.save()
        return instance
