from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import UserLoginView, SignUpView

app_name = 'accounts'
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("sign-up/", SignUpView.as_view(), name="sign-up"),
]
