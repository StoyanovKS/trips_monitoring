from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from .forms import RegisterForm, LoginForm, ProfileEditForm

User = get_user_model()
class RegisterView(CreateView):
    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("login")


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm


class UserLogoutView(LogoutView):
    pass


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user
