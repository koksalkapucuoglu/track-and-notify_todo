from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


from todo.models import Todo, Status, Notify
from todo.serializers import (
    TodoSerializer, TodoGetSerializer, StatusSerializer, NotifySerializer,
    NotifyGetSerializer
)


class StatusViewSet(viewsets.ModelViewSet):
    serializer_class = StatusSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Status.objects.filter(
            user=self.request.user
        ).select_related(
            'user'
        )


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['id', 'title', 'status__order']
    ordering = ['-id']

    def get_serializer_class(self):
        if self.request.method in ['GET', 'RETRIEVE']:
            return TodoGetSerializer
        else:
            return TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(
            user=self.request.user
        ).select_related(
            'user', 'status'
        )


class NotifyViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'head', 'options', 'trace']
    serializer_class = NotifySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['id', 'status__order']
    ordering = ['-id']

    def get_serializer_class(self):
        if self.request.method in ['GET', 'RETRIEVE']:
            return NotifyGetSerializer
        else:
            return NotifySerializer

    def get_queryset(self):
        return Notify.objects.filter(
            user=self.request.user
        ).select_related(
            'user', 'status'
        )
