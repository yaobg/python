from django.urls import path, include, re_path

from . import views

app_name = "users"
urlpatterns = [
    re_path(r"^register/$", views.RegisterView.as_view(), name="register"),
    re_path(r"^login/$", views.LoginView.as_view(), name="login"),
    re_path(r"^usernames/(?P<username>[a-zA-z0-9_-]{5,20})/count/$", views.UsernameCountView.as_view()),
    re_path(r"^phone/(?P<mobile>1[3-9]]\d{9})/count/$", views.MobileCountView.as_view()),
]
