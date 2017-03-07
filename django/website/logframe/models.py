from __future__ import unicode_literals

from datetime import date, timedelta
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.text import slugify

from organizations.models import Organization

from contacts.models import User

# http://djangosnippets.org/snippets/1054/


class AverageTargetPercentMixin(object):
    OK = 'ok'
    WARNING = 'warning'
    DANGER = 'danger'

    def _average_sequence(self, children, attr):
        value_list = [getattr(c, attr) for c in children]
        if len(value_list) == 0:
            return 0
        return sum(value_list) / len(value_list)

    def _calculate_target_percent(self, children):
        return self._average_sequence(children, 'target_percent')

    def _calculate_weighted_average(self, children, attr, weight_attr):
        if len(children) == 0:
            return 0
        weighted_percent_list = [getattr(c, attr) *
                                 getattr(c, weight_attr) for c in children]
        weighting_list = [getattr(c, weight_attr) for c in children]
        return sum(weighted_percent_list) / sum(weighting_list)

    def _calculate_weighted_target_percent(self, children):
        return self._calculate_weighted_average(children, 'target_percent', 'impact_weighting')

    def _calculate_summary_status(self, target_percent, budget_percent):
        if target_percent >= budget_percent:
            return self.OK
        elif target_percent < budget_percent - 10:
            return self.DANGER
        else:
            return self.WARNING


@python_2_unicode_compatible
class LogFrame(AverageTargetPercentMixin, models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )
    slug = models.SlugField(unique=True, help_text=(
        "A 'slug' can consist of letters, numbers, underscores or hyphens and "
        "can be up to 50 characters long."
    ))
    organization = models.ForeignKey(Organization)

    def average_target_percent(self):
        return self._calculate_weighted_target_percent(self.output_set.all())

    def average_budget_percent(self):
        return self._calculate_weighted_average(
            self.output_set.all(), 'budget_percent', 'impact_weighting')

    def average_activities_percent(self):
        return self._calculate_weighted_average(
            self.output_set.all(), 'activities_percent', 'impact_weighting')

    def summary_status(self):
        return self._calculate_summary_status(self.average_target_percent(),
                                              self.average_budget_percent())

    @cached_property
    def milestones(self):
        return self.milestone_set.all()

    def all_assumptions(self):
        """
        Return all assumptions transitively associated with (owned by)
        the curretnt logframe
        """
        return Assumption.objects.filter(result__log_frame=self)

    def get_unique_slug_name(self):
        count = LogFrame.objects.filter(slug__startswith=self.slug[:46]).count()

        max_length = LogFrame._meta.get_field('slug').max_length
        base_slug = slugify(self.name)
        slug = base_slug[:max_length]

        while LogFrame.objects.filter(slug=slug).exists():
            # Based on https://keyerror.com/blog/automatically-generating-unique-slugs-in-django at 03/03/2017
            count += 1
            slug = '{0}{1:d}'.format(base_slug[:max_length - len(unicode(count))], count)

        return slug

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.pk:
            self.slug = self.get_unique_slug_name()
        super(LogFrame, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class RiskRating(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Result(models.Model):
    """ abstract class to be used by Impact(/Goal), Outcome and Output """
    log_frame = models.ForeignKey(LogFrame, related_name='results')
    parent = models.ForeignKey("self", related_name="children",
                               null=True, blank=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    contribution_weighting = models.IntegerField(default=0)  # impact weighting in case of the Impact

    risk_rating = models.ForeignKey(RiskRating, null=True, blank=True)
    rating = models.ForeignKey("Rating", null=True, blank=True)

    # Meta
    level = models.SmallIntegerField(default=0)  # Used to know how deep in hiearchy we are
    order = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("design-result", args=[self.log_frame.id, self.id])

    def save(self, *args, **kwargs):
        if not self.level:
            self.level = 1 if not self.parent else self.parent.level + 1
        if not self.order:
            siblings = Result.objects.filter(log_frame=self.log_frame,
                                             level=self.level).order_by('-order')
            max_order = siblings[0].order if len(siblings) else 0
            self.order = max_order + 1
        super(Result, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Assumption(models.Model):
    description = models.TextField(blank=True)
    result = models.ForeignKey(Result, related_name='assumptions')

    def __str__(self):
        return self.description


@python_2_unicode_compatible
class Indicator(AverageTargetPercentMixin, models.Model):
    result = models.ForeignKey(Result, related_name='indicators')
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(null=True, blank=True)
    source = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_subindicators(self):
        """
        Returns the subindicators associated with this indicator.
        If there none, creates a default 'total' one and returns that.
        """
        if not SubIndicator.objects.filter(indicator=self).exists():
            SubIndicator(
                name=SubIndicator.DEFAULT_NAME,
                indicator=self,
                order=1
            ).save()
        return SubIndicator.objects.filter(indicator=self)


@python_2_unicode_compatible
class Term(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class OrderedTerm(Term):
    class Meta:
        abstract = True
        ordering = ['order']

    order = models.PositiveSmallIntegerField(
        blank=True,
        help_text="Set automatically when not specified.")

    owner = None

    def save(self, *args, **kwargs):
        if not self.order:
            aggregate_dict = self.__class__.objects.filter(
                **{self.owner: getattr(self, self.owner)}
            ).aggregate(models.Max('order'))
            current_order = aggregate_dict['order__max']
            self.order = 1 if not current_order else current_order + 1
        ret = super(Term, self).save(*args, **kwargs)
        # TODO use a modified version of cached_property that is reversible
        # self.log_frame.invalidate_cache()
        return ret


class Milestone(Term):
    """
    Currently there is no 'meta-model' element to define term-groups
    (taxonomies) so Milestone (and SubIndicator) are concrete sub-classes of
    Term are here to keep the values separate.
    """
    class Meta:
        ordering = ['date']

    log_frame = models.ForeignKey(LogFrame)
    date = models.DateField()


class SubIndicator(OrderedTerm):
    """
    Currently there is no 'meta-model' element to define term-groups
    (taxonomies) so SubIndicator (and Milestone) are concrete sub-classes of
    Term are here to keep the values separate. SubIndicator are owned by the
    indicator. The API will reflect this. If in the future we change the model
    here so that the indicator links to a term-group/taxonomy then there will
    still be a way to determine the set of sub-indicators for an inticator
    so the API can stay the same, but the query to fetch the mathcing items
    will change.
    """
    DEFAULT_NAME = "Total"
    owner = 'indicator'
    indicator = models.ForeignKey(Indicator, related_name='subindicators')
    rating = models.ForeignKey("Rating", null=True, blank=True)


@python_2_unicode_compatible
class Column(models.Model):
    indicator = models.ForeignKey(Indicator, related_name='columns')
    date = models.DateField()

    def __str__(self):
        return str(self.date)


class Measurement(models.Model):

    class Meta:
        abstract = True

    # timestamp = model
    value = models.CharField(max_length=200, blank=True)
    indicator = models.ForeignKey(Indicator)
    # Subindicator might become a tag (linked generically) in future, hence we
    # keep separate link to indicator
    subindicator = models.ForeignKey(SubIndicator, null=True, blank=True)

    def __str__(self):
        return self.value


class Target(Measurement):
    """
    A Target is associated with a row (subindicator) and column (milestone).
    This might be two separate relationships with Term, once we can group Terms
    into groups (taxonomies) and thus know which are valid values in each if
    these roles.  Currently there is no general tagging in the app but we do
    need these two special cases to display the results
    """
    milestone = models.ForeignKey(Milestone)


class Actual(Measurement):
    """
    An Actual meausrement is associated with a row (subindicator) inherited
    from Measurement, and a column (Column)
    """
    column = models.ForeignKey(Column)
    evidence = models.TextField(blank=True)


@python_2_unicode_compatible
class Activity(models.Model):
    class Meta:
        verbose_name_plural = "Activities"

    """ abstract class to be used by Impact(/Goal), Outcome and Output """
    log_frame = models.ForeignKey(LogFrame, related_name='activities')
    result = models.ForeignKey(Result, related_name="activities")
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    deliverables = models.TextField(blank=True)
    lead = models.ForeignKey(User, null=True, blank=True)
    # Timing
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    # Meta
    order = models.IntegerField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.order:
            siblings = Activity.objects.filter(
                log_frame=self.log_frame, result=self.result).order_by('-order')
            max_order = siblings[0].order if len(siblings) else 0
            self.order = max_order + 1
        super(Activity, self).save(*args, **kwargs)


@python_2_unicode_compatible
class BudgetLine(models.Model):
    activity = models.ForeignKey(Activity, related_name="others")
    name = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class TAType(OrderedTerm):
    """
    Currently there is no 'meta-model' element to define term-groups
    (taxonomies) so Milestone (and SubIndicator) are concrete sub-classes of
    Term are here to keep the values separate.
    """
    owner = 'log_frame'  # would be organization, if we had one
    log_frame = models.ForeignKey(LogFrame)


@python_2_unicode_compatible
class TALine(models.Model):
    activity = models.ForeignKey(Activity, related_name="tas")
    type = models.ForeignKey(TAType, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    band = models.CharField(max_length=10, null=True, blank=True)  # TODO: This should als be a taxonomy value
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    no_days = models.IntegerField(null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name if self.name else ""


class StatusCode(OrderedTerm):
    """
    These are the classifications for status updates.
    Should become a Taxonomy item when we do that refactor
    """
    owner = 'log_frame'  # would be organization, if we had one
    log_frame = models.ForeignKey(LogFrame)


@python_2_unicode_compatible
class StatusUpdate(models.Model):
    activity = models.ForeignKey(Activity, related_name="status_updates")
    code = models.ForeignKey(StatusCode, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.description if self.description else ""


#
# RATING
#
colors = (
    ('green', 'Green'),
    ('yellow', 'Yellow'),
    ('red', 'Red'),
    ('lightest-grey', 'Lightest grey'),
    ('light-grey', 'Light grey'),
    ('grey', 'Grey'),
)


@python_2_unicode_compatible
class Rating(models.Model):
    log_frame = models.ForeignKey(LogFrame)
    name = models.CharField(max_length=64)
    # Used as class name on front-end for coloring
    color = models.CharField(max_length=32, choices=colors)

    def __str__(self):
        return self.name


#
# PERIODS
#
MONTH_CHOICES = (
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),
)

PERIODS = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (6, 6)
)


@python_2_unicode_compatible
class Period(models.Model):
    log_frame = models.OneToOneField(LogFrame)
    start_month = models.PositiveSmallIntegerField(default=1, choices=MONTH_CHOICES)
    num_periods = models.PositiveSmallIntegerField(default=4, choices=PERIODS)

    def get_periods(self, start_date, end_date):
        periods_begin = [self.start_month + (12 / self.num_periods) * p for p
                         in range(self.num_periods)]
        periods = []
        # Start year earlier to catch also start: 1.1. End is always covered by
        # the last period of the year
        for year in range(start_date.year - 1, end_date.year + 1):
            for month in periods_begin:
                periods.append({
                    'start': date(year, month, 1),
                    'name': "{0} {1}".format(MONTH_CHOICES[month - 1][1], year)
                })
        start = end = 0
        for i, period in enumerate(periods):
            if period['start'] < start_date:
                start = i
            if period['start'] > end_date:
                end = i
                break
        if not end:
            end = len(periods)
        periods = periods[start:end]
        return periods

    def get_period(self, start_date):
        start_date = date(*[int(x) for x in start_date.split("-")])
        new_month = start_date.month + (12 / self.num_periods)

        add_year = 0 if new_month < 13 else 1
        new_month = new_month if new_month < 13 else new_month % 12

        next_period = date(start_date.year + add_year, new_month, 1)
        return (start_date, next_period - timedelta(days=1))

    def __str__(self):
        return 'Periods for logframe %s' % self.log_frame.name


class ResultLevelName(models.Model):
    level_number = models.IntegerField()
    level_name = models.CharField(max_length=128)
    logframe = models.ForeignKey(LogFrame)

    class Meta:
        unique_together = (('level_number', 'logframe'),)

    def __str__(self):
        return '{0} [{1} - {2}]'.format(self.logframe.name,
                                        self.level_number,
                                        self.level_name)
