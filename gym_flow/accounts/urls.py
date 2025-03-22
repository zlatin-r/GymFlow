from django.urls import path, include

from gym_flow.accounts import views

urlpatterns = [
    path('login/', views.AppUserLoginView.as_view(), name='login'),
    path('register/', views.AppUserRegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', include([
        path('', views.ProfileEditView.as_view(), name='profile-edit'),
    ]))
]