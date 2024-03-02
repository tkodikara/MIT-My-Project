from django.contrib.auth.views import LoginView


class UserLoginView(LoginView):
    """Override LoginView to specify template name."""
    template_name = "accounts/login.html"
