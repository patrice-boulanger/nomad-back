from django.urls import path, re_path, include
from django.conf import settings

from drf_yasg import openapi
from drf_yasg.views import get_schema_view, SwaggerUIRenderer

from .views import (EntrepeneurListView, EntrepreneurCreateView,
                    CompanyUserListView, )

schema_view = get_schema_view(
    info=openapi.Info(
        title="Nomad Backend API",
        description="RESTful API for Nomad Social backend",
        default_version="v1.0",
    ),
    public=True,
)

urlpatterns = [
    path('auth/', include(('knox.urls', 'auth'), namespace="auth")),
    path('entrepreneurs/', EntrepeneurListView.as_view(), name="entrepreneurs-list"),
    path('entrepreneurs/register/', EntrepreneurCreateView.as_view(), name="entrepreneurs-create"),
    path('company/users/', CompanyUserListView.as_view(), name="company-users-list"),
]

# Documentation swagger, available only if debug mode is enabled
if settings.DEBUG:
    urlpatterns += [
        re_path('swagger(?P<format>.json)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path('swagger(?P<format>.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    ]