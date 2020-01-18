import time

from django.core.management.base import BaseCommand, CommandError
from problem.models import Problem, Tag


class Command(BaseCommand):

    def handle(self, *args, **options):
        for problem in Problem.objects.all():
            tags = problem.content.get('tags', [])
            if tags:
                for tag in tags:
                    ins, _ = Tag.objects.get_or_create(name=tag)
                    ins.problems.add(problem)
            tags = []
            for tag in problem.tags.all():
                tags.append(tag.name)
            if tags:
                problem.problem_tags = ','.join(tags)
                problem.save()
