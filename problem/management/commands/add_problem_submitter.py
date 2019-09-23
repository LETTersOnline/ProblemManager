import time

from django.core.management.base import BaseCommand, CommandError
from problem.models import Problem
from problem.utils import CrawlerController


class Command(BaseCommand):

    def handle(self, *args, **options):
        controller = CrawlerController.get_controller()

        for contest_id in range(100, 1220):
            try:
                number_of_submitters = controller.get_contest('codeforces', contest_id)
                for i in range(len(number_of_submitters)):
                    pid = f'{contest_id}{chr( ord("A") + i )}'
                    problem = Problem.objects.filter(pid=pid, oj='codeforces').first()
                    if problem:
                        problem.accepted_number = int(number_of_submitters[i][1:])
                        problem.save()
            except Exception as e:
                print(e)