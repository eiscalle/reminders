from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView

from users.forms import UserRegistrationForm, UserUpdateForm, UserPasswordChangeForm, UserAuthenticationForm

User = get_user_model()


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('index')
    template_name = 'base_form.html'


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/detail.html'
    context_object_name = 'object'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'base_form.html'

    def get_queryset(self):
        return super().get_queryset().filter(pk=self.request.user.pk)

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.request.user.pk})


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'base_form.html'

    def get_success_url(self):
        return reverse('user_detail', args=[self.request.user.pk])


class UserLoginView(LoginView):
    form_class = UserAuthenticationForm
    template_name = 'base_form.html'
