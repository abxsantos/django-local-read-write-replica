import logging

from django.db import transaction
from django_q.models import Schedule
from django_q.tasks import schedule
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response


logger = logging.getLogger(__name__)


def print_name():
    print("hello world")


class DjangoTestingView(viewsets.ViewSet):
    @action(detail=False, methods=["POST"])
    def schedule_task_testing_view(self, request: Request) -> Response:
        with transaction.atomic():
            schedule(
                name=f"expire-order",
                func=f"{print_name.__module__}.{print_name.__name__}",
                schedule_type=Schedule.ONCE,
            )
            return Response(
                status=status.HTTP_201_CREATED,
            )
