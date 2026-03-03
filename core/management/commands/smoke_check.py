from django.core.management.base import BaseCommand, CommandError
from django.urls import reverse


class Command(BaseCommand):
    help = 'Run lightweight deployment smoke checks (framework + URL resolution).'

    def handle(self, *args, **options):
        required_routes = ['schema-json', 'token_obtain_pair', 'token_refresh']

        for route_name in required_routes:
            try:
                path = reverse(route_name)
            except Exception as exc:
                raise CommandError(f'Failed to resolve route {route_name}: {exc}') from exc
            self.stdout.write(self.style.SUCCESS(f'{route_name} -> {path}'))

        self.stdout.write(self.style.SUCCESS('Smoke checks passed.'))
