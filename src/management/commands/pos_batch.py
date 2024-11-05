from __future__ import print_function

from django.core.management.base import BaseCommand
from src.management.pos_batch.services.main_services import MainService


class Command(BaseCommand):
    help = 'Run this command to migrate'

    def add_arguments(self, parser):
        parser.add_argument('subcommand',
                            choices=[
                                'healthcheck',
                                'healthcheck_table',
                                'compare_schema',
                                'compare_data',
                                'compare_api',
                            ])

    def handle(self, *args, **options):
        """
        Dispatches by given subcommand
        """
        if options['subcommand'] == 'healthcheck':
            with MainService(**options) as migrate_db:
                migrate_db.healthcheck()
        elif options['subcommand'] == 'healthcheck_table':
            with MainService(**options) as migrate_db:
                migrate_db.healthcheck_table()
        elif options['subcommand'] == 'compare_schema':
            with MainService(**options) as migrate_db:
                migrate_db.compare_schema()
        elif options['subcommand'] == 'compare_data':
            with MainService(**options) as migrate_db:
                migrate_db.compare_data()
        elif options['subcommand'] == 'compare_api':
            with MainService(**options) as migrate_db:
                migrate_db.compare_api()
        else:
            print(self.help)
