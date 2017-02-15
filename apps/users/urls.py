from django.conf.urls import url

from rest_framework.authtoken import views

from users.api import SignUpView


urlpatterns = [
    url(r'^login$', views.obtain_auth_token, name='login'),
    url(r'^signup$', SignUpView.as_view(), name='signup'),
]
