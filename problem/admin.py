from django.contrib import admin
from django.db.models.query import Q

from problem.models import Team, Member, Problem, Record
from problem.filters import PercentageFilterMixin, IntervalFilterMixin


class ACRatePercentageFilter(PercentageFilterMixin):

    title = 'AC Rate in Percentage'
    parameter_name = 'ac_rate_in_percent'


class DifficultNumberIntervalFilter(IntervalFilterMixin):

    title = 'Difficult Number Interval Filter'
    parameter_name = 'difficult_number'

    interval_size = 300
    number_of_intervals = 10


class AcceptNumberIntervalFilter(IntervalFilterMixin):

    title = 'Accept Number Interval Filter'
    parameter_name = 'accepted_number'

    interval_size = 10000
    number_of_intervals = 10


class ProblemSolvedByTeamFilter(admin.SimpleListFilter):

    title = 'Team With Solved Problem'
    parameter_name = 'solved_teams'

    def lookups(self, request, model_admin):
        return ((team.name, team.name) for team in Team.objects.all())

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.filter(solved_teams__name=self.value())


class ProblemUnSolvedByTeamFilter(admin.SimpleListFilter):

    title = 'Team With Unsolved Problem'
    parameter_name = 'unsolved_teams'

    def lookups(self, request, model_admin):
        return ((team.name, team.name) for team in Team.objects.all())

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.filter(~Q(solved_teams__name=self.value()))


def create_record(modeladmin, request, queryset):
    team = Team.objects.filter(active=True).first()
    for problem in queryset:
        Record.objects.create(problem=problem, team=team)


create_record.short_description = "Create a Record on problem selected with current active team"


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):

    list_display = ('name', 'active')
    autocomplete_fields = ('members',)


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'accepted_number', 'submitted_number', 'difficult_number',
                    'ac_rate_in_percent', 'origin_link', 'problem_tags')

    list_filter = ('oj', ACRatePercentageFilter, DifficultNumberIntervalFilter,
                   AcceptNumberIntervalFilter, ProblemSolvedByTeamFilter, ProblemUnSolvedByTeamFilter)

    filter_vertical = ('tags', )
    search_fields = ('problem_tags', )

    actions = [create_record]


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):

    search_fields = ('name', 'nickname')


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):

    list_display = ('team', 'problem', 'create_time')

    autocomplete_fields = ('problem',)
