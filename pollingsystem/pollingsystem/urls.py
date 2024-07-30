
from django.contrib import admin
from django.urls import path, include
from pollingsystem.settings.base import DEBUG, MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="PollingSystem API",
        default_version='v1',
        description="API description"
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/poll/', include("poll.urls")),
    path('api/auth/', include("user.urls")),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),


]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
