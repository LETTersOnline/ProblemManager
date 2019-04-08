from problem.models import *
from rest_framework import serializers


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'

    url = serializers.CharField(source='get_absolute_url', read_only=True)
