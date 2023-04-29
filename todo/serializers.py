from rest_framework import serializers

from core.exceptions import (
    ExistStatusWithThisOrderException, StatusDoesNotExistException
)
from todo.models import Todo, Status, Notify
from user.serializers import UserSerializer


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'
        read_only_fields = ('id', 'user')

    def validate(self, data):
        if self.instance is None:
            user = self.context['request'].user
            if Status.objects.filter(
                    user=user, order=data['order']
            ).exists():
                raise ExistStatusWithThisOrderException
        elif 'order' in data:  # Updating existing object
            user = self.instance.user
            order = data.get('order', self.instance.order)
            if Status.objects.filter(
                    user=user, order=order
            ).exists():
                raise ExistStatusWithThisOrderException
        return data

    def create(self, validated_data):
        status = Status.objects.create(
            **validated_data, user=self.context['request'].user
        )
        return status


class TodoSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ('id', 'user')

    def validate_status(self, value):
        try:
            status = Status.objects.get(
                id=value, user=self.context['request'].user
            )
        except Status.DoesNotExist:
            raise StatusDoesNotExistException
        return status

    def create(self, validated_data):
        todo = Todo.objects.create(
            **validated_data, user=self.context['request'].user
        )
        return todo


class TodoGetSerializer(TodoSerializer):
    status = StatusSerializer(read_only=True)
    user = UserSerializer(read_only=True)


class NotifySerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Notify
        fields = '__all__'
        read_only_fields = ('id', 'user', 'task')

    def validate_status(self, value):
        try:
            status = Status.objects.get(
                id=value, user=self.context['request'].user
            )
        except Status.DoesNotExist:
            raise StatusDoesNotExistException
        return status

    def create(self, validated_data):
        notify = Notify.objects.create(
            **validated_data, user=self.context['request'].user
        )
        return notify


class NotifyGetSerializer(NotifySerializer):
    status = StatusSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    task = serializers.CharField(read_only=True, source='task__title')
