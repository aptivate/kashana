from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.views.generic import (
    CreateView, UpdateView, DeleteView, ListView,
)

from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from spreadsheetresponsemixin.views import SpreadsheetResponseMixin
from django_tables2 import SingleTableMixin

from contacts.models import User
from contacts.forms import (
    AddContactForm, UpdateContactForm, DeleteContactForm,
    UpdatePersonalInfoForm
)
from contacts.tables import UserTable


class ListContacts(LoginRequiredMixin, PermissionRequiredMixin,
                   SingleTableMixin, ListView):
    model = User
    table_class = UserTable
    orderable_columns = ('id', 'first_name', 'last_name')
    orderable_columns_default = 'id'
    template_name = 'contacts/list_contacts.html'
    # Group required
    permission_required = 'contacts.add_user'
    raise_exception = True

    def get_success_url(self):
        return reverse('contact_list')

    def get_context_data(self, **kwargs):
        context = super(ListContacts, self).get_context_data(**kwargs)
        context['num_notactive'] = User.objects.filter(Q(password='!') |
                                                       Q(password='')).count()
        context['query'] = self.request.GET.get("q", "")
        return context

    def get_queryset(self):
        if 'q' in self.request.GET:
            query = self.request.GET['q'].lower()
            qs = self.model.objects
            return qs.filter(Q(first_name__icontains=query) |
                             Q(last_name__icontains=query) |
                             Q(business_email__icontains=query) |
                             Q(personal_email__icontains=query))
        else:
            return self.model.objects.all()


class ListContactsExport(SpreadsheetResponseMixin, ListContacts):
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        fields = ('business_email', 'first_name', 'last_name', 'title',
                  'personal_email', 'is_active', 'contact_type',
                  'home_address')
        list_format = kwargs.get('format')
        if list_format == 'csv':
            return self.render_csv_response(queryset=queryset,
                                            fields=fields)
        elif list_format == 'excel':
            return self.render_excel_response(queryset=queryset,
                                              fields=fields)
        else:
            return super(ListContactsExport, self).get(request,
                                                       *args,
                                                       **kwargs)


class AddContact(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = User
    form_class = AddContactForm
    template_name = 'contacts/edit_contact.html'
    # Group required
    permission_required = 'contacts.add_user'
    raise_exception = True

    def get_success_url(self):
        return reverse('contact_update', args=(self.object.id,))

    def form_valid(self, form):
        self.object = form.save()
        self.object.set_unusable_password()
        self.object.save()
        return super(AddContact, self).form_valid(form)


class UpdateContactBase(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'contacts/edit_contact.html'

    def get_success_url(self):
        if 'save-and-email' in self.request.POST:
            url = reverse('contact_claim_account', args=(self.object.id,))
        else:
            url = reverse('contact_update', args=(self.object.id,))
        return url


class UpdateContact(PermissionRequiredMixin, UpdateContactBase):
    form_class = UpdateContactForm
    permission_required = 'contacts.add_user'
    raise_exception = True

    def form_invalid(self, form):
        messages.error(self.request, ('Contact data not valid, \
                please check and try again.'))
        return super(UpdateContact, self).form_invalid(form)

    def form_valid(self, form):
        # Save object and return redirect
        redirect = super(UpdateContact, self).form_valid(form)
        self.object.save()
        return redirect


class UpdatePersonalInfo(UpdateContactBase):
    form_class = UpdatePersonalInfoForm

    def get_success_url(self):
        return reverse('home')

    def get_object(self):
        return self.request.user


class DeleteContact(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = User
    template_name = 'contacts/delete_contact.html'
    form_class = DeleteContactForm
    # Group required
    permission_required = 'contacts.delete_user'
    raise_exception = True

    def get_success_url(self):
        return reverse('contact_list')
