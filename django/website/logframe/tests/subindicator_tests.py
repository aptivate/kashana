from django.test import TestCase
from django_dynamic_fixture import G
from ..models import (
    Indicator,
    SubIndicator,
)


class SubindicatorTests (TestCase):

    def test_get_subindicators(self):
        """
        Indicator has a subindicators method that returns
        only the subindicators for the given Indicator
        """
        indicator = G(Indicator)
        subindicator = G(SubIndicator, indicator=indicator)
        G(SubIndicator)

        subindicators = indicator.get_subindicators()

        self.assertQuerysetEqual(subindicators, [repr(subindicator)])

    def test_get_default_subindicator(self):
        """
        When fetching Subindicators for an Indicator, if none
        exist, we shoiuld get a newly created fresh one with
        some appropriate default name.
        """
        indicator = G(Indicator)
        assert not SubIndicator.objects.filter(indicator=indicator).exists()

        subindicators = indicator.get_subindicators()

        [si] = SubIndicator.objects.filter(indicator=indicator)
        self.assertEqual(si.name, SubIndicator.DEFAULT_NAME)
        self.assertQuerysetEqual(subindicators, [repr(si)])
