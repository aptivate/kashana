# coding=utf-8
from random import randint

from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from django_tables2 import SingleTableMixin

from braces.views import LoginRequiredMixin, PermissionRequiredMixin
import mock
import openpyxl
import pytest

from ..views import (
    AddContact,
    DeleteContact,
    ListContacts,
    ListContactsExport,
    UpdateContactBase,
    UpdateContact,
    UpdatePersonalInfo,
)
from ..forms import (
    AddContactForm,
    UpdatePersonalInfoForm,
)
from .factories import UserFactory, ContactsManagerFactory


class BracesMixinTests(TestCase):
    def test_views_have_login_required_mixin(self):
        views_with_login_required = [ListContacts,
                                     AddContact,
                                     UpdateContactBase,
                                     UpdateContact,
                                     UpdatePersonalInfo,
                                     DeleteContact]
        for view in views_with_login_required:
            self.assertIsInstance(view(),
                                  LoginRequiredMixin,
                                  "%s does not have LoginRequired" % view)

    def test_views_have_permission_required_mixin(self):
        views_with_permission_required = [ListContacts,
                                          AddContact,
                                          UpdateContact,
                                          DeleteContact]
        for view in views_with_permission_required:
            self.assertIsInstance(view(),
                                  PermissionRequiredMixin,
                                  "%s does not have PermissionRequired" % view)


class SuccessUrlTests(TestCase):
    def test_views_with_success_url_is_contact_list(self):
        views_with_contact_list_success_url = [ListContacts,
                                               DeleteContact]
        for view in views_with_contact_list_success_url:
            self.assertEqual(view().get_success_url(),
                             reverse('contact_list'),
                             "%s does not have contact_list as success_url"
                             % view)

    def test_views_with_success_url_is_contact_page(self):
        views_with_contact_page_success_url = [AddContact,
                                               UpdateContactBase,
                                               UpdateContact]
        for view in views_with_contact_page_success_url:
            view.request = RequestFactory().post('/', {})
            view.object = mock.Mock(id=3)
            self.assertEqual(view().get_success_url(),
                             reverse('contact_update', args=(view.object.id,)),
                             "%s does not have contact_update as success_url"
                             % view)

    def test_views_with_success_url_is_home(self):
        views_with_home_success_url = [UpdatePersonalInfo]
        for view in views_with_home_success_url:
            self.assertEqual(view().get_success_url(),
                             reverse('home'),
                             "%s does not have home as success_url"
                             % view)


@pytest.mark.groupfactory
class ListContactsTests(TestCase):
    """
    Tests for ListContacts Class
    """

    @pytest.mark.django_db
    def setUp(self):
        self.user = ContactsManagerFactory()
        self.request = RequestFactory().get('/', {'q': 'searchterm'})
        self.request.user = self.user
        self.view = ListContacts.as_view()

    def test_has_singletablemixin(self):
        self.assertIsInstance(ListContacts(), SingleTableMixin)

    def test_number_of_not_active_contacts_in_context(self):
        # TODO: not_active is defined by the password field not the is_active
        # field, is that what we want (just remembering conversation from
        # today - Aug 22)?
        UserFactory(password='bob')
        UserFactory()
        response = self.view(self.request)
        # Expect 2 with no password (one from setup, one from this test)
        self.assertEqual(response.context_data['num_notactive'], 2)

    def test_get_queryset_returns_a_subset_from_first_name_search(self):
        searched_user = UserFactory(first_name="searchterm")
        response = self.view(self.request)
        self.assertListEqual(list(response.context_data['object_list']),
                             [searched_user])

    def test_get_queryset_returns_a_subset_from_last_name_search(self):
        searched_user = UserFactory(last_name="searchterm")
        response = self.view(self.request)
        self.assertListEqual(list(response.context_data['object_list']),
                             [searched_user])

    def test_get_queryset_returns_a_subset_from_business_email_search(self):
        searched_user = UserFactory(business_email="searchterm")
        response = self.view(self.request)
        self.assertListEqual(list(response.context_data['object_list']),
                             [searched_user])


class AddContactTests(TestCase):

    def setUp(self):
        self.view = AddContact()
        self.form = mock.Mock(spec=AddContactForm)
        self.form.save = mock.Mock(return_value=mock.Mock(id=1))
        self.form.cleaned_data = {}

    def test_has_expected_permissions_properties(self):
        self.assertEqual(self.view.permission_required, 'contacts.add_user')
        self.assertTrue(self.view.raise_exception)

    def test_form_valid_calls_save_on_form(self):
        self.view.form_valid(self.form)
        self.form.save.assert_called_with()

    def test_form_valid_calls_save_on_object(self):
        self.view.form_valid(self.form)
        self.view.object.save.assert_called_with()

    def test_form_valid_sets_an_unusable_password(self):
        self.view.form_valid(self.form)
        self.view.object.set_unusable_password.assert_called_once_with()


class DeleteContactTests(TestCase):

    def test_has_expected_permissions_properties(self):
        view = DeleteContact()
        self.assertEqual(view.permission_required, 'contacts.delete_user')
        self.assertTrue(view.raise_exception)


class UpdateContactTests(TestCase):
    def test_has_expected_permissions_properties(self):
        view = UpdateContact()
        self.assertEqual(view.permission_required, 'contacts.add_user')
        self.assertTrue(view.raise_exception)

    def test_form_valid_redirects_to_claim_url_if_save_and_email(self):
        view = UpdateContact()
        view.request = RequestFactory().post('/')
        view.request.POST.update({'save-and-email': ''})
        view.object = mock.Mock(id=3)
        assert view.get_success_url() == reverse('contact_claim_account', args=(3,))


class UpdatePersonalInfoTests(TestCase):
    def test_is_instance_of_update_contacts_base(self):
        self.assertIsInstance(UpdatePersonalInfo(), UpdateContactBase)

    def test_has_expected_properties(self):
        view = UpdatePersonalInfo()
        self.assertEqual(view.form_class, UpdatePersonalInfoForm)

    def test_get_object_returns_request_user(self):
        view = UpdatePersonalInfo()
        request = RequestFactory()
        request.user = UserFactory.build()
        view.request = request
        self.assertEqual(view.get_object(), request.user)


###############################
# pytest style starts here
###############################
def test_update_contact_form_invalid_adds_a_message_to_messages(rf):
    view = UpdateContact()
    view.object = mock.MagicMock()
    r = rf.get('/')
    view.request = r
    form = mock.MagicMock()
    with mock.patch('contacts.views.contact_info.messages') as messages:
        view.form_invalid(form)
        messages.error.assert_called_once_with(r, 'Contact data not valid, \
                please check and try again.')


@pytest.mark.django_db
def test_search_term_puts_query_in_context(rf):
    view = ListContacts()
    r = rf.get('/?q=bla')
    view.request = r
    view.object_list = []
    ctx = view.get_context_data(object_list=[])
    assert ctx['query'] == 'bla'


@pytest.mark.django_db
def test_no_search_term_results_in_empty_query_in_context(rf):
    view = ListContacts()
    r = rf.get('/')
    view.request = r
    view.object_list = []
    ctx = view.get_context_data(object_list=[])
    assert ctx['query'] == ''


def create_contact_list():
    return [ContactsManagerFactory() for _ in range(3)]


@pytest.mark.django_db
def test_contacts_list_csv_export():
    contacts = create_contact_list()

    request = RequestFactory().get('/')

    view = ListContactsExport()
    view.request = request

    expected_text_lines = [
        u'Business Email,First Name,Last Name\r\n',
    ]

    for user in contacts:
        user_number = user.first_name.split(' ')[1]
        expected_text_lines.append(
            u'email{0}@test.com,ｆíｒѕｔ {0},ｌåｓｔɭａｓｔ {0}\r\n'.format(user_number)
        )

    expected_text = u"".join(expected_text_lines)

    response = view.get(request, format='csv')

    assert expected_text == response.content.decode('UTF-8')


@pytest.mark.django_db
def test_contacts_list_excel_export():
    contacts = create_contact_list()

    request = RequestFactory().get('/')

    view = ListContactsExport()
    view.request = request

    expected_text_lines = [
        u'Business Email,First Name,Last Name\r\n',
    ]

    for user in contacts:
        user_number = user.first_name.split(' ')[1]
        expected_text_lines.append(
            u'email{0}@test.com,ｆíｒѕｔ {0},ｌåｓｔɭａｓｔ {0}\r\n'.format(user_number)
        )

    expected_text = u"".join(expected_text_lines)

    response = view.get(request, format='excel')

    workbook = openpyxl.load_workbook(ContentFile(response.content))

    worksheet = workbook.worksheets[0]

    actual_text_lines = []
    for row in worksheet.rows:
        row_contents = u",".join([unicode(cell.value) for cell in row])
        actual_text_lines.append(row_contents + u"\r\n")

    actual_text = u"".join(actual_text_lines)

    assert expected_text == actual_text


def test_update_contact_view_with_valid_form_saves_object():
    view = UpdateContact()
    view.request = RequestFactory().post('/', {})
    view.object = mock.Mock(save=mock.Mock())
    view.form_valid(mock.Mock(save=lambda: mock.Mock(id=randint(1, 100))))

    assert view.object.save.called


def test_update_contact_view_with_valid_form_redirects_to_self():
    CONTACT_ID = 1
    view = UpdateContact()
    view.request = RequestFactory().post('/', {})
    view.object = mock.Mock(save=mock.Mock())
    response = view.form_valid(mock.Mock(save=lambda: mock.Mock(id=CONTACT_ID)))

    assert reverse('contact_update', args=[CONTACT_ID]) == response['Location']
