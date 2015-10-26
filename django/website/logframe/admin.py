from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .widgets import ColorSelect

from .models import (
    LogFrame,
    Result,
    RiskRating,
    Milestone,
    Assumption,
    Indicator,
    SubIndicator,
    Column,
    Actual,
    Target,
    Activity,
    BudgetLine,
    TALine,
    TAType,
    StatusCode,
    StatusUpdate,
    Rating,
    Period,

    colors
)


class ResultAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'log_frame')


class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'log_frame')


class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'result')


class SubIndicatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'indicator', 'result')

    def result(self, obj):
        return obj.indicator.result
    result.short_description = 'result'


class AssumptionAdmin(admin.ModelAdmin):
    list_display = ('description', 'result')


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'result')


class ActualAdmin(admin.ModelAdmin):
    list_display = (
        'indicator',
        'subindicator',
        'column',
        'value'
    )


class TALineAdmin(admin.ModelAdmin):
    list_display = ('name', 'activity')


class StatusUpdateAdmin(admin.ModelAdmin):
    list_display = ('activity', 'date', 'user', 'code', 'description')


#
# Rating
#
class RatingForm(forms.ModelForm):
    color = forms.ChoiceField(widget=ColorSelect, choices=colors)

    class Meta:
        model = Rating

    class Media:
        css = {
            "all": ("kashana/admin.css",)
        }


class RatingAdmin(admin.ModelAdmin):
    form = RatingForm
    list_display = ('name', 'colored_name', 'log_frame')

    def colored_name(self, obj):
        color_code = ""
        color_name = "Unknown"
        for code, name in colors:
            if code == obj.color:
                color_code = code
                color_name = name
                break
        return format_html('<span class="rating-list-item {0}">{1}</span>',
                           color_code,
                           color_name)
    colored_name.allow_tags = True

    class Media:
        css = {
            "all": ("kashana/admin.css",)
        }


admin.site.register(LogFrame)
admin.site.register(Result, ResultAdmin)
admin.site.register(Milestone, MilestoneAdmin)
admin.site.register(RiskRating)
admin.site.register(Assumption, AssumptionAdmin)
admin.site.register(Indicator, IndicatorAdmin)
admin.site.register(SubIndicator, SubIndicatorAdmin)
admin.site.register(Column)
admin.site.register(Target)
admin.site.register(Actual, ActualAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(BudgetLine)
admin.site.register(TALine, TALineAdmin)
admin.site.register(TAType)
admin.site.register(StatusCode)
admin.site.register(StatusUpdate, StatusUpdateAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Period)
