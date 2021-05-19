import logging

from django_q.models import Schedule

logger = logging.getLogger(__name__)


class DatabaseRouter:
    """
    A router to control all database operations on models in the
    auth application.
    """

    @staticmethod
    def is_djangoq_schedule(model):
        logger.debug(f"name of model is {model.__name__} and instance of {isinstance(model, Schedule)}")
        return isinstance(model, Schedule)

    def db_for_read(self, model, **hints):
        """
        Always read from REPLICA database
        """
        logger.debug("Using read replica")
        return "replica"

    def db_for_write(self, model, **hints):
        """
        Always write to DEFAULT database
        """
        logger.debug("Using write replica")
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Objects from REPLICA and DEFAULT are de same, then True always
        """
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Only DEFAULT database
        """
        return db == "default"
