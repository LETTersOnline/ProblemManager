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

        for pid in range(1000, 4055):
            try:
                update_problem('poj', str(pid))
            except Exception as e:
                print(f'poj {pid} update failed by error: {e}')
            time.sleep(1)

        for contest_id in range(100, 1220):
            for problem_id in range(15):
                pid = str(contest_id) + chr(ord('A') + problem_id)
                try:
                    update_problem('codeforces', pid)
                except Exception as e:
                    print(f'codeforces {pid} update failed by error: {e}')
                    break
                time.sleep(2)

