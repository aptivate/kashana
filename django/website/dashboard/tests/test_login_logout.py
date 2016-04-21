import pytest

from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django_dynamic_fixture import G

from contacts.tests.factories import UserFactory
from logframe.models import LogFrame, Result, Rating
from dashboard.views import Home


class FrontpageTests(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.view = Home.as_view()

        # Logframe is now created automatically, don't create it if it exists

        try:
            lf = LogFrame.objects.get()
        except LogFrame.DoesNotExist:
            lf = G(LogFrame)

        rating = G(Rating, log_frame=lf)
        G(Result, log_frame=lf, parent=None, rating=rating)

    @pytest.mark.integration
    def test_homepage_logged_out(self):
        request = RequestFactory().get('/')
        request.user = AnonymousUser()
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
