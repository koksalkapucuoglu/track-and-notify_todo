from django.urls import path, include
from rest_framework import routers
from .views import TodoViewSet, StatusViewSet

router = routers.DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todos')
router.register(r'statuses', StatusViewSet, basename='statuses')
