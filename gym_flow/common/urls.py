from django.urls import path

from gym_flow.common import views

urlpatterns = [
    path("", views.home_page, name="home"),
]
