from django.urls import re_path
from . import views

app_name = "verifications"
urlpatterns = [
    re_path(r'^image_codes/(?P<image_code_id>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/$', views.ImageCodeView.as_view()),
    re_path(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),
]
