from django.contrib import admin


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

    interval_size = 300
    number_of_intervals = 10

    def get_interval_length(self):
        return self.interval_size

    def lookups(self, request, model_admin):
        interval_length = self.get_interval_length()
        return (((-1, '(-∞, 0)'),) +
                tuple((i, f'[{i * interval_length}, {(i + 1) * interval_length})')
                      for i in range(self.number_of_intervals - 1)) +
                ((self.number_of_intervals - 1, f'[{(self.number_of_intervals - 1) * interval_length}, +∞)'),)
                )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        val = int(self.value())
        if val == -1:
            return queryset.filter(**{self.parameter_name + '__lt': 0})

        interval_length = self.get_interval_length()
        left, right = val * interval_length, (val + 1) * interval_length
        if val == self.number_of_intervals - 1:
            return queryset.filter(**{self.parameter_name + '__gte': left})
        return queryset.filter(**{self.parameter_name + '__gte': left, self.parameter_name + '__lt': right})
