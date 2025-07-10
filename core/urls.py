
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter

from main.views import *

router=DefaultRouter()

router.register('actors',ActorModelViewSet)
router.register('movies',MovieModelViewSet)
router.register('reviews',ReviewModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
]
