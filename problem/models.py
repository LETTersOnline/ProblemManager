from django.urls import reverse
from django.db import models
from django_mysql.models import JSONField, Model


class Member(Model):
    name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('members-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Team(Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(Member, related_name='teams')

    def get_absolute_url(self):
        return reverse('teams-detail', args=[str(self.id)])

    def __str__(self):
        return '{}(id={})'.format(self.name, self.id)


class Problem(Model):
    oj = models.CharField(max_length=255)
    pid = models.CharField(max_length=255)
    accepted_number = models.IntegerField(default=-1)
    submitted_number = models.IntegerField(default=-1)
    difficult_number = models.IntegerField(default=-1)
    ac_rate_in_percent = models.IntegerField(default=-1)   # x%, 默认只存储x
    origin_link = models.URLField(default='http://codeforces.com')
    content = JSONField(default=dict)

    def __str__(self):
        return '{}-{}'.format(self.oj, self.pid)

    def get_absolute_url(self):
        return reverse('problems-detail', args=[str(self.id)])

    class Meta:
        unique_together = ('oj', 'pid')


class Record(Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('records-detail', args=[str(self.id)])


class Contest(Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    problems = models.ManyToManyField(Problem, related_name='contests')

    def get_absolute_url(self):
        return reverse('contests-detail', args=[str(self.id)])
