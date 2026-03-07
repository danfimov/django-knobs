from django.contrib import admin
from django.urls import path
from showcase import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index),
    path("api/knobs/", views.knobs_api),
]
