from django.contrib import admin

from problem.models import Team, Member, Problem, Record


class PercentageFilterMixin(admin.SimpleListFilter):

    def lookups(self, request, model_admin):
        return (
                (0, '[0%, 20%)'),
                (1, '[20%, 40%)'),
                (2, '[40%, 60%)'),
                (3, '[60%, 80%)'),
                (4, '[80%, 100%)')
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        left, right = 20 * int(self.value()), 20 * (int(self.value()) + 1)
        return queryset.filter(**{self.parameter_name + '__gte': left, self.parameter_name + '__lte': right})


class IntervalFilterMixin(admin.SimpleListFilter):

    min_val = 0
    max_val = 3000
    number_of_intervals = 10

    def get_interval_length(self):
        return (self.max_val - self.min_val) // self.number_of_intervals

    def lookups(self, request, model_admin):
        interval_length = self.get_interval_length()
        return (((-1, '-1'),) +
                tuple((i, f'[{i * interval_length}, {(i + 1) * interval_length})')
                      for i in range(self.number_of_intervals - 1)) +
                ((self.number_of_intervals - 1, f'[{(self.number_of_intervals - 1) * interval_length}, {self.max_val})'),)
                )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        val = int(self.value())
        if val == -1:
            return queryset.filter(**{self.parameter_name: val})

        interval_length = self.get_interval_length()
        left, right = val * interval_length, (val + 1) * interval_length
        if val == self.number_of_intervals - 1:
            right = self.max_val
        return queryset.filter(**{self.parameter_name + '__gte': left, self.parameter_name + '__lt': right})


class ACRatePercentageFilter(PercentageFilterMixin):

    title = 'AC Rate in Percentage'
    parameter_name = 'ac_rate_in_percent'


class DifficultNumberIntervalFilter(IntervalFilterMixin):

    title = 'Difficult Number Interval Filter'
    parameter_name = 'difficult_number'

    min_val = 0
    max_val = 3000
    number_of_intervals = 10


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'accepted_number', 'submitted_number', 'difficult_number',
                    'ac_rate_in_percent', 'origin_link', 'problem_tags')

    list_filter = ('oj', ACRatePercentageFilter, DifficultNumberIntervalFilter)

    filter_vertical = ('tags', )
    search_fields = ('problem_tags', )


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    pass
