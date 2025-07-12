from rest_framework.authtoken.views import obtain_auth_token
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter

from main.views import *

router=DefaultRouter()

router.register('actors',ActorModelViewSet)
router.register('movies',MovieModelViewSet)
router.register('reviews',ReviewModelViewSet)
router.register('comments',CommentModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('get-token/',obtain_auth_token),
]
urlpatterns +=[
    path('register/',RegisterAPIView.as_view()),
]


