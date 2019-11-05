from django.db import models
from django_mysql.models import JSONField, Model


class ProblemSimilarity(Model):

    first = models.ForeignKey('problem.Problem', on_delete=models.CASCADE, related_name='similar_problem_prev')
    second = models.ForeignKey('problem.Problem', on_delete=models.CASCADE, related_name='similar_problem_succ')
    description = JSONField(default=dict)

    '''
    {
        "title_equality': 1
    }
    '''
