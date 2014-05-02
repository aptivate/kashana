import django_tables2 as tables
from django_tables2.utils import A
from .models import User


class UserTable(tables.Table):
    first_name = tables.LinkColumn('contact_update', args=[A('pk')])
    last_name = tables.LinkColumn('contact_update', args=[A('pk')])

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'business_email')
        order_by = ('id', 'first_name', 'last_name')
        attrs = {'class': 'pure-table'}
