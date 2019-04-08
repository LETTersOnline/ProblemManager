
from django.db import models
from django_mysql.models import JSONField, Model


class Member(Model):
    name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Team(Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(Member, related_name='teams')

    def __str__(self):
        return self.name


class Problem(Model):
    oj = models.CharField(max_length=255)
    pid = models.CharField(max_length=255)
    accepted_number = models.IntegerField(default=0)
    submitted_number = models.IntegerField(default=0)
    difficult_number = models.IntegerField(default=0)
    origin_link = models.URLField(default='http://codeforces.com')
    content = JSONField(default=dict)

    def __str__(self):
        return '{}-{}'.format(self.oj, self.pid)

    @property
    def get_absolute_url(self):
        return self.origin_link

    class Meta:
        unique_together = ('oj', 'pid')


class Record(Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
