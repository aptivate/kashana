from django.test import TestCase
from contacts.templatetags import basename


class TemplateTagsTests(TestCase):
    def test_basename(self):
        self.assertEqual(basename.basename('/not/very/long/path/file.exe'),
                         'file.exe')
        self.assertEqual(basename.basename('/not/very/long/path/'),
                         '')
