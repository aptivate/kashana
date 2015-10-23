from django.test import TestCase
from django_dynamic_fixture import G
from ..models import (
    Indicator,
    LogFrame,
    Result,
    SubIndicator,
)


class SubindicatorTests (TestCase):

    def test_get_subindicators(self):
        """
        Indicator has a subindicators method that returns
        only the subindicators for the given Indicator
        """
        logframe = G(LogFrame)
        result = G(Result, log_frame=logframe, ignore_fields=['parent', 'rating'])
        indicator = G(Indicator, result=result)
        subindicator = G(SubIndicator, indicator=indicator, ignore_fields=['rating'])
        G(SubIndicator, indicator=G(Indicator, result=result), ignore_fields=['rating'])

        subindicators = indicator.get_subindicators()

        self.assertQuerysetEqual(subindicators, [repr(subindicator)])

    def test_get_default_subindicator(self):
        """
        When fetching Subindicators for an Indicator, if none
        exist, we shoiuld get a newly created fresh one with
        some appropriate default name.
        """
        logframe = G(LogFrame)
        result = G(Result, log_frame=logframe, ignore_fields=['parent', 'rating'])
        indicator = G(Indicator, result=result)
        assert not SubIndicator.objects.filter(indicator=indicator).exists()

        subindicators = indicator.get_subindicators()

        [si] = SubIndicator.objects.filter(indicator=indicator)
        self.assertEqual(si.name, SubIndicator.DEFAULT_NAME)
        self.assertQuerysetEqual(subindicators, [repr(si)])
