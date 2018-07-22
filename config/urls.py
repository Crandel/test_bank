from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),  # User management
    url(r'^api/users/', include(("users.urls", "users"), namespace="users")),
    url(r'^api/accounts/', include(("accounts.urls", "accounts"), namespace="accounts")),
    url(r'^api/transactions/', include(("transactions.urls", "transactions"), namespace="transactions")),

]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request),
        url(r'^403/$', default_views.permission_denied),
        url(r'^404/$', default_views.page_not_found),
        url(r'^500/$', default_views.server_error),
    ]
