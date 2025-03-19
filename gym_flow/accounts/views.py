from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from gym_flow.accounts.forms import AppUserCreationForm
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
        # Use the user's pk for the profile-edit URL
        return reverse_lazy('home', kwargs={'pk': self.object.pk})


# class ProfileDetailView(DetailView):
#     model = Profile
#     template_name = 'accounts/profile-details-page.html'
#     context_object_name = 'profile'
#
#     def get_object(self):
#         """Ensure the profile is for the logged-in user."""
#         return get_object_or_404(Profile, user=self.request.user)
#
#     def get_context_data(self, **kwargs):
#         """Add user and workout stats to the context."""
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#
#         # Get workout stats
#         workouts = WorkoutSession.objects.filter(user=user).order_by('-date')[:5]
#
#         total_workouts = workouts.count()
#         total_exercises = sum(workout.exercises.count() for workout in workouts)
#
#         # Pass additional context
#         context['user'] = user  # Ensure 'user' context is available in the template
#         context['workouts'] = workouts
#         context['total_workouts'] = total_workouts
#         context['total_exercises'] = total_exercises
#
#         return context


# class ProfileEditView(UpdateView, LoginRequiredMixin):
#     model = Profile
#     form_class = ProfileEditForm
#     template_name = 'accounts/profile-edit-page.html'
#
#     def get_success_url(self):
#         return reverse_lazy(
#             'profile-details',
#             kwargs={
#                 'pk': self.object.pk,
#             }
#         )
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         # Save the new profile picture
#         if self.request.FILES.get('profile_picture'):
#             self.object.profile_picture = self.request.FILES['profile_picture']
#             self.object.save()
#         return response