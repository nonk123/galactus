from django.urls import path

from .views import galactus

urlpatterns = [
    path('<query>/', galactus),
]
