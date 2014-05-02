from collections import defaultdict

from django.views.generic import DetailView
from braces.views import LoginRequiredMixin
from spreadsheetresponsemixin.views import SpreadsheetResponseMixin
from logframe.models import (
    LogFrame, Result, Indicator, SubIndicator, Period, Milestone, Target,
    Actual
)
from bs4 import BeautifulSoup


def html2txt(html):
    value = html if html else u""
    soup = BeautifulSoup(value)
    return soup.get_text()


class ExportObjects(object):
    def __init__(self, logframe):
        self.objects = self.get_objects(logframe)
        self.mapping = self.__map_objects(self.objects, self.parent_attr)

    def get_objects(self, logframe):
        filter_kwargs = {self.filter_arg: logframe}
        return self.model.objects.filter(**filter_kwargs)

    def __map_objects(self, objects, parent_attr):
        o_map = defaultdict(list)
        for item in objects:
            o_map[getattr(item, parent_attr)].append(item)
        return o_map


class ExportSubIndicator(ExportObjects):
    model = SubIndicator
    parent_attr = "indicator_id"
    filter_arg = "indicator__result__log_frame"

    def get_subindicator_targets(self, milestone):
        mapping = {}
        targets = Target.objects.filter(milestone=milestone).values("value", "subindicator")
        for target in targets:
            mapping[target['subindicator']] = target['value']
        return mapping

    def get_value(self, subindicator):
        values = Actual.objects.filter(
            subindicator=subindicator).order_by("-column__date")
        if values.exists():
            return values[0].value
        else:
            return ""

    def get_rating(self, subindicator):
        return subindicator.rating.name if subindicator.rating else "unrated"

    def render_head(self):
        return ['', 'Milestone for period', 'Total to date', 'Rating']

    def render(self, subindicator):
        return [
            subindicator.name,
            self.targets.get(subindicator.id, u""),
            self.get_value(subindicator),
            self.get_rating(subindicator)
        ]


class ExportIndicator(ExportObjects):
    model = Indicator
    parent_attr = "result_id"
    filter_arg = "result__log_frame"

    def render(self, indicator):
        return [
            indicator.name or u"",
            html2txt(indicator.description)
        ]


class ExportLogframeData(LoginRequiredMixin, SpreadsheetResponseMixin, DetailView):
    model = LogFrame

    def get_results(self, logframe):
        def get_children(parent):
            reordered.append(parent)
            for r in results:
                if r.parent_id == parent.id:
                    get_children(r)

        results = Result.objects.filter(log_frame=logframe)
        reordered = []
        for r in results:
            if r.parent is None:
                get_children(r)
        return reordered

    def get_milestone(self, logframe, end_date):
        '''
        If possible return first milestone after period or last one before
        it otherwise.
        '''
        milestones = Milestone.objects.filter(log_frame=logframe).order_by("date")
        if milestones.filter(date__gte=end_date).exists():
            milestone = milestones.filter(date__gte=end_date)[0]
        else:
            milestones = list(milestones)
            milestone = milestones[-1] if len(milestones) else None
        return milestone

    def get_export_head(self, period):
        start, end = period
        return ['Quarterly report', '', start.isoformat(), end.isoformat()]

    def add_row(self, row=[], indent_cells=0):
        self.data.append([u""] * indent_cells + row)

    def get_data(self, **kwargs):
        '''
        Algorithm:
            fetch data
            print period header
            for each result:
                print result head
                for each indicator in result:
                    print indicator head
                    print subindicator head (milestone, total, RAG)
                    for each subindicator in indicator:
                        print subindicator (name, target, measurement, rating)
                    print empty line
                print empty line
        '''
        self.data = []
        logframe = self.get_object()
        period_obj = Period.objects.get(log_frame=logframe)
        period_interval = period_obj.get_period(kwargs.get("period"))

        milestone = self.get_milestone(logframe, period_interval[1])

        results = self.get_results(logframe)
        ind = ExportIndicator(logframe)
        subind = ExportSubIndicator(logframe)
        subind.targets = subind.get_subindicator_targets(milestone)

        self.add_row(self.get_export_head(period_interval))
        self.add_row()

        for result in results:
            self.add_row([
                result.name or u"",
                html2txt(result.description)
            ], 1)

            for indicator in ind.mapping[result.id]:
                self.add_row(ind.render(indicator), 1)
                self.add_row(subind.render_head(), 1)
                for subindicator in subind.mapping[indicator.id]:
                    self.add_row(subind.render(subindicator), 1)
                self.add_row()
            self.add_row()
        return self.data

    # Overrides the one from SpreadsheetResponseMixin
    def render_setup(self, **kwargs):
        self.get_data(**self.kwargs)
        return [self.data, None]

    def get(self, request, *args, **kwargs):
        return self.render_excel_response()
