from django.urls import path

from .views import detail

app_name = 'products'
urlpatterns = [
    path('', detail, name='home'),
]