from datetime import date

from django.core.management.base import BaseCommand, CommandError
from operations.maintenance_services import generate_due_work_orders


class Command(BaseCommand):
    help = 'Create work orders for due preventive maintenance plans (run once daily).'

    def add_arguments(self, parser):
        parser.add_argument('--date', help='Override today (YYYY-MM-DD) for tests/manual runs')

    def handle(self, *args, **options):
        try:
            as_of = date.fromisoformat(options['date']) if options['date'] else None
        except ValueError as exc:
            raise CommandError('Use --date YYYY-MM-DD') from exc
        count = generate_due_work_orders(as_of=as_of)
        self.stdout.write(self.style.SUCCESS(f'Created {count} work orders.'))
