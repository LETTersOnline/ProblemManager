from django.contrib import admin

from problem.models import Team, Member, Problem, Record


class PercentageFilterMixin(admin.SimpleListFilter):

    def lookups(self, request, model_admin):
        return (
                (0, '0% ~ 20%'),
                (1, '20% ~ 40%'),
                (2, '40% ~ 60%'),
                (3, '60% ~ 80%'),
                (4, '80% ~ 100%')
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        left, right = 20 * int(self.value()), 20 * (int(self.value()) + 1)
        return queryset.filter(**{self.parameter_name + '__gte': left, self.parameter_name + '__lte': right})


class ACRatePercentageFilter(PercentageFilterMixin):

    title = 'AC Rate in Percentage'
    parameter_name = 'ac_rate_in_percent'



@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'accepted_number', 'submitted_number', 'difficult_number',
                    'ac_rate_in_percent', 'origin_link')

    list_filter = ('oj', ACRatePercentageFilter)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    pass
