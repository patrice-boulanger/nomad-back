from django.urls import path, re_path, include
from django.conf import settings

from drf_yasg import openapi
from drf_yasg.views import get_schema_view, SwaggerUIRenderer

from .views import (MeView, MeFeaturesListView, MeAvailabilityListView, MeAvailabilityDetailView,
                    EntrepreneurSignUpView,
                    AllFeaturesListView, )

schema_view = get_schema_view(
    info=openapi.Info(
        title="Nomad Backend API",
        description="RESTful API for Nomad Social backend",
        default_version="v1.0",
    ),
    public=True,
)

urlpatterns = [
    # users management
    path('entrepreneurs/register/', EntrepreneurSignUpView.as_view(), name="entrepreneurs-create"),

    # user's information management views
    path('me/', MeView.as_view(), name="me"),
    path('me/features/', MeFeaturesListView.as_view(), name="me-features"),
    path('me/availabilities/', MeAvailabilityListView.as_view(), name="me-availability-list"),
    path('me/availabilities/<int:pk>/', MeAvailabilityDetailView.as_view(), name="me-availability-detail"),

    # list of all features
    path('features/all/', AllFeaturesListView.as_view(), name="features-all"),
]

# Documentation swagger, available only if debug mode is enabled
if settings.DEBUG:
    urlpatterns += [
        re_path('swagger(?P<format>.json)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path('swagger(?P<format>.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    ]