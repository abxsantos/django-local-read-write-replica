from django.contrib import admin
from django.urls import include
from django.urls import path
from rest_framework import routers

from django_local_read_write_replica.apps.my_app.drf.views import MessageViewSet, DjangoTestingView

message_router = routers.DefaultRouter(trailing_slash=False)
message_router.register("message", MessageViewSet, basename="message")



urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(message_router.urls)),
    path(
        "django-testing-view/schedule_task_testing_view/",
        DjangoTestingView.as_view({"post": "schedule_task_testing_view"}),
        name="Scheduled task Django testing view",
    ),
]
