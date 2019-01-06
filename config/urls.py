from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from rest_framework.authtoken import views
from users.api import SignUpView


urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),  # User management
    path('api/transactions/', include(("transactions.urls", "transactions"), namespace="transactions")),
    path('api/accounts/', include(("accounts.urls", "accounts"), namespace="accounts")),
    path('api/login', views.obtain_auth_token, name='login'),
    path('api/signup', SignUpView.as_view(), name='signup'),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path('400', default_views.bad_request),
        path('403', default_views.permission_denied),
        path('404', default_views.page_not_found),
        path('500', default_views.server_error),
    ]
