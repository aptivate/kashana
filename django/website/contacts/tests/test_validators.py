from datetime import date
from django.test import TestCase
from django.core.exceptions import ValidationError
from contacts.validators import year_to_now


today = date.today()
this_year = today.year


class ValidatorTests(TestCase):
    def test_year_to_now(self):
        self.assertRaises(ValidationError, year_to_now, 1899)
        self.assertRaises(ValidationError, year_to_now, '1899')

        self.assertRaises(ValidationError, year_to_now, this_year)
        self.assertRaises(ValidationError, year_to_now, this_year + 3)

        self.assertIsNone(year_to_now(1900))
        self.assertIsNone(year_to_now(this_year - 1))

    def test_calling_year_to_now_with_non_integer_throws_value_error(self):
        self.assertRaises(ValidationError, year_to_now, 'a')
        self.assertRaises(ValidationError, year_to_now, '1900.1')
