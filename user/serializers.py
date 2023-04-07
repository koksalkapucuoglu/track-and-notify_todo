from django.contrib.auth import get_user_model
from django.db import IntegrityError

from rest_framework import serializers

from core.exceptions import (
    WrongOldPasswordException, ShortNewPasswordException,
    PasswordsDoNotMatchException, UserDoesNotExistWithEmailException
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password')

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        try:
            user = User.objects.create(
                **validated_data
            )
            user.set_password(validated_data['password'])
            user.save()
        except IntegrityError as e:
            raise serializers.ValidationError(e.__cause__)
        return user

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise PasswordsDoNotMatchException
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name
        )
        instance.last_name = validated_data.get(
            'last_name', instance.last_name
        )
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255, write_only=True)
    new_password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, data):
        user_id = self.context['request'].user.id
        old_password = data.get('old_password', None)
        new_password = data.get('new_password', None)
        user = User.objects.get(id=user_id)

        if not user.check_password(old_password):
            raise WrongOldPasswordException()

        if len(new_password) < 8:
            raise ShortNewPasswordException()

        user.set_password(new_password)
        user.save()

        return {"message": "Successfully changed"}


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise UserDoesNotExistWithEmailException()
        return value


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise PasswordsDoNotMatchException()
        return data
