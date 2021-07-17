import logging
from time import time, sleep
import psycopg2
import os
from django.core import management
from django.conf import settings
from django.contrib.auth import get_user_model

check_timeout = os.getenv("POSTGRES_CHECK_TIMEOUT", 30)
check_interval = os.getenv("POSTGRES_CHECK_INTERVAL", 1)
interval_unit = "second" if check_interval == 1 else "seconds"
config = {
    "dbname": os.getenv("POSTGRES_DB", "app_db"),
    "user": os.getenv("POSTGRES_USER", "app_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "changeme"),
    "host": os.getenv("POSTGRES_HOST", "app_db"),
    "port": os.getenv("POSTGRES_PORT", "5432")
}

start_time = time()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
assert check_timeout > 0
assert check_interval < check_timeout


def pg_is_ready(host, user, password, dbname, port):
    while time() - start_time < check_timeout:
        try:
            conn = psycopg2.connect(**vars())
            logger.info("Postgres is ready")
            conn.close()
            return True
        except psycopg2.OperationalError:
            logger.info(f"Postgres isn't ready. Waiting for {check_interval} {interval_unit}...")
            sleep(check_interval)

    logger.error(f"We could not connect to Postgres within {check_timeout} seconds.")
    return False


class Command(management.base.BaseCommand):

    def handle(self, *args, **options):
        # Wait for postgresql
        if not settings.DEBUG:
            pg_is_ready(**config)

        # Apply migration if necessary
        self.stdout.write("Step migrate")
        management.call_command('migrate')

        # Create default user
        get_user_model().objects.create_superuser('django', 'change@me.com', 'selenium')
