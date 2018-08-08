from django.urls import path
from login import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("front_callback/", views.FrontCallbackView.as_view(), name="front_callback"),
    path("back_callback/", views.BackCallbackView.as_view(), name="back_callback"),
]
