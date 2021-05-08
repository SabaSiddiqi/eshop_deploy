# users/urls.py
from django.urls import include, path
from django.conf.urls import include, url
from users.views import dashboard, register
from django.contrib.auth import views

from .forms import UserLoginForm
from django.contrib.auth import views as auth_views

urlpatterns = [

    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^dashboard/", dashboard, name="dashboard"),
    url(r"^register/", register, name="register"),
    path(
        'login/',
        views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=UserLoginForm
            ),
        name='login'),
]
