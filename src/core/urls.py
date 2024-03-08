from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .settings import DEBUG

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("common.urls")),
    path("users/", include("user.urls")),
    path("statements/", include("statement.urls")),
    path("achievements/", include("achievement.urls")),
    path("comments/", include("comment.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not DEBUG:
    handler404 = 'common.views.handler404'
    handler500 = 'common.views.handler500'
    handler403 = 'common.views.handler403'

if DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
