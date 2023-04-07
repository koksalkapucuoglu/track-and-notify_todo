from django.contrib import admin
from django.urls import include, path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from user.urls import router as user_router
from user import urls as user_url

schema_view = get_schema_view(
    openapi.Info(
        title="Track and Notify Todo API",
        default_version='v1',
        description="Track and Notify Todo API",
        contact=openapi.Contact(email="koksalkapucuoglu@gmail.com")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()

router.registry.extend(user_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/v1/', include(router.urls)),
    path(r'api/v1/users/', include(user_url)),
    path(r'api/v1/docs/', schema_view.with_ui(), name='schema-swagger-ui'),
    path(r'api/v1/docs/json/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
]
