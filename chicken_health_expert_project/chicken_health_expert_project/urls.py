from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chicken_expert_app.urls')),

    path("__reload__/", include("django_browser_reload.urls")),
]
