from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from rest_framework import serializers
from users.models import User


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'roles',
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'roles',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        self.validate_password(password)
        instance = super().create(validated_data)
        instance.set_password(password)
        instance.save()
        return instance
