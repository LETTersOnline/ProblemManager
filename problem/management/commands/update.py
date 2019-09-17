import time

from django.core.management.base import BaseCommand, CommandError

from problem.utils import update_problem, clear_problems


class Command(BaseCommand):

    def handle(self, *args, **options):
        clear_problems()
        for pid in range(1000, 7000):
            try:
                update_problem('hdu', str(pid))
            except Exception as e:
                print(f'hud {pid} update failed by error: {e}')
            time.sleep(0.5)
