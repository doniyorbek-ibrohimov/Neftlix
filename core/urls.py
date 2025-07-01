
from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('actors/',ActorsAPIView.as_view()),
    path('subs/',SubAPIView.as_view()),
    path('actors/<int:pk>/',ActorRetrieveAPIView.as_view()),
    path('subs/<int:pk>/',SubRetrieveAPIView.as_view()),
]
