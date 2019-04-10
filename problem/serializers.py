from problem.models import *
from django.db.models import Q
from rest_framework import serializers
import random
from ojcrawler.control import Controller
from rest_framework.decorators import action

controller = Controller()


class UpdateProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'
        read_only_fields = ('accepted_number', 'submitted_number', 'difficult_number',
                            'origin_link', 'content')

    oj = models.CharField()
    pid = models.CharField()

    def validate_oj(self, value):
        value = value.lower()
        if value not in controller.supports():
            raise serializers.ValidationError('Auto import only support oj_name in {}'.format(controller.supports()))
        return value

    def update(self, instance, validated_data):
        return instance

    def create(self, validated_data):
        instance = None

        return instance


class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'problems-detail'}
        }


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    teams = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='teams-detail')

    def create(self, validated_data):
        instance = super().create(validated_data)
        team = Team.objects.create(name='{}(个人)'.format(instance.name))
        team.members.add(instance)
        team.save()
        return team

    class Meta:
        model = Member
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'members-detail'}
        }


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    members = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='members-detail')

    class Meta:
        model = Team
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'teams-detail'}
        }


class RangeSerializer(serializers.Serializer):
    lower = serializers.IntegerField()
    upper = serializers.IntegerField()

    def validate(self, attrs):
        if attrs['lower'] > attrs['upper']:
            raise serializers.ValidationError('lower value can not less than upper value')
        if attrs['lower'] < 0 or attrs['upper'] < 0:
            raise serializers.ValidationError('lower value and upper value can not be negative')
        return attrs


class ContestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contest
        fields = ('team', 'problems',
                  'score', 'submit', 'accept', 'ac_rate_in_percent',
                  'problem_cnt', 'ignore_date', 'url')
        extra_kwargs = {
            'url': {'view_name': 'contests-detail'}
        }

    score = RangeSerializer(write_only=True, required=False, help_text='难度值范围')
    submit = RangeSerializer(write_only=True, required=False, help_text='提交数量范围')
    accept = RangeSerializer(write_only=True, required=False, help_text='通过数量范围')
    ac_rate_in_percent = RangeSerializer(write_only=True, required=False, help_text='通过率百分比范围')

    problem_cnt = serializers.IntegerField(write_only=True, help_text='需要的题目数量')
    ignore_date = serializers.DateField(required=False, write_only=True)

    problems = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='problems-detail')
    # team = serializers.SlugRelatedField(queryset=Team.objects.all(), slug_field='name')
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    # team = serializers.HyperlinkedRelatedField(read_only=True, view_name='teams-detail')

    def create(self, validated_data):
        team = validated_data['team']
        score = validated_data.pop('score', None)
        submit = validated_data.pop('submit', None)
        accept = validated_data.pop('accept', None)
        ac_rate_in_percent = validated_data.pop('ac_rate_in_percent', None)

        problem_cnt = validated_data.pop('problem_cnt')
        ignore_date = validated_data.pop('ignore_date', None)
        problems = Problem.objects.all()
        record_queryset = Record.objects.all() \
            if not ignore_date else Record.objects.filter(create_time__gte=ignore_date)

        for member in team.members.all():
            # 难度值，difficult_number字段中不等于-1进行过滤
            tol_team_ids = [item.id for item in member.teams.all()]
            qs = record_queryset.filter(team__id__in=tol_team_ids)
            q_object = Q()
            if score is not None:
                q_score = Q(problem__difficult_number__gte=score['lower'],
                            problem__difficult_number__lte=score['upper'])
                q_object.add(q_score, Q.OR)
            if submit is not None:
                q_submit = Q(problem__submitted_number__gte=submit['lower'],
                             problem__submitted_number__lte=submit['upper'])
                q_object.add(q_submit, Q.OR)
            if accept is not None:
                q_accept = Q(problem__accepted_number__gte=accept['lower'],
                             problem__accepted_number__lte=accept['upper'])
                q_object.add(q_accept, Q.OR)
            if ac_rate_in_percent is not None:
                q_ac_rate = Q(problem__ac_rate_in_percent__gte=ac_rate_in_percent['lower'],
                              problem__ac_rate_in_percent__lte=ac_rate_in_percent['upper'])
                q_object.add(q_ac_rate, Q.OR)
            qs = qs.filter(q_object)
            problems = problems.exclude(id__in=qs.values_list('problem__id', flat=True))

        exist_cnt = problems.count()
        if exist_cnt < problem_cnt:
            raise serializers.ValidationError('no enough problems, only %d but need %d.' % (exist_cnt, problem_cnt))

        problems = list(problems.order_by('difficult_number'))
        choice_problems = random.sample(problems, problem_cnt)

        contest = Contest.objects.create(team=team)
        contest.problems.add(*choice_problems)
        contest.save()

        return contest

    def update(self, instance, validated_data):
        raise serializers.ValidationError('No support for update contest')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        problems_cnt = len(data['problems'])
        tol_difficult_number = 0.0
        for problem in data['problems']:
            tol_difficult_number += problem['difficult_number']
        data['average_difficult_number'] = tol_difficult_number / problems_cnt
        return data
