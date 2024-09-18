from django.urls import path
from .views import CoverageAPIView

urlpatterns = [
    path("coverage/", CoverageAPIView.as_view(), name="coverage"),
]
