from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("api/", include("coverage_app.urls")),
]
