from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from gym_flow.accounts.forms import AppUserCreationForm, ProfileEditForm
from gym_flow.accounts.models import Profile

UserModel = get_user_model()


class AppUserLoginView(LoginView):
    template_name = 'accounts/login.html'


class AppUserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)

        return response

    def get_success_url(self):
        return reverse_lazy('home', )


class ProfileEditView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit.html'

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user

    def get_success_url(self):
        return reverse_lazy(
            'profile-details', kwargs={'pk': self.object.pk, }
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        # Save the new profile picture
        if self.request.FILES.get('profile_picture'):
            self.object.profile_picture = self.request.FILES['profile_picture']
            self.object.save()
        return response


class ProfileDetailView(DetailView):
    model = UserModel
    template_name = 'accounts/profile-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        return context
