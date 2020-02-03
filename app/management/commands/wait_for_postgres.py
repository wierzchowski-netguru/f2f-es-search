import os
from time import sleep, time

from django.core.management import BaseCommand

import psycopg2


class Command(BaseCommand):
    help = 'Helper command making sure database is ready'
    start_time = time()
    check_interval = 1
    database_url = os.getenv('DATABASE_URL')

    def add_arguments(self, parser):
        parser.add_argument('check_timeout', nargs='+', type=int)

    def handle(self, *args, **options):
        check_timeout = options['check_timeout'][0]

        while time() - self.start_time < check_timeout:
            try:
                conn = psycopg2.connect(self.database_url)
                self.stdout.write("Postgres is ready.")
                conn.close()
                return
            except psycopg2.OperationalError:
                self.stdout.write(f"Postgres is not ready. Waiting {self.check_interval} second...")
                sleep(self.check_interval)

        self.stderr.write(f"Could not connect to Postgres within {check_timeout} seconds.")
