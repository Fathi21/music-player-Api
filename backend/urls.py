from django.contrib import admin
from django.urls import path, include

from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static 
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)


from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view


schema_view = swagger_get_schema_view(
    openapi.Info(
        title="MusicPlayer API",
        default_version='1.0.0',
        description="API documentation of App",
    ),
    public=True,
)


urlpatterns = [
    path('', include('musicPlayerApi.urls')),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', 
        include([
            path('post/', include(('musicPlayerApi.urls', 'MusicPlayer'), namespace='MusicPlayer')),
            path('swagger/schema/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
        ])
    ),
    
] 

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)