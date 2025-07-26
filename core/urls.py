from rest_framework.authtoken.views import obtain_auth_token
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import path,include
from rest_framework.routers import DefaultRouter

from main.views import *

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

...

schema_view = get_schema_view(
   openapi.Info(
      title="Budget Tracker API",
      default_version='v1',
      description="Test",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="doniyorbek.info@gmail.com"),
      license=openapi.License(name="Codial License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


router=DefaultRouter()

router.register('actors',ActorModelViewSet)
router.register('movies',MovieModelViewSet)
router.register('reviews',ReviewModelViewSet)
router.register('comments',CommentModelViewSet)

urlpatterns = [
    # Language switcher
    path('i18n/', include('django.conf.urls.i18n')),

    path('',include(router.urls)),
    path('get-token/',obtain_auth_token),
]
urlpatterns +=[
    path('register/',RegisterAPIView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('example/',example_view)
)



