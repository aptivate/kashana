from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from django_tables2.columns import Column, LinkColumn
from django_tables2.tables import Table
from django_tables2.utils import A

from .models import LogFrame


class LogframeManagementTable(Table):
    name = Column()
    slug = Column()
    edit = LinkColumn(
        'update-logframe',
        args=[A('slug')],
        text=mark_safe('<img src="{0}admin/img/icon_changelink.gif" alt="{1}" />'.format(settings.STATIC_URL, _("Edit Logframe"))),
        orderable=False,
        empty_values=()
    )
    delete = LinkColumn(
        'delete-logframe',
        args=[A('slug')],
        text=mark_safe('<img src="{0}admin/img/icon_deletelink.gif" alt="{1}" />'.format(settings.STATIC_URL, _("Delete Logframe"))),
        orderable=False,
        empty_values=()
    )

    class Meta:
        model = LogFrame
        attrs = {"class": "paleblue"}
