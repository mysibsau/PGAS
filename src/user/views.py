from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .models import User


class UserEdit(UpdateView):
    model = User
    template_name = "user_edit.html"
    success_url = reverse_lazy("common:home")
    fields = ["first_name", "last_name", "group"]

    def get_object(self, queryset=None):
        return self.request.user


class LoginView(BaseLoginView):
    template_name = "login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.telegram_id:
            return reverse_lazy("common:home")
        return reverse_lazy("user:me")
