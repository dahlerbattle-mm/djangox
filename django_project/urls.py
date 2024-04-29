from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("user-accounts/", include("accounts.urls")),  
    path("", include("pages.urls")),
    path("dashboards/", include("dashboards.urls")),
    path("integrations/", include("integrations.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
