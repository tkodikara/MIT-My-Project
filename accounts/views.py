from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView


class UserLoginView(LoginView):
    """Override LoginView to specify template name."""
    template_name = "accounts/login.html"


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'
