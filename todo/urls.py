from rest_framework import routers

from todo.views import TodoViewSet, StatusViewSet, NotifyViewSet

router = routers.DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todos')
router.register(r'statuses', StatusViewSet, basename='statuses')
router.register(r'notifies', NotifyViewSet, basename='notifies')
