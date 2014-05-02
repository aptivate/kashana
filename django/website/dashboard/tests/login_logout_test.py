import pytest

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django_dynamic_fixture import G

from contacts.tests.factories import UserFactory
from logframe.models import LogFrame, Result
from dashboard.views import Home


class FrontpageTests(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.view = Home.as_view()
        lf = G(LogFrame)
        G(Result, log_frame=lf, parent=None)

    @pytest.mark.integration
    def test_homepage_logged_out(self):
        request = RequestFactory().get('/')
        response = self.view(request)
        next_url = "{0}?next={1}".format(reverse("login"), reverse("home"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], next_url)

    @pytest.mark.integration
    def test_homepage_logged_in(self):
        request = RequestFactory().get('/')
        request.user = self.user  # So we're logged in
        response = self.view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse("dashboard"))

    @pytest.mark.integration
    @pytest.mark.client
    def test_login(self):
        email = self.user.business_email
        password = 'fakepass'
        self.user.set_password(password)
        self.user.save()

        # Can we log in?
        login_data = {
            'username': email,
            'password': password,
        }
        c = Client()
        response = c.post(reverse('login'), login_data, follow=True)
        self.assertContains(response, 'Log out')
