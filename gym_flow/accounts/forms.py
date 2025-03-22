from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from gym_flow.accounts.models import Profile

UserModel = get_user_model()


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = '__all__'

# class ProfileEditForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         exclude = ('user', )
#
#     date_of_birth = forms.DateField(
#         widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'})
#     )
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Override the widget for profile_picture
#         self.fields['profile_picture'].widget = forms.FileInput(attrs={'class': 'file-input'})
